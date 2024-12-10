import logging
import time
import os
import json
from typing import Any, Coroutine
import uuid
import asyncio
import aiohttp
from .constants import ACParameter

HEADER_CONTENT_TYPE = "Content-Type"
HEADER_USER_AGENT = "User-Agent"
HEADER_VALUE_CONTENT_TYPE = "application/json"
HEADER_AUTHORIZATION = "Authorization"


class AirstageApi:
    """Airstage API"""

    async def get_devices(self) -> Coroutine[Any, Any, dict]:
        """Get account devices"""
        pass

    async def set_parameter(self, dsn: str, name: str, value: str):
        """Get set device parameter"""
        pass


class ApiError(Exception):
    """Airstage Error"""


_LOGGER = logging.getLogger(__name__)


def _api_headers(access_token: str | None = None) -> dict[str, str]:
    headers = {
        HEADER_CONTENT_TYPE: HEADER_VALUE_CONTENT_TYPE,
        HEADER_USER_AGENT: "Mozilla/5.0 (iPhone; CPU iPhone OS 16_6 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Mobile/15E148",
    }

    if access_token:
        headers[HEADER_AUTHORIZATION] = "Bearer " + access_token

    return headers


class ApiCloud(AirstageApi):
    def __init__(
        self,
        region: str = "eu",
        tokenpath: str = "token.json",
        session: aiohttp.ClientSession = None,
        retry: int = 5,
        username: str | None = None,
        password: str | None = None,
        country: str | None = None,
    ) -> None:
        if session is None:
            session = aiohttp.ClientSession()
        self.region = region
        self.osVersion = "iOS 16.6"
        self.session = session
        self.retry = retry
        self.deviceToken = (
            "daKkE967jU78oX5UsuE8dc:APA91bGNPMLBZFdiKDo97U5Oxtg7bJyGhdMbh8e37SKRE2hq1i2HIDooGDfoeiCyqaWd3H5FdgmfOemHzPpZuvE2RALkUod-5O-6lnNHIeuQ0VSxjYKyav9ph7D3aqdokGn6LGNlo372",
        )
        self.username = username
        self.password = password
        self.country = country

        if region == "eu":
            self._SIGNIN_BODY = '{"user": {"email": "%s","password": "%s","country": "%s","language": "en","deviceToken": "%s","ssid": "%s","osVersion": "%s"}}'
            self._REFRESH_BODY = '{"user": {"refreshToken": "%s"}}'
            self._SET_PARAMETER_BODY = '{"deviceSubId": 0, "parameters": [{"name": "%s","desiredValue": "%s"}]}'
            self._API_GET_ACCESS_TOKEN_URL = (
                "https://bke.euro.airstagelight.com/apiv1/users/sign_in"
            )
            self._API_REFRESH_TOKEN_URL = (
                "https://bke.euro.airstagelight.com/apiv1/users/me/refresh_token"
            )
            self._API_BASE_URL = "https://bke.euro.airstagelight.com/apiv1/"
        elif region == "cn":
            raise ApiError("CN region not supported yet")
        else:
            raise ApiError("US region not supported yet")

        self._ACCESS_TOKEN_FILE = tokenpath

    async def authenticate(self, refresh_token: str | None = None) -> str:
        if refresh_token:
            response = await self.async_call_api(
                "POST",
                self._API_REFRESH_TOKEN_URL,
                json=self._REFRESH_BODY % (refresh_token),
                headers=_api_headers(),
            )
        else:
            if not self.username:
                raise ApiError("username should not be empty")

            response = await self.async_call_api(
                "POST",
                self._API_GET_ACCESS_TOKEN_URL,
                json=self._SIGNIN_BODY
                % (
                    self.username,
                    self.password,
                    self.country,
                    self.deviceToken,
                    str(uuid.uuid4()),
                    self.osVersion,
                ),
                headers=_api_headers(),
            )

        response["time"] = int(time.time())
        access_token = response["accessToken"]

        f = open(self._ACCESS_TOKEN_FILE, "w", encoding="utf8")
        f.write(json.dumps(response))
        return access_token

    async def get_devices(self):
        access_token = await self._read_token()
        response = await self.async_call_api(
            "GET",
            f"{self._API_BASE_URL}/devices/all",
            headers=_api_headers(access_token=access_token),
        )

        devices = {}
        if response["devices"]:
            for device in response["devices"]:
                devices[device["deviceId"]] = device

        _LOGGER.debug(devices)

        return devices

    async def set_parameter(self, dsn: str, name: str, value: str):
        access_token = await self._read_token()
        response = await self.async_call_api(
            "POST",
            f"{self._API_BASE_URL}/devices/{dsn}/set_parameters_request",
            json=self._SET_PARAMETER_BODY % (name, value),
            headers=_api_headers(access_token=access_token),
        )
        _LOGGER.debug(self._SET_PARAMETER_BODY % (name, value))

        _LOGGER.debug(response)

        return response

    async def async_call_api(
        self,
        method: str,
        url: str,
        access_token: str | None = None,
        retry: int = None,
        **kwargs,
    ):
        retry = retry or self.retry
        data = {}
        count = 0
        error = None

        payload = kwargs.get("json")

        if "headers" not in kwargs:
            if access_token:
                kwargs["headers"] = _api_headers(access_token=access_token)
            else:
                kwargs["headers"] = _api_headers()

        if method.lower() == "post":
            if not payload:
                raise ApiError(f"Post method needs a request body!")

        while count < retry:
            count += 1
            try:
                async with self.session.request(
                    method,
                    url,
                    timeout=aiohttp.ClientTimeout(total=4),
                    data=payload,
                    headers=kwargs.get("headers"),
                ) as resp:
                    assert resp.status == 200
                    data = await resp.json(content_type=None)
                    return data
            except (
                aiohttp.ClientError,
                aiohttp.ClientConnectorError,
                aiohttp.client_exceptions.ServerDisconnectedError,
                ConnectionResetError,
            ) as err:
                error = err
            except asyncio.TimeoutError:
                error = "Connection timed out."
            except AssertionError:
                error = "Response status not 200."
                break
            except SyntaxError as err:
                error = "Invalid response"
                break

            await asyncio.sleep(1)
        raise ApiError(
            f"No valid response after {count} failed attempt{['','s'][count>1]}. Last error was: {error}"
        )

    async def _read_token(self, access_token_file=None) -> str | None:
        if not access_token_file:
            access_token_file = self._ACCESS_TOKEN_FILE
        if (
            os.path.exists(access_token_file)
            and os.stat(access_token_file).st_size != 0
        ):
            f = open(access_token_file, "r", encoding="utf8")
            access_token_file_content = f.read()
            data = json.loads(access_token_file_content)
            now = int(time.time())
            if data["accessToken"]:
                access_token = data["accessToken"]

                if now < (int(data["time"]) + int(data["expiresIn"])):
                    return access_token
                os.remove(access_token_file)
                return await self.authenticate(refresh_token=data["refreshToken"])
        return await self.authenticate()


