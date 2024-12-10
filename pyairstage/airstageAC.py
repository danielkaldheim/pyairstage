from .constants import *

from .airstageApi import AirstageApi, ApiCloud, ApiLocal
from typing import Any


class AirstageACError(Exception):
    """Airstage AC Error"""


class AirstageAC:
    """Class to represent an Airstage Air Conditioner."""

    def __init__(self, dsn: str, api: AirstageApi | ApiCloud | ApiLocal) -> None:
        if not api:
            raise AirstageACError("Missing api")

        if not dsn or not isinstance(dsn, str):
            raise ValueError("dsn must be a non-empty string")

        self._dsn = dsn
        self._api = api
        self._cache = {}
        self._lastGoodValue = {}

    def refresh_parameters(self, data: dict | None = None):
        if not data:
            devices = self._api.get_devices()
            if not isinstance(self._dsn, devices):
                raise AirstageACError(f"dsn not found {self._dsn}")
            data = devices[self._dsn]

        self._cache = data

        for parameter in data["parameters"]:
            try:
                name = parameter["name"]
                value = parameter["value"]
                parameter_name = ACParameter(name)

                self._cache[parameter_name] = value
                if value != CAPABILITY_NOT_AVAILABLE:
                    self._lastGoodValue[parameter_name] = value
            except ValueError as e:
                print(f"Error processing parameter: {e}")
                pass
        return self

    def get_cache(self):
        """Returns the current cache of device parameters."""
        return self._cache

    def _get_cached_device_parameter(self, parameterName: ACParameter) -> Any:
        if not isinstance(parameterName, ACParameter):
            raise AirstageACError(f"Invalid parameter name: {parameterName}")

        if parameterName in self._cache:
            value = self._cache[parameterName]
            if (
                value == CAPABILITY_NOT_AVAILABLE
                and parameterName in self._lastGoodValue
            ):
                return self._lastGoodValue[parameterName]

            return value

    def _is_capability_available(self, parameter: ACParameter) -> bool:
        value = self._get_cached_device_parameter(parameter)
        return value != CAPABILITY_NOT_AVAILABLE

    async def _set_device_parameter(self, parameterName: ACParameter, value):
        if not isinstance(parameterName, ACParameter):
            raise AirstageACError(f"Invalid property name: {parameterName}")

        updatedValue = await self._api.set_parameter(self._dsn, parameterName, value)
        if updatedValue is not None:
            self._cache[parameterName] = value
            return value

    def get_device_parameter(self, parameterName: ACParameter) -> Any:
        value = self._lastGoodValue[parameterName]
        if (
            parameterName is ACParameter.INDOOR_TEMPERATURE
            or parameterName is ACParameter.OUTDOOR_TEMPERATURE
        ):
            value = (int(value) - 5000) / 100
        return value

    def get_device_name(self) -> str:
        return str(self._get_cached_device_parameter(ACParameter.DEVICE_NAME))

    def get_device_on_off_state(self):
        return VALUE_TO_BOOLEAN[
            int(self._get_cached_device_parameter(ACParameter.ONOFF_MODE))
        ]

    async def turn_on(self):
        await self._set_device_parameter(ACParameter.ONOFF_MODE, BooleanProperty.ON)

    async def turn_off(self):
        await self._set_device_parameter(ACParameter.ONOFF_MODE, BooleanProperty.OFF)

    def get_operating_mode(self):
        if int(self._get_cached_device_parameter(ACParameter.ONOFF_MODE)) == 0:
            return OperationModeDescriptors.OFF
        return VALUE_TO_OPERATION_MODE[
            int(self._get_cached_device_parameter(ACParameter.OPERATION_MODE))
        ]

    async def set_operation_mode(self, mode: OperationMode):
        if not isinstance(mode, OperationMode):
            raise AirstageACError(f"Invalid operationMode value: {mode}")
        await self._set_device_parameter(ACParameter.OPERATION_MODE, mode)

    def get_fan_speed(self):
        return VALUE_TO_FAN_SPEED[
            int(self._get_cached_device_parameter(ACParameter.FAN_SPEED))
        ]

    async def set_fan_speed(self, fan_speed: FanSpeed):
        if not isinstance(fan_speed, FanSpeed):
            raise AirstageACError(f"Invalid fan speed value: {fan_speed}")
        await self._set_device_parameter(ACParameter.FAN_SPEED, fan_speed)

    def get_display_temperature(self) -> float | None:
        if self._is_capability_available(ACParameter.INDOOR_TEMPERATURE) == False:
            return None
        return self.get_device_parameter(ACParameter.INDOOR_TEMPERATURE)

    def get_outdoor_temperature(self) -> float | None:
        if self._is_capability_available(ACParameter.OUTDOOR_TEMPERATURE) == False:
            return None
        return self.get_device_parameter(ACParameter.OUTDOOR_TEMPERATURE)

    def get_target_temperature(self) -> float | None:
        if self._is_capability_available(ACParameter.TARGET_TEMPERATURE) == False:
            return None
        return (
            int(self._get_cached_device_parameter(ACParameter.TARGET_TEMPERATURE)) / 10
        )

    async def set_target_temperature(self, target_temperature: float):
        match self.get_operating_mode():
            case OperationModeDescriptors.AUTO:
                min_temp = ACConstants.AUTO_MIN_TEMP
                max_temp = ACConstants.AUTO_MAX_TEMP
            case OperationModeDescriptors.COOL:
                min_temp = ACConstants.COOL_MIN_TEMP
                max_temp = ACConstants.COOL_MAX_TEMP
            case OperationModeDescriptors.DRY:
                min_temp = ACConstants.DRY_MIN_TEMP
                max_temp = ACConstants.DRY_MAX_TEMP
            case OperationModeDescriptors.FAN:
                raise AirstageACError(
                    f"Invalid targetTemperature: {target_temperature}. targetTemperature cannot be set in FAN mode"
                )
            case OperationModeDescriptors.HEAT:
                min_temp = ACConstants.HEAT_MIN_TEMP
                max_temp = ACConstants.HEAT_MAX_TEMP

        if target_temperature < min_temp or target_temperature > max_temp:
            raise AirstageACError(
                f"Invalid targetTemperature: {target_temperature}. Value must be {min_temp} <= target <= {max_temp}"
            )

        rounded_temp = round(target_temperature * 2) / 2
        actual_target = int(rounded_temp * 10)
        await self._set_device_parameter(ACParameter.TARGET_TEMPERATURE, actual_target)

    def get_vertical_direction(self) -> VerticalSwingPositions | None:
        if self._is_capability_available(ACParameter.VERTICAL_DIRECTION):
            value = self._get_cached_device_parameter(ACParameter.VERTICAL_DIRECTION)
            total_positions = self.get_num_vertical_swing_positions()
            if total_positions == 6:
                return VerticalSwingPositions[
                    VerticalSwing6PositionsValues(int(value)).name
                ]
            else:
                return VerticalSwingPositions[
                    VerticalSwing4PositionsValues(int(value)).name
                ]
        return None

    async def set_vertical_direction(self, direction: VerticalSwingPositions):
        if not isinstance(direction, VerticalSwingPositions):
            raise AirstageACError(
                f"Invalid fan direction value: {type(direction)}: {direction}"
            )
        total_positions = self.get_num_vertical_swing_positions()
        if total_positions == 6:
            direction_value = VerticalSwing6PositionsValues[direction.name]
        else:
            direction_value = VerticalSwing4PositionsValues[direction.name]

        await self._set_device_parameter(
            ACParameter.VERTICAL_DIRECTION, direction_value
        )

    def get_num_vertical_swing_positions(self) -> int:
        """We have observed this being 4 or 6"""
        return int(
            self._get_cached_device_parameter(ACParameter.VERTICAL_SWING_POSITIONS)
        )

    def get_vertical_swing(self) -> BooleanDescriptors | None:
        if self._is_capability_available(ACParameter.VERTICAL_SWING):
            value = self._get_cached_device_parameter(ACParameter.VERTICAL_SWING)
            return VALUE_TO_BOOLEAN[int(value)]
        return None

    async def set_vertical_swing(self, mode: BooleanProperty):
        if not isinstance(mode, BooleanProperty):
            raise AirstageACError(f"Invalid mode value: {mode}")
        await self._set_device_parameter(ACParameter.VERTICAL_SWING, mode)

    def get_economy_mode(self) -> BooleanDescriptors | None:
        if self._is_capability_available(ACParameter.ECONOMY_MODE):
            value = self._get_cached_device_parameter(ACParameter.ECONOMY_MODE)
            return VALUE_TO_BOOLEAN[int(value)]
        return None

    async def set_economy_mode(self, mode: BooleanProperty):
        if not isinstance(mode, BooleanProperty):
            raise AirstageACError(f"Invalid mode value: {mode}")
        await self._set_device_parameter(ACParameter.ECONOMY_MODE, mode)

    def get_energy_save_fan(self):
        return VALUE_TO_BOOLEAN[
            int(self._get_cached_device_parameter(ACParameter.ENERGY_SAVE_FAN))
        ]

    async def set_energy_save_fan(self, mode: BooleanProperty):
        if not isinstance(mode, BooleanProperty):
            raise AirstageACError(f"Invalid mode value: {mode}")
        await self._set_device_parameter(ACParameter.ENERGY_SAVE_FAN, mode)

    def get_powerful_mode(self) -> BooleanDescriptors | None:
        if self._is_capability_available(ACParameter.POWERFUL_MODE):
            value = self._get_cached_device_parameter(ACParameter.POWERFUL_MODE)
            return VALUE_TO_BOOLEAN[int(value)]
        return None

    async def set_powerful_mode(self, mode: BooleanProperty):
        if not isinstance(mode, BooleanProperty):
            raise AirstageACError(f"Invalid mode value: {mode}")
        await self._set_device_parameter(ACParameter.POWERFUL_MODE, mode)

    def get_outdoor_low_noise(self) -> BooleanDescriptors | None:
        if self._is_capability_available(ACParameter.OUTDOOR_LOW_NOISE):
            value = self._get_cached_device_parameter(ACParameter.OUTDOOR_LOW_NOISE)
            return VALUE_TO_BOOLEAN[int(value)]
        return None

    async def set_outdoor_low_noise(self, mode: BooleanProperty):
        if not isinstance(mode, BooleanProperty):
            raise AirstageACError(f"Invalid mode value: {mode}")
        await self._set_device_parameter(ACParameter.OUTDOOR_LOW_NOISE, mode)

    def get_indoor_led(self) -> BooleanDescriptors | None:
        if self._is_capability_available(ACParameter.INDOOR_LED):
            value = self._get_cached_device_parameter(ACParameter.INDOOR_LED)
            return VALUE_TO_BOOLEAN[int(value)]
        return None

    async def set_indoor_led(self, mode: BooleanProperty):
        if not isinstance(mode, BooleanProperty):
            raise AirstageACError(f"Invalid mode value: {mode}")
        await self._set_device_parameter(ACParameter.INDOOR_LED, mode)

    def get_minimum_heat(self) -> BooleanDescriptors | None:
        if self._is_capability_available(ACParameter.MINIMUM_HEAT):
            value = self._get_cached_device_parameter(ACParameter.MINIMUM_HEAT)
            return VALUE_TO_BOOLEAN[int(value)]
        return None

    async def set_minimum_heat(self, mode: BooleanProperty):
        if not isinstance(mode, BooleanProperty):
            raise AirstageACError(f"Invalid mode value: {mode}")
        await self._set_device_parameter(ACParameter.MINIMUM_HEAT, mode)

    def get_hmn_detection(self) -> BooleanDescriptors | None:
        if self._is_capability_available(ACParameter.HMN_DETECTION):
            value = self._get_cached_device_parameter(ACParameter.HMN_DETECTION)
            return VALUE_TO_BOOLEAN[int(value)]
        return None
