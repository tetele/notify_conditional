# Conditional notifications

[![GitHub Release][releases-shield]][releases]
[![GitHub Activity][commits-shield]][commits]
[![License][license-shield]](LICENSE)

[![hacs][hacsbadge]][hacs]
![Project Maintenance][maintenance-shield]
[![BuyMeCoffee][buymecoffeebadge]][buymecoffee]

[![Community Forum][forum-shield]][forum]

_A solution to send notifications conditionally using Home Assistant._

**This integration will set up the following platforms.**

Platform | Description
-- | --
`binary_sensor` | Show something `True` or `False`.
`sensor` | Show info from blueprint API.
`switch` | Switch something `True` or `False`.

## Installation

1. Using the tool of choice open the directory (folder) for your HA configuration (where you find `configuration.yaml`).
1. If you do not have a `custom_components` directory (folder) there, you need to create it.
1. In the `custom_components` directory (folder) create a new folder called `notify_conditional`.
1. Download _all_ the files from the `custom_components/notify_conditional/` directory (folder) in this repository.
1. Place the files you downloaded in the new directory (folder) you created.
1. Restart Home Assistant
1. In the HA UI go to "Configuration" -> "Integrations" click "+" and search for "Conditional notifications"

## Contributions are welcome!

If you want to contribute to this please read the [Contribution guidelines](CONTRIBUTING.md)

***

[buymecoffee]: https://www.buymeacoffee.com/t3t3l3
[buymecoffeebadge]: https://img.shields.io/badge/buy%20me%20a%20coffee-donate-yellow.svg?style=for-the-badge
[commits-shield]: https://img.shields.io/github/commit-activity/y/tetele/notify_conditional.svg?style=for-the-badge
[commits]: https://github.com/tetele/notify_conditional/commits/main
[hacs]: https://github.com/hacs/integration
[hacsbadge]: https://img.shields.io/badge/HACS-Custom-orange.svg?style=for-the-badge
[exampleimg]: example.png
[forum-shield]: https://img.shields.io/badge/community-forum-brightgreen.svg?style=for-the-badge
[forum]: https://community.home-assistant.io/
[license-shield]: https://img.shields.io/github/license/tetele/notify_conditional.svg?style=for-the-badge
[maintenance-shield]: https://img.shields.io/badge/maintainer-Tudor%20Sandu%20%40tetele-blue.svg?style=for-the-badge
[releases-shield]: https://img.shields.io/github/release/tetele/notify_conditional.svg?style=for-the-badge
[releases]: https://github.com/tetele/notify_conditional/releases
