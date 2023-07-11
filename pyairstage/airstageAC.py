from .constants import *
from .api import Api


class AirstageAC:
    def __init__(self, dsn: str, api: Api) -> None:
        if not api:
            raise Exception("Missing api")

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
                raise Exception(f"dsn not found {self.dsn}")
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

    def _get_cached_device_parameter(self, parameterName: ACParameter) -> any:
        if not isinstance(parameterName, ACParameter):
            raise Exception(f"Invalid parameter name: {parameterName}")

        if parameterName in self._cache:
            return self._cache[parameterName]

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
            raise Exception(f"Invalid operationMode value: {mode}")
        await self._set_device_parameter(ACParameter.OPERATION_MODE, mode)

    def get_fan_speed(self):
        return VALUE_TO_FAN_SPEED[
            int(self._get_cached_device_parameter(ACParameter.FAN_SPEED))
        ]

    async def set_fan_speed(self, fan_speed: FanSpeed):
        if not isinstance(fan_speed, FanSpeed):
            raise Exception(f"Invalid fan speed value: {fan_speed}")
        await self._set_device_parameter(ACParameter.FAN_SPEED, fan_speed)

    def get_display_temperature(self) -> float | None:
        return (
            int(self._get_cached_device_parameter(ACParameter.INDOOR_TEMPERATURE))
            - 5000
        ) / 100

    def get_target_temperature(self) -> float | None:
        return (
            int(self._get_cached_device_parameter(ACParameter.TARGET_TEMPERATURE)) / 10
        )

    async def set_target_temperature(self, target_temperature: float):
        if target_temperature < self._min_temp or target_temperature > self._max_temp:
            raise Exception(
                f"Invalid targetTemperature: {target_temperature}. Value must be {self._min_temp} <= target <= {self._max_temp}"
            )

        actual_target = int(target_temperature * 10)
        await self._set_device_parameter(ACParameter.TARGET_TEMPERATURE, actual_target)

    def get_vertical_direction(self):
        return VALUE_TO_VERTICAL_POSITION[
            int(self._get_cached_device_parameter(ACParameter.VERTICAL_DIRECTION))
        ]

    async def set_vertical_direction(self, direction: VerticalSwingPosition):
        if not isinstance(direction, VerticalSwingPosition):
            raise Exception(f"Invalid fan direction value: {direction}")
        await self._set_device_parameter(ACParameter.VERTICAL_DIRECTION, direction)

    def get_vertical_swing(self):
        return VALUE_TO_BOOLEAN[
            int(self._get_cached_device_parameter(ACParameter.VERTICAL_SWING))
        ]

    async def set_vertical_swing(self, mode: BooleanProperty):
        if not isinstance(mode, BooleanProperty):
            raise Exception(f"Invalid mode value: {mode}")
        await self._set_device_parameter(ACParameter.VERTICAL_SWING, mode)

    async def _set_device_parameter(self, parameterName: ACParameter, value):
        if not isinstance(parameterName, ACParameter):
            raise Exception(f"Invalid property name: {parameterName}")

        await self._api.set_parameter(self._dsn, parameterName, value)
        self._cache[parameterName] = value
