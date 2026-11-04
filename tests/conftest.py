"""Shared fixtures: a fake dongle on localhost, an ApiLocal, and an AirstageAC."""

from __future__ import annotations

import asyncio
from collections.abc import AsyncIterator, Iterator
from typing import Any

import aiohttp
import pytest

from pyairstage.airstageAC import AirstageAC
from pyairstage.airstageApi import ApiLocal
from tests.fake_dongle import FakeDongle

DEVICE_ID: str = "106838E4F507"


@pytest.fixture
def dongle() -> Iterator[FakeDongle]:
    fake = FakeDongle().start()
    try:
        yield fake
    finally:
        fake.stop()


@pytest.fixture
def fast_sleep(monkeypatch: pytest.MonkeyPatch) -> None:
    """Skip the hard-coded 1s pause inside ApiLocal.get_devices().

    Note: this patches ``asyncio.sleep`` for the whole process during the test,
    not just the pyairstage module — monkeypatch restores it afterwards.
    """

    async def _noop(*args: Any, **kwargs: Any) -> None:
        return None

    monkeypatch.setattr(asyncio, "sleep", _noop)


@pytest.fixture
async def session() -> AsyncIterator[aiohttp.ClientSession]:
    async with aiohttp.ClientSession() as client_session:
        yield client_session


@pytest.fixture
async def api(dongle: FakeDongle, session: aiohttp.ClientSession) -> ApiLocal:
    # ip_address is interpolated straight into f"{protocol}://{ip_address}/GetParam",
    # so "host:port" works with no patching.
    return ApiLocal(
        session=session,
        device_id=dongle.device_id,
        ip_address=dongle.hostport,
        retry=2,
        timeout_seconds=2,
    )


@pytest.fixture
async def ac(dongle: FakeDongle, api: ApiLocal) -> AirstageAC:
    device = AirstageAC(dongle.device_id, api)
    device.refresh_parameters(dongle.device_payload())
    return device
