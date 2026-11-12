import enum

CAPABILITY_NOT_AVAILABLE = "65535"


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
    MEDIUM_LOW = "MEDIUM_LOW"
    MEDIUM = "MEDIUM"
    MEDIUM_HIGH = "MEDIUM_HIGH"
    HIGH = "HIGH"
    AUTO = "AUTO"

    def __str__(self):
        return self._value_


VALUE_TO_FAN_SPEED = {
    0: FanSpeedDescriptors.AUTO,
    2: FanSpeedDescriptors.QUIET,
    5: FanSpeedDescriptors.LOW,
    7: FanSpeedDescriptors.MEDIUM_LOW,
    8: FanSpeedDescriptors.MEDIUM,
    9: FanSpeedDescriptors.MEDIUM_HIGH,
    11: FanSpeedDescriptors.HIGH,
}


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

    POWER_CONSUMPTION = "iu_pow_cons"

    VERTICAL_SWING = "iu_af_swg_vrt"
    VERTICAL_SWING_POSITIONS = "iu_af_inc_vrt"
    VERTICAL_DIRECTION = "iu_af_dir_vrt"

    HORIZONTAL_SWING = "iu_af_swg_hrz"
    HORIZONTAL_DIRECTION = "iu_af_dir_hrz"

    HMN_DETECTION = "iu_hmn_det"
    HMN_DETECTION_AUTO_SAVE = "iu_hmn_det_auto_save"

    OUTDOOR_LOW_NOISE = "ou_low_noise"

    INDOOR_LED = "iu_wifi_led"

    MINIMUM_HEAT = "iu_min_heat"

    MODEL = "iu_model"

    ERROR_CODE = "iu_err_code"
    DEMAND = "iu_demand"
    SIGN_RESET = "iu_fltr_sign_reset"

    # full list of known parameters as a reference (note: many not actually populated, at least on my units)
    # iu_af_dir_cntr_hrz
    # iu_af_dir_cntr_vrt
    # iu_af_dir_hrz
    # iu_af_dir_side_hrz
    # iu_af_dir_side_vrt
    # iu_af_dir_vrt
    # iu_af_fan_pattern
    # iu_af_inc_hrz
    # iu_af_inc_vrt
    # iu_af_swg_hrz
    # iu_af_swg_vrt
    # iu_ai_auto_fnc
    # iu_ai_eco
    # iu_ai_eco_jp
    # iu_ai_ecosw_jp
    # iu_ai_fnc
    # iu_ai_group_id
    # iu_ai_hist
    # iu_ai_infr
    # iu_ai_infr_chg
    # iu_ai_sug_time
    # iu_ai_time_h
    # iu_ai_time_m
    # iu_ai_timer
    # iu_ai_timer_fnc
    # iu_ai_timer_stat
    # iu_anti_frz
    # iu_auto_clean_jp
    # iu_auto_off_time
    # iu_auto_save_time
    # iu_buzzer
    # iu_clean_sug
    # iu_cmp_time
    # iu_coil_dry
    # iu_comf_af
    # iu_consign
    # iu_demand
    # iu_dev_cap
    # iu_drain_pump
    # iu_dry_adj
    # iu_dry_cool_jp
    # iu_dry_type
    # iu_economy
    # iu_eeprom
    # iu_eeprom_fw_ota_path
    # iu_eeprom_model_name
    # iu_eeprom_ver
    # iu_eep_ver
    # iu_eng_time
    # iu_err_code
    # iu_fan
    # iu_fan_ctrl
    # iu_fan_rot
    # iu_fan_side_spd
    # iu_fan_spd
    # iu_fld_set
    # iu_fld_set_start
    # iu_fltr_sign_reset
    # iu_fltr_time
    # iu_force_dump
    # iu_frz_prev
    # iu_fw_fw_ota_path
    # iu_has_af_wide
    # iu_has_ai_eco
    # iu_has_ai_timer
    # iu_has_auto_clean
    # iu_has_comf_af
    # iu_has_fld_set
    # iu_has_heat_ster
    # iu_has_hmd_snsr
    # iu_has_mtim
    # iu_has_srv_mntr
    # iu_has_tmp_lmt
    # iu_has_upd_eep
    # iu_has_upd_main
    # iu_has_watch
    # iu_heat_ex_tmp
    # iu_heat_ster
    # iu_hmd
    # iu_hmn_det
    # iu_hmn_det_auto_off
    # iu_hmn_det_auto_save
    # iu_indoor_tmp
    # iu_indoor_tmp_crct
    # iu_int_op_mode
    # iu_main
    # iu_main_model_name
    # iu_main_ver
    # iu_malfnc_detail
    # iu_malfnc_disp
    # iu_malfnc_disp_
    # iu_malfnc_stat
    # iu_min_heat
    # iu_mnt_icon
    # iu_model
    # iu_monitor
    # iu_mtim
    # iu_mtim_stat
    # iu_obj
    # iu_onoff
    # iu_on_timer_sug
    # iu_op_mode
    # iu_op_stat
    # iu_outdoor_tmp
    # iu_polling_data
    # iu_pow_cons
    # iu_powerful
    # iu_pow_inf_yest
    # iu_push_ntfy
    # iu_room
    # iu_schedule_execute
    # iu_set_tmp
    # iu_set_tmp_
    # iu_side_fan
    # iu_side_fan_fnc
    # iu_suct_tmp
    # iu_test_op
    # iu_tmp_hi_auto
    # iu_tmp_hi_cool
    # iu_tmp_hi_heat
    # iu_tmp_inc
    # iu_tmp_lo_auto
    # iu_tmp_lo_cool
    # iu_tmp_lo_heat
    # iu_watch_stat
    # iu_wifi_led
    # ou_cmp_freq
    # ou_current
    # ou_disc_tmp
    # ou_exp_vlv
    # ou_fan
    # ou_fan_rot
    # ou_four_way_vlv
    # ou_heat_ex_tmp
    # ou_heat_ex_tmp_out
    # ou_low_noise
    # ou_model
    # ou_outdoor_tmp

    def __str__(self):
        return self._value_


