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


class VerticalSwingPositions(enum.StrEnum):
    # Note: These strings correspond to HA swing positions
    HIGHEST = "Highest"
    HIGH = "High"
    CENTER_HIGH = "Center High"
    CENTER_LOW = "Center Low"
    LOW = "Low"
    LOWEST = "Lowest"


class VerticalSwing4PositionsValues(enum.IntEnum):
    HIGHEST = 1
    HIGH = 2
    LOW = 3
    LOWEST = 4


class VerticalSwing6PositionsValues(enum.IntEnum):
    HIGHEST = 1
    HIGH = 2
    CENTER_HIGH = 3
    CENTER_LOW = 4
    LOW = 5
    LOWEST = 6


CAPABILITY_NOT_AVAILABLE = "65535"


class ACParameter(enum.StrEnum):
    ONOFF_MODE = "iu_onoff"
    OPERATION_MODE = "iu_op_mode"
    FAN_SPEED = "iu_fan_spd"

    POWERFUL_MODE = "iu_powerful"
    ECONOMY_MODE = "iu_economy"
    ENERGY_SAVE_FAN = "iu_fan_ctrl"
    TARGET_TEMPERATURE = "iu_set_tmp"
    INDOOR_TEMPERATURE = "iu_indoor_tmp"
    OUTDOOR_TEMPERATURE = "iu_outdoor_tmp"

    REFRESH_READ_PROPERTIES = "get_prop"
    VERTICAL_SWING = "iu_af_swg_vrt"
    VERTICAL_SWING_POSITIONS = "iu_af_inc_vrt"
    VERTICAL_DIRECTION = "iu_af_dir_vrt"
    HORIZONTAL_SWING = "iu_af_dir_hrz"
    HORIZONTAL_DIRECTION = "iu_af_swg_hrz"

    HMN_DETECTION = "iu_hmn_det"
    HMN_DETECTION_AUTO_SAVE = "iu_hmn_det_auto_save"

    OUTDOOR_LOW_NOISE = "ou_low_noise"

    INDOOR_LED = "iu_wifi_led"

    MINIMUM_HEAT = "iu_min_heat"

    # # below are readonly properties
    # DISPLAY_TEMPERATURE = "display_temperature"
    # # Unclear what this does, seems to somewhat correlate to af_vertical_direction but not entirely
    # VERTICAL_SWING_POSITION = "af_vertical_num_dir"
    DEVICE_NAME = "deviceName"
    MODEL = "iu_model"

    ERROR_CODE = "iu_err_code"
    DEMAND = "iu_demand"
    SIGN_RESET = "iu_fltr_sign_reset"

    def __str__(self):
        return self._value_


class ACConstants:
    AUTO_MIN_TEMP = 18.0
    AUTO_MAX_TEMP = 30.0
    COOL_MIN_TEMP = 18.0
    COOL_MAX_TEMP = 30.0
    DRY_MIN_TEMP = 18.0
    DRY_MAX_TEMP = 30.0
    HEAT_MIN_TEMP = 16.0
    HEAT_MAX_TEMP = 30.0
