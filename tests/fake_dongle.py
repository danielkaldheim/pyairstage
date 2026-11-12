"""In-process stand-in for a Fujitsu Airstage Wi-Fi dongle's local HTTP API."""

from __future__ import annotations

import json
import logging
import threading
import time
from collections.abc import Mapping
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from types import TracebackType
from typing import Any, TypeAlias, TypedDict

_LOGGER = logging.getLogger(__name__)

DEVICE_ID: str = "106838E4F507"
MODEL: str = "ASUH07LPTA"

#: Wire format is always string -> string, exactly as the real adapter sends it.
RawParams: TypeAlias = dict[str, str]
#: Decoded JSON request body; the library sends arbitrary keys, so `Any` is honest here.
JsonObject: TypeAlias = dict[str, Any]


class ParameterEntry(TypedDict):
    """One element of the `parameters` list in a `get_devices()` payload."""

    name: str
    value: str
    modifiedAt: str


class DevicePayload(TypedDict):
    """Shape returned by `ApiLocal.get_devices()[device_id]`."""

    isSubuser: bool
    deviceId: str
    deviceName: str
    model: str
    parameters: list[ParameterEntry]


class RequestRecord(TypedDict):
    """Captured request, for wire-format assertions."""

    method: str
    path: str
    body: JsonObject


# Values mirror the real unit: temps are (value - 5000) / 100, setpoint is value / 10.
DEFAULT_PARAMS: RawParams = {
    "iu_model": MODEL,
    "iu_wifi_led": "1",
    "iu_indoor_tmp": "7425",
    "iu_outdoor_tmp": "7400",
    "iu_pow_cons": "228928",
    "ou_pow_cons": "0",
    "iu_onoff": "1",
    "iu_op_mode": "4",  # 4 = HEAT
    "iu_fan_spd": "5",  # 5 = LOW
    "iu_set_tmp": "220",  # 22.0 C
    "iu_af_swg_vrt": "0",
    "iu_af_inc_vrt": "4",  # 4 swing positions
    "iu_af_dir_vrt": "3",  # 3 of 4 = LOW
    "iu_af_dir_hrz": "0",
    "iu_af_swg_hrz": "0",
    "iu_hmn_det": "65535",  # capability unavailable
    "iu_hmn_det_auto_save": "65535",
    "iu_min_heat": "0",
    "iu_powerful": "0",
    "iu_economy": "0",
    "iu_fan_ctrl": "0",
    "iu_err_code": "0",
    "iu_demand": "0",
    "iu_fltr_sign_reset": "0",
    "ou_low_noise": "0",
}


