"""The ha-pyamdgpuinfo component."""

from homeassistant.config_entries import ConfigEntry
from homeassistant.core import HomeAssistant

from .const import CONF_RESOURCES, DOMAIN, PLATFORMS


async def async_setup_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Set up AMD GPU from a config entry."""
    await hass.config_entries.async_forward_entry_setups(entry, PLATFORMS)
    return True


async def async_unload_entry(hass: HomeAssistant, entry: ConfigEntry) -> bool:
    """Unload a config entry."""
    return await hass.config_entries.async_unload_platforms(entry, PLATFORMS)


def find_resources_in_config_entry(config_entry):
    """Find the configured resources in the config entry."""
    if CONF_RESOURCES in config_entry.options:
        return config_entry.options[CONF_RESOURCES]
    return config_entry.data[CONF_RESOURCES]
