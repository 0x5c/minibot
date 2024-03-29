# Changelog for Minibot

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres (somewhat) to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).


## [Unreleased]


## [1.5.1] - 2023-08-28
### Changed
- Updated Pycord to temporary Git URL to support new "pomelo" Discord usernames.
- Changed default python version in tooling to `3.11`.


## [1.5.0] - 2022-12-25
### Added
- Config option to automatically strip spaces after the prefix. Update your configs.
- First support for Pycord logging output.
### Changed
- Migrated to Pycord.
- Commands are now case-insensitive.


## [1.4.0] - 2021-01-18
### Added
- Ability to exclude bots from autorole (on by default).
- `mb?rolestats` command.
- Support for membership screening in autorole.
### Changed
- Bumped version of discord.py dependency to 1.6.0


## [1.3.2] - 2020-10-06
### Changed
- Bumped version of discord.py to 1.5.0


## [1.3.1] - 2020-07-30
### Fixed
- Version pinning of `discord.py`.


## [1.3.0] - 2020-02-25
### Added
- (selfroles) Ability to get/remove more than one role at a time.
- New `display_prefix` key to the config.
- More prefixes to the config template.
### Fixed
- Missing command description for `roleme`.


## [1.2.1] - 2020-02-19
### Fixed
- Fixed bug where `mb?info` would not work in DMs.


## [1.2.0] - 2020-02-17
### Added
- Selfrole system. Includes new elements in `options.py`.
- Official guild invite in 'info'.
- Activity message.


## [1.0.1] - 2019-12-23
### Changed
- Fix autorole msg being printed for each role.
- Fix default prefix being too generic.


## [1.0.0] - 2019-12-23
### Added
- Autorole system


[Unreleased]: https://github.com/0x5c/minibot/compare/v1.5.1...HEAD
[1.5.1]: https://github.com/0x5c/minibot/releases/tag/v1.5.1
[1.5.0]: https://github.com/0x5c/minibot/releases/tag/v1.5.0
[1.4.0]: https://github.com/0x5c/minibot/releases/tag/v1.4.0
[1.3.2]: https://github.com/0x5c/minibot/releases/tag/v1.3.2
[1.3.1]: https://github.com/0x5c/minibot/releases/tag/v1.3.1
[1.3.0]: https://github.com/0x5c/minibot/releases/tag/v1.3.0
[1.2.1]: https://github.com/0x5c/minibot/releases/tag/v1.2.1
[1.2.0]: https://github.com/0x5c/minibot/releases/tag/v1.2.0
[1.0.1]: https://github.com/0x5c/minibot/releases/tag/v1.0.1
[1.0.0]: https://github.com/0x5c/minibot/releases/tag/v1.0.0