class FakeDongle:
    """Threaded HTTP server that speaks the local GetParam/SetParam protocol.

    Any parameter the client asks for is echoed back from ``params``; unknown
    names are silently omitted, which is what the real adapter does.
    """

    def __init__(
        self,
        device_id: str = DEVICE_ID,
        params: Mapping[str, str] | None = None,
    ) -> None:
        self.device_id: str = device_id
        self.params: RawParams = dict(DEFAULT_PARAMS if params is None else params)
        self.requests: list[RequestRecord] = []
        self.result: str | None = None  # force "NG" to simulate a rejected call
        self.delay: float = 0.0  # seconds to stall before replying
        self.drop_next: int = 0  # close the socket instead of replying
        self._server: ThreadingHTTPServer | None = None
        self._thread: threading.Thread | None = None

    # ---- lifecycle -------------------------------------------------
    def start(self) -> Self:  # noqa: F821  (typing.Self, 3.11+)
        outer = self

        class Handler(BaseHTTPRequestHandler):
            protocol_version = "HTTP/1.1"

            def do_GET(self) -> None:  # curl -X GET, like a real unit
                outer._handle(self)

            def do_POST(self) -> None:  # what ApiLocal actually sends
                outer._handle(self)

            def log_message(self, format: str, *args: Any) -> None:
                pass

            def log_error(self, format: str, *args: Any) -> None:
                _LOGGER.warning(format % args)

        self._server = ThreadingHTTPServer(("127.0.0.1", 0), Handler)
        self._server.daemon_threads = True

        self._thread = threading.Thread(
            target=self._server.serve_forever, daemon=True, name="fake-dongle"
        )
        self._thread.start()
        return self

    def stop(self) -> None:
        if self._server is not None:
            self._server.shutdown()
            self._server.server_close()
            self._server = None
        if self._thread is not None:
            self._thread.join(timeout=5)
            self._thread = None

    def __enter__(self) -> Self:
        return self.start()

    def __exit__(
        self,
        exc_type: type[BaseException] | None,
        exc: BaseException | None,
        tb: TracebackType | None,
    ) -> None:
        self.stop()

    @property
    def port(self) -> int:
        assert self._server is not None, "dongle not started"
        return int(self._server.server_address[1])

    @property
    def hostport(self) -> str:
        """Pass straight to ``ApiLocal(ip_address=...)``."""
        return f"127.0.0.1:{self.port}"

    @property
    def url(self) -> str:
        return f"http://{self.hostport}"

    # ---- test helpers ----------------------------------------------
    def reset(self) -> None:
        self.requests.clear()
        self.result = None
        self.delay = 0.0
        self.drop_next = 0

    def device_payload(self) -> DevicePayload:
        """A ``get_devices()``-shaped dict for ``AirstageAC.refresh_parameters(data=...)``."""
        return {
            "isSubuser": False,
            "deviceId": self.device_id,
            "deviceName": self.device_id,
            "model": self.params.get("iu_model", "Airstage"),
            "parameters": [
                {"name": name, "value": value, "modifiedAt": ""}
                for name, value in self.params.items()
            ],
        }

    def last_request(self, path: str) -> RequestRecord:
        for req in reversed(self.requests):
            if req["path"] == path:
                return req
        seen = [r["path"] for r in self.requests]
        raise AssertionError(f"no request to {path}; saw {seen}")

    # ---- protocol --------------------------------------------------
    @staticmethod
    def _read_body(handler: BaseHTTPRequestHandler) -> JsonObject:
        length = int(handler.headers.get("Content-Length") or 0)
        raw = handler.rfile.read(length) if length else b""
        if not raw:
            return {}
        try:
            parsed: Any = json.loads(raw)
        except json.JSONDecodeError:
            return {"_raw": raw.decode("utf-8", "replace")}
        return parsed if isinstance(parsed, dict) else {"_parsed": parsed}

    @staticmethod
    def _reply(
        handler: BaseHTTPRequestHandler,
        payload: Mapping[str, Any],
        status: int = 200,
    ) -> None:
        body = json.dumps(payload).encode()
        handler.send_response(status)
        handler.send_header("Content-Type", "application/json")
        handler.send_header("Content-Length", str(len(body)))
        handler.send_header("Connection", "close")
        handler.end_headers()
        handler.wfile.write(body)
        handler.close_connection = True

    def _handle(self, handler: BaseHTTPRequestHandler) -> None:
        body = self._read_body(handler)
        path = handler.path.split("?")[0]
        self.requests.append(
            RequestRecord(method=handler.command, path=path, body=body)
        )

        if self.delay:
            time.sleep(self.delay)

        if self.drop_next:
            self.drop_next -= 1
            handler.close_connection = True
            try:
                handler.connection.close()  # mimic the adapter hanging up
            except OSError:
                pass
            return

        result = self.result or "OK"
        envelope: dict[str, Any] = {
            "read_res": "ack",
            "device_id": body.get("device_id", self.device_id),
            "device_sub_id": body.get("device_sub_id", 0),
            "req_id": body.get("req_id", ""),
            "modified_by": body.get("modified_by", ""),
            "set_level": body.get("set_level", "03"),
            "cause": "",
            "result": result,
            "error": "" if result == "OK" else "injected failure",
        }

        if body.get("device_id") not in (None, self.device_id):
            envelope.update(result="NG", error="device_id mismatch")
            self._reply(handler, envelope)
            return

        if path == "/GetParam":
            names: list[str] = body.get("list") or []
            envelope["value"] = {
                name: self.params[name] for name in names if name in self.params
            }
        elif path == "/SetParam":
            values: Mapping[str, Any] = body.get("value") or {}
            for name, value in values.items():
                self.params[str(name)] = str(value)  # visible to later reads
            envelope["value"] = {}
        else:
            envelope.update(result="NG", error="unknown endpoint")
            self._reply(handler, envelope, status=404)
            return

        self._reply(handler, envelope)