DEFAULT_PARAMETER_COLLECTION = [
    ACParameter.MODEL,
    ACParameter.INDOOR_LED,
    ACParameter.INDOOR_TEMPERATURE,
    ACParameter.OUTDOOR_TEMPERATURE,
    ACParameter.POWER_CONSUMPTION,
    ACParameter.HMN_DETECTION,
    ACParameter.ONOFF_MODE,
    ACParameter.OPERATION_MODE,
    ACParameter.FAN_SPEED,
    ACParameter.TARGET_TEMPERATURE,
    ACParameter.VERTICAL_SWING_POSITIONS,
    ACParameter.VERTICAL_DIRECTION,
    ACParameter.VERTICAL_SWING,
    ACParameter.HORIZONTAL_DIRECTION,
    ACParameter.HORIZONTAL_SWING,
    ACParameter.OUTDOOR_LOW_NOISE,
    ACParameter.ENERGY_SAVE_FAN,
    ACParameter.HMN_DETECTION_AUTO_SAVE,
    ACParameter.MINIMUM_HEAT,
    ACParameter.POWERFUL_MODE,
    ACParameter.ECONOMY_MODE,
    ACParameter.ERROR_CODE,
    ACParameter.DEMAND,
    ACParameter.SIGN_RESET,
]


class ACConstants:
    AUTO_MIN_TEMP = 18.0
    AUTO_MAX_TEMP = 30.0
    COOL_MIN_TEMP = 18.0
    COOL_MAX_TEMP = 30.0
    DRY_MIN_TEMP = 18.0
    DRY_MAX_TEMP = 30.0
    HEAT_MIN_TEMP = 16.0
    HEAT_MAX_TEMP = 30.0
