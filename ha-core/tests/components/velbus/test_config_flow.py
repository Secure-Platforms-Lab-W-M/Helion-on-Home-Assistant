"""Tests for the Velbus config flow."""
from unittest.mock import AsyncMock, patch

import pytest
from velbusaio.exceptions import VelbusConnectionFailed

from homeassistant import data_entry_flow
from homeassistant.components.velbus import config_flow
from homeassistant.const import CONF_NAME, CONF_PORT

from tests.common import MockConfigEntry

PORT_SERIAL = "/dev/ttyACME100"
PORT_TCP = "127.0.1.0.1:3788"


@pytest.fixture(name="controller_assert")
def mock_controller_assert():
    """Mock the velbus controller with an assert."""
    with patch("velbusaio.controller.Velbus", side_effect=VelbusConnectionFailed()):
        yield


@pytest.fixture(name="controller")
def mock_controller():
    """Mock a successful velbus controller."""
    controller = AsyncMock()
    with patch("velbusaio.controller.Velbus", return_value=controller):
        yield controller


def init_config_flow(hass):
    """Init a configuration flow."""
    flow = config_flow.VelbusConfigFlow()
    flow.hass = hass
    return flow


async def test_user(hass, controller):
    """Test user config."""
    flow = init_config_flow(hass)

    result = await flow.async_step_user()
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["step_id"] == "user"

    result = await flow.async_step_user(
        {CONF_NAME: "Velbus Test Serial", CONF_PORT: PORT_SERIAL}
    )
    assert result["type"] == data_entry_flow.RESULT_TYPE_CREATE_ENTRY
    assert result["title"] == "velbus_test_serial"
    assert result["data"][CONF_PORT] == PORT_SERIAL

    result = await flow.async_step_user(
        {CONF_NAME: "Velbus Test TCP", CONF_PORT: PORT_TCP}
    )
    assert result["type"] == data_entry_flow.RESULT_TYPE_CREATE_ENTRY
    assert result["title"] == "velbus_test_tcp"
    assert result["data"][CONF_PORT] == PORT_TCP


async def test_user_fail(hass, controller_assert):
    """Test user config."""
    flow = init_config_flow(hass)

    result = await flow.async_step_user(
        {CONF_NAME: "Velbus Test Serial", CONF_PORT: PORT_SERIAL}
    )
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["errors"] == {CONF_PORT: "cannot_connect"}

    result = await flow.async_step_user(
        {CONF_NAME: "Velbus Test TCP", CONF_PORT: PORT_TCP}
    )
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["errors"] == {CONF_PORT: "cannot_connect"}


async def test_import(hass, controller):
    """Test import step."""
    flow = init_config_flow(hass)

    result = await flow.async_step_import({CONF_PORT: PORT_TCP})
    assert result["type"] == data_entry_flow.RESULT_TYPE_CREATE_ENTRY
    assert result["title"] == "velbus_import"


async def test_abort_if_already_setup(hass):
    """Test we abort if Daikin is already setup."""
    flow = init_config_flow(hass)
    MockConfigEntry(
        domain="velbus", data={CONF_PORT: PORT_TCP, CONF_NAME: "velbus home"}
    ).add_to_hass(hass)

    result = await flow.async_step_import(
        {CONF_PORT: PORT_TCP, CONF_NAME: "velbus import test"}
    )
    assert result["type"] == data_entry_flow.RESULT_TYPE_ABORT
    assert result["reason"] == "already_configured"

    result = await flow.async_step_user(
        {CONF_PORT: PORT_TCP, CONF_NAME: "velbus import test"}
    )
    assert result["type"] == data_entry_flow.RESULT_TYPE_FORM
    assert result["errors"] == {"port": "already_configured"}
