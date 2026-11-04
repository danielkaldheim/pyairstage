import logging

from .airstageApi import AirstageApi, ApiCloud, ApiLocal
from .constants import *

DATA_TYPES = int | float | str | bool

_LOGGER = logging.getLogger(__name__)


class AirstageACError(Exception):
    """Airstage AC Error"""


class AirstageAC:
    """Class to represent an Airstage Air Conditioner."""

    def __init__(self, dsn: str, api: AirstageApi | ApiCloud | ApiLocal):
        if not api:
            raise AirstageACError("Missing api")

        if not dsn or not isinstance(dsn, str):
            raise ValueError("dsn must be a non-empty string")

        self._dsn = dsn
        self._api = api
        self._cache = {}
        self._lastGoodValue = {}

    def refresh_parameters(
        self, data: dict[str, DATA_TYPES] | None = None
    ) -> AirstageAC:
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
                _LOGGER.debug("Error processing parameter: %s", e)
        return self

    def get_cache(self) -> dict[str, DATA_TYPES]:
        """Returns the current cache of device parameters."""
        return self._cache

    def _get_cached_device_parameter(
        self, parameterName: ACParameter
    ) -> DATA_TYPES | None:
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

    async def _set_device_parameter(
        self, parameterName: ACParameter, value: DATA_TYPES
    ) -> DATA_TYPES | None:
        if not isinstance(parameterName, ACParameter):
            raise AirstageACError(f"Invalid property name: {parameterName}")

        updatedValue = await self._api.set_parameter(self._dsn, parameterName, value)
        if updatedValue is not None:
            self._cache[parameterName] = value
            return value

    def get_device_parameter(self, parameterName: ACParameter) -> DATA_TYPES | None:
        value = self._lastGoodValue[parameterName]
        if (
            parameterName is ACParameter.INDOOR_TEMPERATURE
            or parameterName is ACParameter.OUTDOOR_TEMPERATURE
        ):
            value = (int(value) - 5000) / 100 if value is not None else None
        return value

    def get_device_name(self) -> str | None:
        return self._get_cached_device_parameter(ACParameter.DEVICE_NAME)

    def get_device_on_off_state(self) -> bool | None:
        raw = self._get_cached_device_parameter(ACParameter.ONOFF_MODE)
        return VALUE_TO_BOOLEAN.get(int(raw))

    async def _set_boolean(self, param: ACParameter, value: bool):
        await self.set_device_parameter(
            param, BooleanProperty.ON if value else BooleanProperty.OFF
        )

    def _get_boolean(self, param: ACParameter) -> bool | None:
        if self._is_capability_available(param):
            value = self._get_cached_device_parameter(param)
            return bool(value) if value is not None else None
        return None

    async def turn_on(self):
        await self._set_boolean(ACParameter.ONOFF_MODE, True)

    async def turn_off(self):
        await self._set_boolean(ACParameter.ONOFF_MODE, False)

    def get_operating_mode(self) -> OperationModeDescriptors | None:
        if int(self._get_cached_device_parameter(ACParameter.ONOFF_MODE)) == 0:
            return OperationModeDescriptors.OFF
        return VALUE_TO_OPERATION_MODE.get(
            int(self._get_cached_device_parameter(ACParameter.OPERATION_MODE))
        )

    async def set_operation_mode(self, mode: OperationMode):
        if not isinstance(mode, OperationMode):
            raise AirstageACError(f"Invalid operationMode value: {mode}")
        await self._set_device_parameter(ACParameter.OPERATION_MODE, mode)

    def get_fan_speed(self) -> FanSpeedDescriptors | None:
        return VALUE_TO_FAN_SPEED.get(
            int(self._get_cached_device_parameter(ACParameter.FAN_SPEED))
        )

    async def set_fan_speed(self, fan_speed: FanSpeed):
        if not isinstance(fan_speed, FanSpeed):
            raise AirstageACError(f"Invalid fan speed value: {fan_speed}")
        await self._set_device_parameter(ACParameter.FAN_SPEED, fan_speed)

    def get_display_temperature(self) -> float | None:
        if self._is_capability_available(ACParameter.INDOOR_TEMPERATURE):
            return self.get_device_parameter(ACParameter.INDOOR_TEMPERATURE)
        return None

    def get_outdoor_temperature(self) -> float | None:
        if self._is_capability_available(ACParameter.OUTDOOR_TEMPERATURE):
            return self.get_device_parameter(ACParameter.OUTDOOR_TEMPERATURE)
        return None

    def get_target_temperature(self) -> float | None:
        if self._is_capability_available(ACParameter.TARGET_TEMPERATURE):
            return (
                int(self._get_cached_device_parameter(ACParameter.TARGET_TEMPERATURE))
                / 10
            )
        return None

    def get_minimum_temperature(self) -> float | None:
        match self.get_operating_mode():
            case OperationModeDescriptors.AUTO:
                return ACConstants.AUTO_MIN_TEMP
            case OperationModeDescriptors.COOL:
                return ACConstants.COOL_MIN_TEMP
            case OperationModeDescriptors.DRY:
                return ACConstants.DRY_MIN_TEMP
            case OperationModeDescriptors.HEAT:
                return ACConstants.HEAT_MIN_TEMP
            case OperationModeDescriptors.FAN:
                return None

    def get_maximum_temperature(self) -> float | None:
        match self.get_operating_mode():
            case OperationModeDescriptors.AUTO:
                return ACConstants.AUTO_MAX_TEMP
            case OperationModeDescriptors.COOL:
                return ACConstants.COOL_MAX_TEMP
            case OperationModeDescriptors.DRY:
                return ACConstants.DRY_MAX_TEMP
            case OperationModeDescriptors.HEAT:
                return ACConstants.HEAT_MAX_TEMP
            case OperationModeDescriptors.FAN:
                return None

    async def set_target_temperature(self, target_temperature: float):
        # TODO: excise validation logic, get_minimum_temperature/get_maximum_temperature can be used to pre-validate
        min_temp = self.get_minimum_temperature()
        max_temp = self.get_maximum_temperature()
        if min_temp is None or max_temp is None:
            raise AirstageACError(
                f"Invalid targetTemperature: {target_temperature}. targetTemperature cannot be set in FAN mode"
            )

        if target_temperature < min_temp or target_temperature > max_temp:
            raise AirstageACError(
                f"Invalid targetTemperature: {target_temperature}. Value must be {min_temp} <= target <= {max_temp}"
            )

        rounded_temp = round(target_temperature * 2) / 2
        actual_target = int(rounded_temp * 10)
        await self._set_device_parameter(ACParameter.TARGET_TEMPERATURE, actual_target)

    def get_vertical_direction(self) -> VerticalSwingPositions | None:
        if self._is_capability_available(
            ACParameter.VERTICAL_DIRECTION
        ) and self._is_capability_available(ACParameter.VERTICAL_SWING_POSITIONS):
            value = self._get_cached_device_parameter(ACParameter.VERTICAL_DIRECTION)
            total_positions = self.get_num_vertical_swing_positions()
            if total_positions == 8:
                return VerticalSwingPositions.get(
                    VerticalSwing8PositionsValues(int(value)).name
                )
            elif total_positions == 6:
                return VerticalSwingPositions.get(
                    VerticalSwing6PositionsValues(int(value)).name
                )
            elif total_positions == 4:
                return VerticalSwingPositions.get(
                    VerticalSwing4PositionsValues(int(value)).name
                )
            else:
                raise AirstageACError(
                    f"Invalid total_positions value: {total_positions}. Only 4, 6 and 8 are supported"
                )
        return None

    async def set_vertical_direction(self, direction: VerticalSwingPositions):
        if not isinstance(direction, VerticalSwingPositions):
            raise AirstageACError(
                f"Invalid fan direction value: {type(direction)}: {direction}"
            )
        total_positions = self.get_num_vertical_swing_positions()
        if total_positions == 8:
            direction_value = VerticalSwing8PositionsValues[direction.name]
        elif total_positions == 6:
            direction_value = VerticalSwing6PositionsValues[direction.name]
        elif total_positions == 4:
            direction_value = VerticalSwing4PositionsValues[direction.name]
        else:
            raise AirstageACError(
                f"Invalid total_positions value: {total_positions}. Only 4, 6 and 8 are supported"
            )

        await self._set_device_parameter(
            ACParameter.VERTICAL_DIRECTION, direction_value
        )

    def get_num_vertical_swing_positions(self) -> int:
        """We have observed this being 4 or 6"""
        return int(
            self._get_cached_device_parameter(ACParameter.VERTICAL_SWING_POSITIONS)
        )

    def get_vertical_swing(self) -> bool | None:
        return self._get_boolean(ACParameter.VERTICAL_SWING)

    async def set_vertical_swing(self, value: bool):
        await self._set_boolean(ACParameter.VERTICAL_SWING, value)

    def get_horizontal_swing(self) -> bool | None:
        return self._get_boolean(ACParameter.HORIZONTAL_SWING)

    async def set_horizontal_swing(self, value: bool):
        await self._set_boolean(ACParameter.HORIZONTAL_SWING, value)

    def get_economy_mode(self) -> bool | None:
        return self._get_boolean(ACParameter.ECONOMY_MODE)

    async def set_economy_mode(self, value: bool):
        await self._set_boolean(ACParameter.ECONOMY_MODE, value)

    def get_energy_save_fan(self) -> bool | None:
        return self._get_boolean(ACParameter.ENERGY_SAVE_FAN)

    async def set_energy_save_fan(self, value: bool):
        await self._set_boolean(ACParameter.ENERGY_SAVE_FAN, value)

    def get_powerful_mode(self) -> bool | None:
        return self._get_boolean(ACParameter.POWERFUL_MODE)

    async def set_powerful_mode(self, value: bool):
        await self._set_boolean(ACParameter.POWERFUL_MODE, value)

    def get_outdoor_low_noise(self) -> bool | None:
        return self._get_boolean(ACParameter.OUTDOOR_LOW_NOISE)

    async def set_outdoor_low_noise(self, value: bool):
        await self._set_boolean(ACParameter.OUTDOOR_LOW_NOISE, value)

    def get_indoor_led(self) -> bool | None:
        return self._get_boolean(ACParameter.INDOOR_LED)

    async def set_indoor_led(self, value: bool):
        await self._set_boolean(ACParameter.INDOOR_LED, value)

    def get_minimum_heat(self) -> bool | None:
        return self._get_boolean(ACParameter.MINIMUM_HEAT)

    async def set_minimum_heat(self, value: bool):
        await self._set_boolean(ACParameter.MINIMUM_HEAT, value)

    def get_hmn_detection(self) -> bool | None:
        return self._get_boolean(ACParameter.HMN_DETECTION)

    def get_hmn_detection_auto_save(self) -> bool | None:
        return self._get_boolean(ACParameter.HMN_DETECTION_AUTO_SAVE)

    async def set_hmn_detection_auto_save(self, value: bool):
        await self._set_boolean(ACParameter.HMN_DETECTION_AUTO_SAVE, value)
