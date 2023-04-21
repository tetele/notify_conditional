"""Conditional platform for notify component."""
from __future__ import annotations

import asyncio
from collections.abc import Mapping
from copy import deepcopy
from typing import Any

import voluptuous as vol

from homeassistant.components.automation import IfAction
from homeassistant.components.notify import (
    ATTR_DATA,
    ATTR_MESSAGE,
    ATTR_TARGET,
    ATTR_TITLE,
    DOMAIN as NOTIFY_DOMAIN,
    NOTIFY_SERVICE_SCHEMA,
    PLATFORM_SCHEMA,
    BaseNotificationService,
)
from homeassistant.const import ATTR_SERVICE
from homeassistant.core import HomeAssistant
from homeassistant.exceptions import (
    ConditionError,
    ConditionErrorContainer,
    ConditionErrorIndex,
    HomeAssistantError,
)
from homeassistant.helpers import condition
import homeassistant.helpers.config_validation as cv
from homeassistant.helpers.trace import trace_path
from homeassistant.helpers.typing import ConfigType, DiscoveryInfoType

from .const import LOGGER

CONF_SERVICES = "services"
CONF_CONDITION = "condition"

FORWARDED_ATTRIBUTES = (
    ATTR_MESSAGE,
    ATTR_TITLE,
    ATTR_TARGET,
    ATTR_DATA,
)

PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Required(CONF_SERVICES): vol.All(
            cv.ensure_list,
            [
                NOTIFY_SERVICE_SCHEMA.extend(
                    {
                        vol.Required(ATTR_SERVICE): cv.entity_domain(NOTIFY_DOMAIN),
                        vol.Required(CONF_CONDITION): vol.All(
                            cv.ensure_list, [cv.CONDITION_SCHEMA]
                        ),
                    }
                )
            ],
        )
    }
)


def add_defaults(
    input_data: dict[str, Any], default_data: dict[str, Any]
) -> dict[str, Any]:
    """Deep update a dictionary with default values."""
    for key, val in default_data.items():
        if isinstance(val, Mapping):
            input_data[key] = add_defaults(input_data.get(key, {}), val)  # type: ignore[arg-type]
        elif key not in input_data:
            input_data[key] = val
    return input_data


async def async_get_service(
    hass: HomeAssistant,
    config: ConfigType,
    discovery_info: DiscoveryInfoType | None = None,
) -> ConditionalNotifyPlatform:
    """Get the Conditional notification service."""
    return ConditionalNotifyPlatform(hass, config[CONF_SERVICES])


async def _async_process_if(
    hass: HomeAssistant, name: str, config: dict[str, Any]
) -> IfAction | None:
    """Process if checks."""
    if_configs = config[CONF_CONDITION]

    checks: list[condition.ConditionCheckerType] = []
    for if_config in if_configs:
        try:
            checks.append(await condition.async_from_config(hass, if_config))
        except HomeAssistantError as ex:
            LOGGER.warning("Invalid condition: %s", ex)
            return None

    def if_action(variables: Mapping[str, Any] | None = None) -> bool:
        """AND all conditions."""
        errors: list[ConditionErrorIndex] = []
        for index, check in enumerate(checks):
            try:
                with trace_path(["condition", str(index)]):
                    if check(hass, variables) is False:
                        return False
            except ConditionError as ex:
                errors.append(
                    ConditionErrorIndex(
                        "condition", index=index, total=len(checks), error=ex
                    )
                )

        if errors:
            LOGGER.warning(
                "Error evaluating condition for '%s':\n%s",
                name,
                ConditionErrorContainer("condition", errors=errors),
            )
            return False

        return True

    result: IfAction = if_action  # type: ignore[assignment]
    result.config = if_configs

    return result


class ConditionalNotifyPlatform(BaseNotificationService):
    """Implement the notification service for the group notify platform."""

    def __init__(self, hass: HomeAssistant, entities: list[dict[str, Any]]) -> None:
        """Initialize the service."""
        self.hass = hass
        self.entities = entities

    async def async_send_message(self, message: str = "", **kwargs: Any) -> None:
        """Send message to all entities in the group."""
        payload: dict[str, Any] = {ATTR_MESSAGE: message}
        payload.update({key: val for key, val in kwargs.items() if val})

        tasks: list[asyncio.Task[bool | None]] = []
        for entity in self.entities:
            variables: dict[str, Any] = {
                "entity": entity,
            }
            forwarded_attributes = {}
            for k in FORWARDED_ATTRIBUTES:
                if k in entity:
                    forwarded_attributes[k] = entity[k]
            variables.update({"call": forwarded_attributes})

            if CONF_CONDITION in entity:
                cond_func = await _async_process_if(
                    self.hass, entity[ATTR_SERVICE], entity
                )
                if cond_func is not None and not cond_func(
                    variables
                ):  # Evaluate conditions
                    continue

            sending_payload = deepcopy(payload.copy())
            if (default_data := entity.get(ATTR_DATA)) is not None:
                add_defaults(sending_payload, default_data)
            service = entity[ATTR_SERVICE][(len(NOTIFY_DOMAIN) + 1) :]
            tasks.append(
                asyncio.create_task(
                    self.hass.services.async_call(
                        NOTIFY_DOMAIN, service, sending_payload
                    )
                )
            )

        if tasks:
            await asyncio.wait(tasks)
