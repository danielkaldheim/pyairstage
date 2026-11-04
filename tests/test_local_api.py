"""Wire-format and behaviour tests against the fake dongle."""

from __future__ import annotations

import pytest

from pyairstage.airstageAC import AirstageAC, AirstageACError
from pyairstage.airstageApi import ApiError, ApiLocal
from pyairstage.constants import (
    ACParameter,
    BooleanDescriptors,
    FanSpeedDescriptors,
    OperationMode,
    OperationModeDescriptors,
)
from tests.fake_dongle import FakeDongle


async def test_get_parameters_wire_format(api: ApiLocal, dongle: FakeDongle) -> None:
    params = await api.get_parameters(
        [ACParameter.MODEL, ACParameter.INDOOR_TEMPERATURE]
    )

    assert params == {"iu_model": "ASUH07LPTA", "iu_indoor_tmp": "7425"}

    req = dongle.last_request("/GetParam")
    assert req["method"] == "POST"
    assert req["body"] == {
        "device_id": "106838E4F507",
        "device_sub_id": 0,
        "req_id": "",
        "modified_by": "",
        "set_level": "03",
        "list": ["iu_model", "iu_indoor_tmp"],
    }


async def test_unknown_parameter_is_omitted(api: ApiLocal) -> None:
    params = await api.get_parameters(["iu_model", "iu_not_a_real_param"])
    assert params == {"iu_model": "ASUH07LPTA"}


async def test_get_devices_shape(
    api: ApiLocal, dongle: FakeDongle, fast_sleep: None
) -> None:
    devices = await api.get_devices()

    assert list(devices) == ["106838E4F507"]
    device = devices["106838E4F507"]
    assert device["model"] == "ASUH07LPTA"
    assert {p["name"] for p in device["parameters"]} >= {"iu_onoff", "iu_set_tmp"}
    assert len(dongle.requests) == 2  # two batched GetParam calls


async def test_refresh_and_typed_getters(ac: AirstageAC) -> None:
    assert ac.get_device_on_off_state() is BooleanDescriptors.ON
    assert ac.get_operating_mode() is OperationModeDescriptors.HEAT
    assert ac.get_fan_speed() is FanSpeedDescriptors.LOW
    assert ac.get_target_temperature() == 22.0
    assert ac.get_display_temperature() == pytest.approx(24.25)
    assert ac.get_outdoor_temperature() == pytest.approx(24.0)
    assert ac.get_indoor_led() is BooleanDescriptors.ON
    assert ac.get_hmn_detection() is None  # 65535 -> capability unavailable
    assert ac.get_minimum_temperature() == 16.0
    assert ac.get_num_vertical_swing_positions() == 4


async def test_turn_off_sends_boolean(ac: AirstageAC, dongle: FakeDongle) -> None:
    await ac.turn_off()

    body = dongle.last_request("/SetParam")["body"]
    assert body["set_level"] == "02"
    assert body["value"] == {"iu_onoff": "0"}
    assert dongle.params["iu_onoff"] == "0"


async def test_set_operation_mode_sends_intenum_value(
    ac: AirstageAC, dongle: FakeDongle
) -> None:
    await ac.set_operation_mode(OperationMode.COOL)

    body = dongle.last_request("/SetParam")["body"]
    assert body["value"] == {"iu_op_mode": "1"}


async def test_set_target_temperature_rounds_to_half_degree(
    ac: AirstageAC, dongle: FakeDongle
) -> None:
    await ac.set_target_temperature(21.3)

    body = dongle.last_request("/SetParam")["body"]
    assert body["value"] == {"iu_set_tmp": "215"}
    assert dongle.params["iu_set_tmp"] == "215"
    assert ac.get_target_temperature() == 21.5


async def test_set_target_temperature_out_of_range(ac: AirstageAC) -> None:
    with pytest.raises(AirstageACError, match=r"Value must be 16.0 <= target <= 30.0"):
        await ac.set_target_temperature(35.0)


async def test_rejected_write_is_not_detected(
    ac: AirstageAC, dongle: FakeDongle
) -> None:
    """Documents current behaviour: ApiLocal.set_parameter never inspects `result`."""
    dongle.result = "NG"

    await ac.set_target_temperature(24.0)  # no exception raised
    assert ac.get_target_temperature() == 22.0  # cache correctly did not update


async def test_wrong_device_id_raises(api: ApiLocal, dongle: FakeDongle) -> None:
    dongle.device_id = "DEADBEEF0000"
    with pytest.raises(ApiError, match="Get parameter failed"):
        await api.get_parameters(["iu_model"])


async def test_set_parameter_accepts_only_strings(
    api: ApiLocal, dongle: FakeDongle
) -> None:
    """Non-string values are coerced by `str()` before hitting the wire."""
    await api.set_parameter("106838E4F507", ACParameter.TARGET_TEMPERATURE, 200)  # type: ignore[arg-type]

    assert dongle.last_request("/SetParam")["body"]["value"] == {"iu_set_tmp": "200"}
