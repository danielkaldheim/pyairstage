from .constants import *

from .airstageApi import AirstageApi, ApiCloud, ApiLocal


class AirstageACError(Exception):
    """Airstage AC Error"""


class AirstageAC:
    def __init__(self, dsn: str, api: AirstageApi | ApiCloud | ApiLocal) -> None:
        if not api:
            raise AirstageACError("Missing api")

        if not dsn or not isinstance(dsn, str):
            raise ValueError("dsn must be a non-empty string")

        self._dsn = dsn
        self._api = api
        self._cache = {}
        self._min_temp = 18.0
        self._max_temp = 30.0

    def refresh_parameters(self, data: dict | None = None):
        if not data:
            devices = self._api.get_devices()
            if not isinstance(self.dsn, devices):
                raise AirstageACError(f"dsn not found {self.dsn}")
            data = devices[self.dsn]

        self._cache = data

        for parameter in data["parameters"]:
            try:
                name = parameter["name"]
                value = parameter["value"]
                parameter_name = ACParameter(name)

                self._cache[parameter_name] = value
            except ValueError:
                pass
        return self

    def getCache(self):
        return self._cache

    def _get_cached_device_parameter(self, parameterName: ACParameter) -> any:
        if not isinstance(parameterName, ACParameter):
            raise AirstageACError(f"Invalid parameter name: {parameterName}")

        if parameterName in self._cache:
            return self._cache[parameterName]

    def have_device_parameter_capability(self, parameterName: ACParameter) -> bool:
        return (
            self._get_cached_device_parameter(parameterName) != CAPABILITY_NOT_AVAILABLE
        )

    def get_device_parameter(self, parameterName: ACParameter) -> any:
        value = self._cache[parameterName]
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
        return (
            int(self._get_cached_device_parameter(ACParameter.INDOOR_TEMPERATURE))
            - 5000
        ) / 100

    def get_outdoor_temperature(self) -> float | None:
        return (
            int(self._get_cached_device_parameter(ACParameter.OUTDOOR_TEMPERATURE))
            - 5000
        ) / 100

    def get_target_temperature(self) -> float | None:
        return (
            int(self._get_cached_device_parameter(ACParameter.TARGET_TEMPERATURE)) / 10
        )

    async def set_target_temperature(self, target_temperature: float):
        if target_temperature < self._min_temp or target_temperature > self._max_temp:
            raise AirstageACError(
                f"Invalid targetTemperature: {target_temperature}. Value must be {self._min_temp} <= target <= {self._max_temp}"
            )

        actual_target = int(target_temperature * 10)
        await self._set_device_parameter(ACParameter.TARGET_TEMPERATURE, actual_target)

    def get_vertical_direction(self):
        value = self._get_cached_device_parameter(ACParameter.VERTICAL_DIRECTION)
        if value == CAPABILITY_NOT_AVAILABLE:
            return

        return VALUE_TO_VERTICAL_POSITION[int(value)]

    async def set_vertical_direction(self, direction: VerticalSwingPosition):
        if not isinstance(direction, VerticalSwingPosition):
            raise AirstageACError(f"Invalid fan direction value: {direction}")
        await self._set_device_parameter(ACParameter.VERTICAL_DIRECTION, direction)

    def get_vertical_swing(self) -> BooleanDescriptors | None:
        value = self._get_cached_device_parameter(ACParameter.VERTICAL_SWING)
        if value == CAPABILITY_NOT_AVAILABLE:
            return

        return VALUE_TO_BOOLEAN[int(value)]

    async def set_vertical_swing(self, mode: BooleanProperty):
        if not isinstance(mode, BooleanProperty):
            raise AirstageACError(f"Invalid mode value: {mode}")
        await self._set_device_parameter(ACParameter.VERTICAL_SWING, mode)

    async def _set_device_parameter(self, parameterName: ACParameter, value):
        if not isinstance(parameterName, ACParameter):
            raise AirstageACError(f"Invalid property name: {parameterName}")

        updatedValue = await self._api.set_parameter(self._dsn, parameterName, value)
        if updatedValue is not None:
            self._cache[parameterName] = value
            return value

    def get_economy_mode(self) -> BooleanDescriptors | None:
        value = self._get_cached_device_parameter(ACParameter.ECONOMY_MODE)
        if value == CAPABILITY_NOT_AVAILABLE:
            return

        return VALUE_TO_BOOLEAN[int(value)]

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
        value = self._get_cached_device_parameter(ACParameter.POWERFUL_MODE)
        if value == CAPABILITY_NOT_AVAILABLE:
            return

        return VALUE_TO_BOOLEAN[int(value)]

    async def set_powerful_mode(self, mode: BooleanProperty):
        if not isinstance(mode, BooleanProperty):
            raise AirstageACError(f"Invalid mode value: {mode}")
        await self._set_device_parameter(ACParameter.POWERFUL_MODE, mode)

    def get_outdoor_low_noise(self) -> BooleanDescriptors | None:
        value = self._get_cached_device_parameter(ACParameter.OUTDOOR_LOW_NOISE)
        if value == CAPABILITY_NOT_AVAILABLE:
            return

        return VALUE_TO_BOOLEAN[int(value)]

    async def set_outdoor_low_noise(self, mode: BooleanProperty):
        if not isinstance(mode, BooleanProperty):
            raise AirstageACError(f"Invalid mode value: {mode}")
        await self._set_device_parameter(ACParameter.OUTDOOR_LOW_NOISE, mode)

    def get_indoor_led(self) -> BooleanDescriptors | None:
        value = self._get_cached_device_parameter(ACParameter.INDOOR_LED)
        if value == CAPABILITY_NOT_AVAILABLE:
            return

        return VALUE_TO_BOOLEAN[int(value)]

    async def set_indoor_led(self, mode: BooleanProperty):
        if not isinstance(mode, BooleanProperty):
            raise AirstageACError(f"Invalid mode value: {mode}")
        await self._set_device_parameter(ACParameter.INDOOR_LED, mode)
