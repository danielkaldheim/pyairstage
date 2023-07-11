import enum


# version 1.0.0


class OperationMode(enum.IntEnum):
    AUTO = 0
    COOL = 1
    DRY = 2
    FAN = 3
    HEAT = 4

    def __str__(self):
        return str(self._value_)


class OperationModeDescriptors(enum.Enum):
    OFF = "OFF"
    ON = "ON"
    AUTO = "AUTO"
    COOL = "COOL"
    DRY = "DRY"
    FAN = "FAN"
    HEAT = "HEAT"

    def __str__(self):
        return self._value_


# 0: OperationModeDescriptors.OFF,
# 1: OperationModeDescriptors.ON,
VALUE_TO_OPERATION_MODE = {
    0: OperationModeDescriptors.AUTO,
    1: OperationModeDescriptors.COOL,
    2: OperationModeDescriptors.DRY,
    3: OperationModeDescriptors.FAN,
    4: OperationModeDescriptors.HEAT,
}


class FanSpeed(enum.IntEnum):
    AUTO = 0
    QUIET = 2
    LOW = 5
    MEDIUM = 8
    HIGH = 11

    def __str__(self):
        return str(self._value_)


class FanSpeedDescriptors(enum.Enum):
    QUIET = "QUIET"
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    AUTO = "AUTO"

    def __str__(self):
        return self._value_


VALUE_TO_FAN_SPEED = {
    0: FanSpeedDescriptors.AUTO,
    2: FanSpeedDescriptors.QUIET,
    5: FanSpeedDescriptors.LOW,
    8: FanSpeedDescriptors.MEDIUM,
    11: FanSpeedDescriptors.HIGH,
}


class BooleanProperty(enum.IntEnum):
    OFF = 0
    ON = 1

    def __str__(self):
        return str(self._value_)


class BooleanDescriptors(enum.Enum):
    ON = "ON"
    OFF = "OFF"

    def __str__(self):
        return self._value_


VALUE_TO_BOOLEAN = {0: BooleanDescriptors.OFF, 1: BooleanDescriptors.ON}


class VerticalSwingPosition(enum.IntEnum):
    HIGHEST = 1
    HIGH = 2
    LOW = 3
    LOWEST = 4

    def __str__(self):
        return str(self._value_)


class VerticalPositionDescriptors(enum.Enum):
    HIGHEST = "HIGHEST"
    HIGH = "HIGH"
    CENTER_HIGH = "CENTER_HIGH"
    CENTER_LOW = "CENTER_LOW"
    LOW = "LOW"
    LOWEST = "LOWEST"

    def __str__(self):
        return self._value_


VALUE_TO_VERTICAL_POSITION = {
    1: VerticalPositionDescriptors.HIGHEST,
    2: VerticalPositionDescriptors.HIGH,
    3: VerticalPositionDescriptors.LOW,
    4: VerticalPositionDescriptors.LOWEST,
}


class ACParameter(enum.Enum):
    ONOFF_MODE = "iu_onoff"
    OPERATION_MODE = "iu_op_mode"
    FAN_SPEED = "iu_fan_spd"

    POWERFUL_MODE = "iu_powerful"
    ECONOMY_MODE = "iu_economy"
    TARGET_TEMPERATURE = "iu_set_tmp"
    INDOOR_TEMPERATURE = "iu_indoor_tmp"
    OUTDOOR_TEMPERATURE = "iu_outdoor_tmp"

    REFRESH_READ_PROPERTIES = "get_prop"
    VERTICAL_SWING = "iu_af_swg_vrt"
    VERTICAL_DIRECTION = "iu_af_dir_vrt"

    # # below are readonly properties
    # DISPLAY_TEMPERATURE = "display_temperature"
    # # Unclear what this does, seems to somewhat correlate to af_vertical_direction but not entirely
    # VERTICAL_SWING_POSITION = "af_vertical_num_dir"
    DEVICE_NAME = "deviceName"

    def __str__(self):
        return self._value_
