# Conditional notifications

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Community Forum][forum-shield]][forum]

_A solution to send notifications conditionally using Home Assistant._

Imagine you want to be notified of certain events, but you'd like Google Home to speak to you when you're at home during the day, you want phone notifications when you're away and you want to silence notifications completely at night.

You could embed that in automations, but if you want the same notification pattern it gets hard to maintain. You could write a script, but that may also become hard to maintain at some point.

With this integration, you simply configure a `notify` service that calls other `notify` services based on conditions. Here's an example:

```
notify:
  - name: me_based_on_context
    platform: notify_conditional
    services:
      - service: notify.google_home
        condition:
          - condition: state
            entity_id: person.me
            state: home
          - condition: time
            after: "08:00:00"
            before: "22:00:00"
        message: "{{ call.message }}"
      - service: notify.my_phone
        condition:
          - condition: state
            entity_id: person.me
            state: not_home
        message: >
          {{ call.message }}
        data:
          url: >
            {{ call.data.url }}
```

Then you would simply call the `notify.me_based_on_context` service in your automations. Much simpler!

## Installation

### Manual installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `notify_conditional`.
1. Download _all_ the files from the `custom_components/notify_conditional/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant

## Usage

First you need to define a new service in `configuration.yaml`

```
notify:
  - name: service_name   # Use whatever you want
    platform: notify_conditional   # platform name must be notify_conditional
    services:   # the list of services to forward the call to
      - service: notify.existing_service_1
        condition:   # list of conditions that need to be true to forward the service call (same syntax as automations - https://www.home-assistant.io/docs/scripts/conditions/)
          - condition: state
            entity_id: person.me
            state: home
          - condition: time
            after: "08:00:00"
            before: "22:00:00"
        message: "Hello there!"   # the message
        title: "Example title"
        data:
          foo: bar   # this depends on the service that receives the call
      - service: notify.existing_service_2
        condition:
          - condition: template
            value_template: "{{ is_state('some.entity', '2') }}"
        message: >   # you can also use the `call` variable to get data from the initial service call
          {{ call.message }}
```

### Reference

Config var | Type | Description
-- | -- | --
`name` | slug | The name of the notify service.
`platform` | `notify_conditional` | This is a fixed value that references the conditional notification platform
`services` | list | A list of `notify` services, referenced by full name, that will be called. See details below

For each service, the configuration variables are:

Config var | Type | Description
-- | -- | --
`service` | service ID | The name of the notify service to call if the conditions are met (e.g. `notify.persistent_notification`).
`condition` | list | A list of [conditions][conditions-docs] that **ALL** need to be true in order for the service to get called. Use an [OR condition][condition-or-docs] if you want a different behavior.
`message` | template | The message that will be forwarded to the notify service. It can be a template and you can use `{{ call.message }}` to get the value that your `notify_conditional` service was called with.
`title` | template | The title that will be forwarded to the notify service. It can be a template and you can use `{{ call.title }}` to get the value that your `notify_conditional` service was called with.
`target` | list | The list of target entities, in case you want to forward to `notify.notify`.
`data` | object | The additional data that will be forwarded to the notify service. For each value, you can use `{{ call.data.some_var }}` to get the value that your `notify_conditional` service was called with.



## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[buymecoffee]: https://www.buymeacoffee.com/t3t3l3
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/tetele/notify_conditional.svg?style=for-the-badge
[commits]: https://github.com/tetele/notify_conditional/commits/main
[conditions-docs]: https://www.home-assistant.io/docs/scripts/conditions/
[condition-or-docs]: https://www.home-assistant.io/docs/scripts/conditions/#or-condition
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[exampleimg]: example.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/tetele/notify_conditional.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Tudor%20Sandu%20%40tetele-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/tetele/notify_conditional.svg?style=for-the-badge
[releases]: https://github.com/tetele/notify_conditional/releases
