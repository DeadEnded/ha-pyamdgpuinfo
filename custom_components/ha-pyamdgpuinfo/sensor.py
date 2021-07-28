"""
Support for AMD GPU sensors.

For more details about this platform, please refer to the documentation at
https://github.com/DeadEnded/ha-pyamdgpuinfo/
"""
import logging
import voluptuous as vol
import pyamdgpuinfo

from homeassistant.components.sensor import PLATFORM_SCHEMA, SensorEntity
import homeassistant.helpers.config_validation as cv
from homeassistant.const import (
    CONF_RESOURCES,
    DATA_GIBIBYTES,
    DATA_MEBIBYTES,
    PERCENTAGE,
    TEMP_CELSIUS,
    POWER_WATT,
    ATTR_VOLTAGE,
)

_LOGGER = logging.getLogger(__name__)

# Schema: [name, unit of measurement, icon, device class, flag if mandatory arg]
SENSOR_TYPES = {
    "gpu_temperature": ["GPU temperature", TEMP_CELSIUS, "mdi:thermometer", None, False, ],
    "vram_size": ["VRAM Size", DATA_MEBIBYTES, "mdi:memory", None, False],
    "vram_usage": ["VRAM Usage", DATA_MEBIBYTES, "mdi:memory", None, False],
    "vram_percent": ["VRAM Usage (percent)", PERCENTAGE, "mdi:memory", None, False],
    "gtt_size": ["GTT Size", DATA_MEBIBYTES, "mdi:memory", None, False],
    "gtt_usage": ["GTT Usage", DATA_MEBIBYTES, "mdi:memory", None, False],
    "gtt_percent": ["GTT Usage (percent)", PERCENTAGE, "mdi:memory", None, False],
    "sclk_max": ["Shader Clock Max", "GHz", "mdi:chip", None, False],
    "sclk_usage": ["Shader Clock Usage", "GHz", "mdi:chip", None, False],
    "sclk_percent": ["Shader Clock Usage (percent)", PERCENTAGE, "mdi:chip", None, False],
    "mclk_max": ["Memory Clock Max", "GHz", "mdi:chip", None, False],
    "mclk_usage": ["Memory Clock Usage", "GHz", "mdi:chip", None, False],
    "mclk_percent": ["Memory Clock Usage (percent)", PERCENTAGE, "mdi:chip", None, False],
    "query_load": ["Overall GPU load", PERCENTAGE, "mdi:chip", None, False],
    "query_power": ["Power consumption", POWER_WATT, "mdi:lightning-bolt", None, False],
    "query_northbridge_voltage": ["Northbrige Voltage", ATTR_VOLTAGE, "mdi:lightning-bolt", None, False],
    "query_graphics_voltage": ["Graphics Voltage", ATTR_VOLTAGE, "mdi:lightning-bolt", None, False],
    "texture_addresser": ["Texture Addresser (percent)", PERCENTAGE, "mdi:chip", None, False],
    "shader_export": ["Shader Export (percent)", PERCENTAGE, "mdi:chip", None, False],
    "shader_interpolator": ["Shader Interpolator (percent)", PERCENTAGE, "mdi:chip", None, False],
    "primitive_assembly": ["Primitive Assembly (percent)", PERCENTAGE, "mdi:chip", None, False],
    "depth_block": ["Depth Block (percent)", PERCENTAGE, "mdi:chip", None, False],
    "colour_block": ["Colour Block (percent)", PERCENTAGE, "mdi:chip", None, False],
    "graphics_pipe": ["GPU use (percent)", PERCENTAGE, "mdi:chip", None, False]
}

# Validation of the user's configuration
PLATFORM_SCHEMA = PLATFORM_SCHEMA.extend(
    {
        vol.Optional(CONF_RESOURCES, default=[]): vol.All(
            cv.ensure_list, [vol.In(SENSOR_TYPES)]
        ),
    }
)

# Define the GPU index to be queried
first_gpu = pyamdgpuinfo.get_gpu(0)


async def async_setup_platform(hass, config, async_add_entities, discovery_info=None):
    """Set up the system monitor sensors."""
    try:
        first_gpu.stop_utilisation_polling()
    except RuntimeError:
        _LOGGER.debug("Polling is not running")

    try:
        first_gpu.start_utilisation_polling()
    except:
        _LOGGER.debug("Something stopped polling from starting")
    else:
        _LOGGER.debug("Polling started")

    entities = []

    for resource in config[CONF_RESOURCES]:
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
            self._state = pyamdgpuinfo.get_gpu(0).query_temperature()
        elif self.type == "vram_size":
            self._state = round(pyamdgpuinfo.get_gpu(0).memory_info.get("vram_size") / 1024 ** 2, 1)
        elif self.type == "vram_usage":
            self._state = round(pyamdgpuinfo.get_gpu(0).query_vram_usage() / 1024 ** 2, 1)
        elif self.type == "vram_percent":
            self._state = round((pyamdgpuinfo.get_gpu(0).query_vram_usage() / 1024 ** 2) / (pyamdgpuinfo.get_gpu(0).memory_info.get("vram_size") / 1024 ** 2), 3) * 100
        elif self.type == "gtt_size":
            self._state = round(pyamdgpuinfo.get_gpu(0).memory_info.get("gtt_size") / 1024 ** 2, 1)
        elif self.type == "gtt_usage":
            self._state = round(pyamdgpuinfo.get_gpu(0).query_gtt_usage() / 1024 ** 2, 1)
        elif self.type == "gtt_percent":
            self._state = round((pyamdgpuinfo.get_gpu(0).query_gtt_usage() / 1024 ** 2) / (pyamdgpuinfo.get_gpu(0).memory_info.get("gtt_size") / 1024 ** 2), 3) * 100
        elif self.type == "sclk_max":
            self._state = round(pyamdgpuinfo.get_gpu(0).query_max_clocks().get("sclk_max") / 1000 ** 3, 2)
        elif self.type == "sclk_usage":
            self._state = round(pyamdgpuinfo.get_gpu(0).query_sclk() / 1000 ** 3, 2)
        elif self.type == "sclk_percent":
            self._state = round((pyamdgpuinfo.get_gpu(0).query_sclk() / 1000 ** 3) / (pyamdgpuinfo.get_gpu(0).query_max_clocks().get("sclk_max") / 1000 ** 3), 4) * 100
        elif self.type == "mclk_max":
            self._state = round(pyamdgpuinfo.get_gpu(0).query_max_clocks().get("mclk_max") / 1000 ** 3, 2)
        elif self.type == "mclk_usage":
            self._state = round(pyamdgpuinfo.get_gpu(0).query_mclk() / 1000 ** 3, 2)
        elif self.type == "mclk_percent":
            self._state = round((pyamdgpuinfo.get_gpu(0).query_mclk() / 1000 ** 3) / (pyamdgpuinfo.get_gpu(0).query_max_clocks().get("mclk_max") / 1000 ** 3), 4) * 100
        elif self.type == "query_load":
            self._state = round(pyamdgpuinfo.get_gpu(0).query_load() * 100, 2)
        elif self.type == "query_power":
            self._state = pyamdgpuinfo.get_gpu(0).query_power()
        elif self.type == "query_northbridge_voltage":
            self._state = pyamdgpuinfo.get_gpu(0).query_northbridge_voltage()
        elif self.type == "query_graphics_voltage":
            self._state = pyamdgpuinfo.get_gpu(0).query_graphics_voltage()
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
