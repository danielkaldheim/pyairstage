## [2.4.1](https://github.com/danielkaldheim/pyairstage/compare/v2.4.0...v2.4.1) (2025-10-16)


### Bug Fixes

* **release:** Attempting to kick semantic-release ([d5338da](https://github.com/danielkaldheim/pyairstage/commit/d5338da260e93ee5b082e789a8766200e4729e39))

# [2.4.0](https://github.com/danielkaldheim/pyairstage/compare/v2.3.0...v2.4.0) (2025-10-16)


### Features

* **hmn detection:** added getter/setter for hmn_detection_auto_save ([4a7947f](https://github.com/danielkaldheim/pyairstage/commit/4a7947f9056c29b41f141dd6dfb52b007ecc77a5))
* **vertical swing:** add support for 8-position vertical swing ([#11](https://github.com/danielkaldheim/pyairstage/issues/11)) ([542b968](https://github.com/danielkaldheim/pyairstage/commit/542b96893940a5eba4f6eb31745c2b9bfa3fe27a))

# [2.4.0](https://github.com/danielkaldheim/pyairstage/compare/v2.3.0...v2.4.0) (2025-10-16)


### Features

* **hmn detection:** added getter/setter for hmn_detection_auto_save ([4a7947f](https://github.com/danielkaldheim/pyairstage/commit/4a7947f9056c29b41f141dd6dfb52b007ecc77a5))
* **vertical swing:** add support for 8-position vertical swing ([#11](https://github.com/danielkaldheim/pyairstage/issues/11)) ([542b968](https://github.com/danielkaldheim/pyairstage/commit/542b96893940a5eba4f6eb31745c2b9bfa3fe27a))

# [2.4.0](https://github.com/danielkaldheim/pyairstage/compare/v2.3.0...v2.4.0) (2025-10-16)


### Features

* **hmn detection:** added getter/setter for hmn_detection_auto_save ([4a7947f](https://github.com/danielkaldheim/pyairstage/commit/4a7947f9056c29b41f141dd6dfb52b007ecc77a5))
* **vertical swing:** add support for 8-position vertical swing ([#11](https://github.com/danielkaldheim/pyairstage/issues/11)) ([542b968](https://github.com/danielkaldheim/pyairstage/commit/542b96893940a5eba4f6eb31745c2b9bfa3fe27a))

# [2.4.0](https://github.com/danielkaldheim/pyairstage/compare/v2.3.0...v2.4.0) (2025-10-16)


### Features

* **hmn detection:** added getter/setter for hmn_detection_auto_save ([4a7947f](https://github.com/danielkaldheim/pyairstage/commit/4a7947f9056c29b41f141dd6dfb52b007ecc77a5))
* **vertical swing:** add support for 8-position vertical swing ([#11](https://github.com/danielkaldheim/pyairstage/issues/11)) ([542b968](https://github.com/danielkaldheim/pyairstage/commit/542b96893940a5eba4f6eb31745c2b9bfa3fe27a))

# [2.3.0](https://github.com/danielkaldheim/pyairstage/compare/v2.2.0...v2.3.0) (2025-08-08)


### Features

* **fan speed:** adding cases for fans with medium-low and medium-high ([d89abe4](https://github.com/danielkaldheim/pyairstage/commit/d89abe48042ef7075b2c0b181da0883578eeb7a6))

# [2.2.0](https://github.com/danielkaldheim/pyairstage/compare/v2.1.0...v2.2.0) (2025-07-28)


### Features

* **power:** start pulling power consumption value ([8b7295a](https://github.com/danielkaldheim/pyairstage/commit/8b7295a78b21c89f4abee8a7ee0fd7b5aa0e10c0))

# [2.1.0](https://github.com/danielkaldheim/pyairstage/compare/v2.0.1...v2.1.0) (2025-05-04)


### Features

* **temperature:** Adding in getters for minimum & maximum temperature ([2f9a4da](https://github.com/danielkaldheim/pyairstage/commit/2f9a4dadd497351d2ed193a5acdbc6cf817dec6c))

## [2.0.1](https://github.com/danielkaldheim/pyairstage/compare/v2.0.0...v2.0.1) (2025-04-13)


### Bug Fixes

* **dependencies:** paring down requirements to direct needs, removing transitive dependencies as requirements ([baca54d](https://github.com/danielkaldheim/pyairstage/commit/baca54d76dffebaa9e848c83e54b331abc76db38))

# [2.0.0](https://github.com/danielkaldheim/pyairstage/compare/v1.1.3...v2.0.0) (2025-04-13)


* feat(swing) Reworking vertical swing for 4 or 6 position devices via enum reworking ([35d9a7b](https://github.com/danielkaldheim/pyairstage/commit/35d9a7b35c594ecc3723bdbd21116a743639cca9))


### BREAKING CHANGES

* get_vertical_direction and set_vertical_direction have had signature changes; VerticalSwingPosition, VerticalPositionDescriptors, and VALUE_TO_VERTICAL_POSITION have been replaced with VerticalSwingPositions, VerticalSwing4PositionsValues, and VerticalSwing6PositionsValues.

## [1.1.3](https://github.com/danielkaldheim/pyairstage/compare/v1.1.2...v1.1.3) (2024-03-20)


### Bug Fixes

* set temp correctly when F instead of C ([862cf11](https://github.com/danielkaldheim/pyairstage/commit/862cf11d767f26f7a4be22f452eac0deb5552c9b))

## [1.1.2](https://github.com/danielkaldheim/pyairstage/compare/v1.1.1...v1.1.2) (2024-03-20)


### Bug Fixes

* **lint:** fixes lint errors ([3e6416e](https://github.com/danielkaldheim/pyairstage/commit/3e6416eec5ac111642fb294a520298827e76e22a))

## [1.1.1](https://github.com/danielkaldheim/pyairstage/compare/v1.1.0...v1.1.1) (2023-10-17)


### Bug Fixes

* **target temperature:** get last good value if value returns error ([abf2cb1](https://github.com/danielkaldheim/pyairstage/commit/abf2cb1994ecee56bc12f0fac125acc5c7795288))

# [1.1.0](https://github.com/danielkaldheim/pyairstage/compare/v1.0.4...v1.1.0) (2023-08-18)


### Features

* **human detection:** added parameter for human detection(?) ([5f30667](https://github.com/danielkaldheim/pyairstage/commit/5f30667736e885e702ca07a82fc8d6afd227a4f1))

## [1.0.4](https://github.com/danielkaldheim/pyairstage/compare/v1.0.3...v1.0.4) (2023-08-16)


### Bug Fixes

* **led:** added missing led option ([0837d3b](https://github.com/danielkaldheim/pyairstage/commit/0837d3bcefe441fa8f6f4ccddd9097a456974ddb))

## [1.0.3](https://github.com/danielkaldheim/pyairstage/compare/v1.0.2...v1.0.3) (2023-08-15)


### Bug Fixes

* **parameters:** check if parameter is available ([614bbd7](https://github.com/danielkaldheim/pyairstage/commit/614bbd7e723759af15b250005b0540630f7b9b19))

## [1.0.2](https://github.com/danielkaldheim/pyairstage/compare/v1.0.1...v1.0.2) (2023-08-08)


### Bug Fixes

* **switches:** added support for controling switches ([5ba824b](https://github.com/danielkaldheim/pyairstage/commit/5ba824bb00f9a5baae4eabfa89a0cc34b8ff3b8c))

## [1.0.1](https://github.com/danielkaldheim/pyairstage/compare/v1.0.0...v1.0.1) (2023-08-08)


### Bug Fixes

* **ci:** bump version ([1609ab8](https://github.com/danielkaldheim/pyairstage/commit/1609ab82d750528611fe84c078fbd9de091b601b))

# 1.0.0 (2023-08-08)


### Bug Fixes

* **ci:** bump version ([103bd58](https://github.com/danielkaldheim/pyairstage/commit/103bd58f162982875e65cfa47f0c2619ac0d3db2))
* **ci:** bump version ([e9ef50a](https://github.com/danielkaldheim/pyairstage/commit/e9ef50acc26e71a99263523be3d860c1e9ce75ff))
* **ci:** bump version ([dd07a5d](https://github.com/danielkaldheim/pyairstage/commit/dd07a5dbc4af8cc63962a722aad35255afdb8653))


### Features

* **local:** refactor for support local connection ([0cddc13](https://github.com/danielkaldheim/pyairstage/commit/0cddc136adab65575693362ba88752c7614f0279))

# 1.0.0 (2023-08-08)


### Bug Fixes

* **ci:** bump version ([103bd58](https://github.com/danielkaldheim/pyairstage/commit/103bd58f162982875e65cfa47f0c2619ac0d3db2))
* **ci:** bump version ([e9ef50a](https://github.com/danielkaldheim/pyairstage/commit/e9ef50acc26e71a99263523be3d860c1e9ce75ff))
* **ci:** bump version ([dd07a5d](https://github.com/danielkaldheim/pyairstage/commit/dd07a5dbc4af8cc63962a722aad35255afdb8653))


### Features

* **local:** refactor for support local connection ([0cddc13](https://github.com/danielkaldheim/pyairstage/commit/0cddc136adab65575693362ba88752c7614f0279))

# 1.0.0 (2023-08-08)


### Bug Fixes

* **ci:** bump version ([e9ef50a](https://github.com/danielkaldheim/pyairstage/commit/e9ef50acc26e71a99263523be3d860c1e9ce75ff))
* **ci:** bump version ([dd07a5d](https://github.com/danielkaldheim/pyairstage/commit/dd07a5dbc4af8cc63962a722aad35255afdb8653))


### Features

* **local:** refactor for support local connection ([0cddc13](https://github.com/danielkaldheim/pyairstage/commit/0cddc136adab65575693362ba88752c7614f0279))

# 1.0.0 (2023-08-08)


### Bug Fixes

* **ci:** bump version ([dd07a5d](https://github.com/danielkaldheim/pyairstage/commit/dd07a5dbc4af8cc63962a722aad35255afdb8653))


### Features

* **local:** refactor for support local connection ([0cddc13](https://github.com/danielkaldheim/pyairstage/commit/0cddc136adab65575693362ba88752c7614f0279))

# 1.0.0 (2023-08-08)


### Features

* **local:** refactor for support local connection ([0cddc13](https://github.com/danielkaldheim/pyairstage/commit/0cddc136adab65575693362ba88752c7614f0279))
