"""Tests for the Freedompro lock."""
from datetime import timedelta
from unittest.mock import ANY, patch

from homeassistant.components.lock import (
    DOMAIN as LOCK_DOMAIN,
    SERVICE_LOCK,
    SERVICE_UNLOCK,
)
from homeassistant.const import ATTR_ENTITY_ID, STATE_LOCKED, STATE_UNLOCKED
from homeassistant.helpers import device_registry as dr, entity_registry as er
from homeassistant.util.dt import utcnow

from tests.common import async_fire_time_changed
from tests.components.freedompro.const import DEVICES_STATE

uid = "2WRRJR6RCZQZSND8VP0YTO3YXCSOFPKBMW8T51TU-LQ*2VAS3HTWINNZ5N6HVEIPDJ6NX85P2-AM-GSYWUCNPU0"


async def test_lock_get_state(hass, init_integration):
    """Test states of the lock."""
    init_integration
    registry = er.async_get(hass)
    registry_device = dr.async_get(hass)

    device = registry_device.async_get_device({("freedompro", uid)})
    assert device is not None
    assert device.identifiers == {("freedompro", uid)}
    assert device.manufacturer == "Freedompro"
    assert device.name == "lock"
    assert device.model == "lock"

    entity_id = "lock.lock"
    state = hass.states.get(entity_id)
    assert state
    assert state.state == STATE_UNLOCKED
    assert state.attributes.get("friendly_name") == "lock"

    entry = registry.async_get(entity_id)
    assert entry
    assert entry.unique_id == uid

    get_states_response = list(DEVICES_STATE)
    for state_response in get_states_response:
        if state_response["uid"] == uid:
            state_response["state"]["lock"] = 1
    with patch(
        "homeassistant.components.freedompro.get_states",
        return_value=get_states_response,
    ):
        async_fire_time_changed(hass, utcnow() + timedelta(hours=2))
        await hass.async_block_till_done()

        state = hass.states.get(entity_id)
        assert state
        assert state.attributes.get("friendly_name") == "lock"

        entry = registry.async_get(entity_id)
        assert entry
        assert entry.unique_id == uid

        assert state.state == STATE_LOCKED


async def test_lock_set_unlock(hass, init_integration):
    """Test set on of the lock."""
    init_integration
    registry = er.async_get(hass)

    entity_id = "lock.lock"
    state = hass.states.get(entity_id)
    assert state
    assert state.state == STATE_LOCKED
    assert state.attributes.get("friendly_name") == "lock"

    entry = registry.async_get(entity_id)
    assert entry
    assert entry.unique_id == uid

    with patch("homeassistant.components.freedompro.lock.put_state") as mock_put_state:
        assert await hass.services.async_call(
            LOCK_DOMAIN,
            SERVICE_UNLOCK,
            {ATTR_ENTITY_ID: [entity_id]},
            blocking=True,
        )
    mock_put_state.assert_called_once_with(ANY, ANY, ANY, '{"lock": 0}')

    await hass.async_block_till_done()
    state = hass.states.get(entity_id)
    assert state.state == STATE_LOCKED


async def test_lock_set_lock(hass, init_integration):
    """Test set on of the lock."""
    init_integration
    registry = er.async_get(hass)

    entity_id = "lock.lock"
    state = hass.states.get(entity_id)
    assert state
    assert state.state == STATE_LOCKED
    assert state.attributes.get("friendly_name") == "lock"

    entry = registry.async_get(entity_id)
    assert entry
    assert entry.unique_id == uid

    with patch("homeassistant.components.freedompro.lock.put_state") as mock_put_state:
        assert await hass.services.async_call(
            LOCK_DOMAIN,
            SERVICE_LOCK,
            {ATTR_ENTITY_ID: [entity_id]},
            blocking=True,
        )
    mock_put_state.assert_called_once_with(ANY, ANY, ANY, '{"lock": 1}')

    await hass.async_block_till_done()
    state = hass.states.get(entity_id)
    assert state.state == STATE_LOCKED
