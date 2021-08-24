"""Config flow for AMD GPU integration."""
import logging

import voluptuous as vol

from homeassistant import config_entries

from homeassistant.core import callback
import homeassistant.helpers.config_validation as cv

from . import find_resources_in_config_entry
from .const import (
    CONF_RESOURCES,
    DOMAIN,
    SENSOR_TYPES,
)

_LOGGER = logging.getLogger(__name__)


def _resource_schema_base(available_resources, selected_resources):
    """Resource selection schema."""

    known_available_resources = {
        sensor_id: sensor[0]
        for sensor_id, sensor in SENSOR_TYPES.items()
        if sensor_id in available_resources
    }

    return {
        vol.Required(CONF_RESOURCES, default=selected_resources): cv.multi_select(
            known_available_resources
        )
    }


class ConfigFlow(config_entries.ConfigFlow, domain=DOMAIN):
    """Handle a config flow for AMD GPU."""

    def __init__(self):
        self.gpu_config = {}
        self.available_resources = SENSOR_TYPES.keys()

    async def async_step_user(self, user_input=None):
        """Invoked when a user initiates a flow via the user interface."""
        if self._async_current_entries():
            return self.async_abort(reason="single_instance_allowed")

        if user_input is None:
            return self.async_show_form(
                step_id="user",
                data_schema=vol.Schema(
                    _resource_schema_base(self.available_resources, [])
                ),
            )
        self.gpu_config.update(user_input)
        return self.async_create_entry(title=DOMAIN, data=self.gpu_config)

    @staticmethod
    @callback
    def async_get_options_flow(config_entry):
        """Get the options flow for this handler."""
        return OptionsFlowHandler(config_entry)


class OptionsFlowHandler(config_entries.OptionsFlow):
    """Invoked when a user reconfigures via the user interface."""

    def __init__(self, config_entry: config_entries.ConfigEntry) -> None:
        self.config_entry = config_entry
        self.available_resources = SENSOR_TYPES.keys()

    async def async_step_init(self, user_input=None):
        """Manage the options."""
        if user_input is not None:
            return self.async_create_entry(title="", data=user_input)

        resources = find_resources_in_config_entry(self.config_entry)
        base_schema = _resource_schema_base(self.available_resources, resources)

        return self.async_show_form(step_id="init", data_schema=vol.Schema(base_schema))