class ApiLocal(AirstageApi):
    _GET_PARAMETER_BODY = '{"device_id": "%s","device_sub_id": %i,"req_id": "","modified_by": "","set_level": "%s","list": %s }'
    _GET_PARAMETER_BODY = ""

    def __init__(
        self,
        session: aiohttp.ClientSession = None,
        retry: int = 5,
        device_id: str | None = None,
        ip_address: str | None = None,
    ) -> None:
        if session is None:
            session = aiohttp.ClientSession()

        self.session = session
        self.retry = retry
        self.device_id = device_id
        self.ip_address = ip_address

    async def get_devices(self):
        modelInfo = {}
        try:
            modelInfo = await self.get_parameters(
                [
                    ACParameter.MODEL,
                ],
            )
        except ApiError as err:
            _LOGGER.debug(err)

        acInfo = await self.get_parameters(
            [
                ACParameter.INDOOR_LED,
                # "iu_af_inc_hrz",
                # "iu_af_inc_vrt",
                ACParameter.INDOOR_TEMPERATURE,
                ACParameter.OUTDOOR_TEMPERATURE,
                ACParameter.HMN_DETECTION,
                # "iu_main_ver",
                # "iu_eep_ver",
                # "iu_has_upd_main",
                # "iu_has_upd_eep",
                # "iu_fld_set80",
            ],
        )

        modeInfo = await self.get_parameters(
            [
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
            ],
        )

        parameters = modelInfo | acInfo | modeInfo

        formattedParameters = []
        for key in parameters:
            formattedParameters.append(
                {"name": key, "value": parameters[key], "modifiedAt": ""}
            )

        devices = {}

        model = "Airstage"
        if ACParameter.MODEL in parameters:
            model = parameters[ACParameter.MODEL]

        devices[self.device_id] = {
            "isSubuser": False,
            "deviceId": self.device_id,
            "deviceName": self.device_id,
            "model": model,
            "parameters": formattedParameters,
        }

        _LOGGER.debug(devices)

        return devices

    async def get_parameters(
        self, value: [], device_sub_id: int = 0, level: str = "03"
    ):
        jsonPayload = {
            "device_id": self.device_id,
            "device_sub_id": device_sub_id,
            "req_id": "",
            "modified_by": "",
            "set_level": level,
            "list": value,
        }

        _LOGGER.debug(json.dumps(jsonPayload))

        response = await self.async_call_api(
            "POST", f"http://{self.ip_address}/GetParam", json=json.dumps(jsonPayload)
        )

        _LOGGER.debug(response)

        if "result" in response and response["result"] == "OK":
            return response["value"]

        raise ApiError(f"Get parameter failed")

    async def set_parameter(self, dsn: str, name: str, value: str):
        jsonPayload = {
            "device_id": dsn,
            "device_sub_id": 0,
            "req_id": "",
            "modified_by": "",
            "set_level": "02",
            "value": {str(name): str(value)},
        }

        _LOGGER.debug(json.dumps(jsonPayload))

        response = await self.async_call_api(
            "POST", f"http://{self.ip_address}/SetParam", json=json.dumps(jsonPayload)
        )

        _LOGGER.debug(response)

        return response

    async def async_call_api(
        self,
        method: str,
        url: str,
        retry: int = None,
        **kwargs,
    ):
        retry = retry or self.retry
        data = {}
        count = 0
        error = None

        payload = kwargs.get("json")

        if method.lower() == "post":
            if not payload:
                raise ApiError(f"Post method needs a request body!")

        while count < retry:
            count += 1
            try:
                async with self.session.request(
                    method,
                    url,
                    timeout=aiohttp.ClientTimeout(total=4),
                    data=payload,
                    headers=kwargs.get("headers"),
                ) as resp:
                    assert resp.status == 200
                    data = await resp.json(content_type=None)
                    return data
            except (
                aiohttp.ClientError,
                aiohttp.ClientConnectorError,
                aiohttp.client_exceptions.ServerDisconnectedError,
                ConnectionResetError,
            ) as err:
                error = err
            except asyncio.TimeoutError:
                error = "Connection timed out."
            except AssertionError:
                error = "Response status not 200."
                break
            except SyntaxError as err:
                error = "Invalid response"
                break

            await asyncio.sleep(1)
        raise ApiError(
            f"No valid response after {count} failed attempt{['','s'][count>1]}. Last error was: {error}"
        )
