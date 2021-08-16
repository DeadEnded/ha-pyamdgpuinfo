"""
Support for AMD GPU sensors.

For more details about this platform, please refer to the documentation at
https://github.com/DeadEnded/ha-pyamdgpuinfo/
"""
import logging
from time import sleep
import voluptuous as vol
import pyamdgpuinfo

from homeassistant.components.sensor import SensorEntity#, PLATFORM_SCHEMA
import homeassistant.helpers.config_validation as cv
from .const import (
    CONF_RESOURCES,
    DEVICE_ID,
    DOMAIN,
    MANUFACTURER,
    MODEL,
    NAME,
    SENSOR_TYPES,
)

_LOGGER = logging.getLogger(__name__)


# # Validation of the user's configuration
# PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
#     {
#         vol.Optional(CONF_RESOURCES, default=[]): vol.All(
#             cv.ensure_list, [vol.In(SENSOR_TYPES)]
#         ),
#     }
# )

# Define the GPU index to be queried
first_gpu = pyamdgpuinfo.get_gpu(0)


async def async_setup_entry(hass, config_entry, async_add_entities):
    """Set up the system monitor sensors."""
    try:
        first_gpu.stop_utilisation_polling()
    except RuntimeError:
        _LOGGER.debug("Polling is not running")

    try:
        first_gpu.start_utilisation_polling()
        sleep(1)
    except:
        _LOGGER.debug("Something stopped polling from starting")
    else:
        _LOGGER.debug("Polling started")

    if CONF_RESOURCES in config_entry.options:
        resources = config_entry.options[CONF_RESOURCES]
    else:
        resources = config_entry.data[CONF_RESOURCES]

    entities = []
    for resource in resources:
        entities.append(AMDGPUSensor(resource))

    async_add_entities(entities, True)


class AMDGPUSensor(SensorEntity):
    """Implementation of a pyamdgpuinfo sensor."""

    def __init__(self, sensor_type):
        """Initialize the sensor."""
        self._name = SENSOR_TYPES[sensor_type][0]
        self._unique_id = sensor_type
        self.type = sensor_type
        self._state = None
        self._unit_of_measurement = SENSOR_TYPES[sensor_type][1]
        self._available = True

    @property
    def name(self):
        """Return the name of the sensor."""
        return self._name.rstrip()

    @property
    def unique_id(self):
        """Return the unique ID."""
        return self._unique_id

    @property
    def device_info(self):
        """Get device information."""
        return {
            "identifiers": {(DOMAIN, DEVICE_ID)},
            "name": NAME,
            "model": MODEL,
            "manufacturer": MANUFACTURER,
        }

    @property
    def device_class(self):
        """Return the class of this sensor."""
        return SENSOR_TYPES[self.type][3]

    @property
    def icon(self):
        """Icon to use in the frontend, if any."""
        return SENSOR_TYPES[self.type][2]

    @property
    def state(self):
        """Return the state of the device."""
        return self._state

    @property
    def unit_of_measurement(self):
        """Return the unit of measurement of this entity, if any."""
        return self._unit_of_measurement

    @property
    def available(self):
        """Return True if entity is available."""
        return self._available

    def update(self):
        """Get the latest system information."""

        if self.type == "gpu_temperature":
            self._state = first_gpu.query_temperature()
        elif self.type == "vram_size":
            self._state = round(first_gpu.memory_info.get("vram_size") / 1024 ** 2, 1)
        elif self.type == "vram_usage":
            self._state = round(first_gpu.query_vram_usage() / 1024 ** 2, 1)
        elif self.type == "vram_percent":
            self._state = round((first_gpu.query_vram_usage() / 1024 ** 2) / (pyamdgpuinfo.get_gpu(0).memory_info.get("vram_size") / 1024 ** 2), 3) * 100
        elif self.type == "gtt_size":
            self._state = round(first_gpu.memory_info.get("gtt_size") / 1024 ** 2, 1)
        elif self.type == "gtt_usage":
            self._state = round(first_gpu.query_gtt_usage() / 1024 ** 2, 1)
        elif self.type == "gtt_percent":
            self._state = round((first_gpu.query_gtt_usage() / 1024 ** 2) / (pyamdgpuinfo.get_gpu(0).memory_info.get("gtt_size") / 1024 ** 2), 3) * 100
        elif self.type == "sclk_max":
            self._state = round(first_gpu.query_max_clocks().get("sclk_max") / 1000 ** 3, 2)
        elif self.type == "sclk_usage":
            self._state = round(first_gpu.query_sclk() / 1000 ** 3, 2)
        elif self.type == "sclk_percent":
            self._state = round((first_gpu.query_sclk() / 1000 ** 3) / (pyamdgpuinfo.get_gpu(0).query_max_clocks().get("sclk_max") / 1000 ** 3), 4) * 100
        elif self.type == "mclk_max":
            self._state = round(first_gpu.query_max_clocks().get("mclk_max") / 1000 ** 3, 2)
        elif self.type == "mclk_usage":
            self._state = round(first_gpu.query_mclk() / 1000 ** 3, 2)
        elif self.type == "mclk_percent":
            self._state = round((first_gpu.query_mclk() / 1000 ** 3) / (pyamdgpuinfo.get_gpu(0).query_max_clocks().get("mclk_max") / 1000 ** 3), 4) * 100
        elif self.type == "query_load":
            self._state = round(first_gpu.query_load() * 100, 2)
        elif self.type == "query_power":
            self._state = first_gpu.query_power()
        elif self.type == "query_northbridge_voltage":
            self._state = first_gpu.query_northbridge_voltage()
        elif self.type == "query_graphics_voltage":
            self._state = first_gpu.query_graphics_voltage()
        elif self.type == "texture_addresser":
            self._state = first_gpu.query_utilisation().get("texture_addresser") * 100
        elif self.type == "shader_export":
            self._state = first_gpu.query_utilisation().get("shader_export") * 100
        elif self.type == "shader_interpolator":
            self._state = first_gpu.query_utilisation().get("shader_interpolator") * 100
        elif self.type == "primitive_assembly":
            self._state = first_gpu.query_utilisation().get("primitive_assembly") * 100
        elif self.type == "depth_block":
            self._state = first_gpu.query_utilisation().get("depth_block") * 100
        elif self.type == "colour_block":
            self._state = first_gpu.query_utilisation().get("colour_block") * 100
        elif self.type == "graphics_pipe":
            self._state = first_gpu.query_utilisation().get("graphics_pipe") * 100
