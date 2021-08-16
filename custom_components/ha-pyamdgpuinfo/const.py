""" The AMD GPU component."""

from homeassistant.components.sensor import (
    DEVICE_CLASS_POWER,
    DEVICE_CLASS_TEMPERATURE,
    DEVICE_CLASS_VOLTAGE,
)

from homeassistant.const import (
    CONF_RESOURCES,
    DATA_MEBIBYTES,
    PERCENTAGE,
    TEMP_CELSIUS,
    POWER_WATT,
    ATTR_VOLTAGE,
)

DEVICE_ID = "0"
DOMAIN = "ha_pyamdgpuinfo"
MANUFACTURER = "AMD"
MODEL = "Unknown"
NAME = "AMD GPU"

PLATFORMS = ["sensor"]

# Schema: [name, unit of measurement, icon, device class, flag if mandatory arg]
SENSOR_TYPES = {
    "gpu_temperature": ["GPU temperature", TEMP_CELSIUS, "mdi:thermometer", DEVICE_CLASS_TEMPERATURE, False, ],
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
    "query_power": ["Power consumption", POWER_WATT, "mdi:lightning-bolt", DEVICE_CLASS_POWER, False],
    "query_northbridge_voltage": ["Northbrige Voltage", ATTR_VOLTAGE, "mdi:lightning-bolt", DEVICE_CLASS_VOLTAGE, False],
    "query_graphics_voltage": ["Graphics Voltage", ATTR_VOLTAGE, "mdi:lightning-bolt", DEVICE_CLASS_VOLTAGE, False],
    "texture_addresser": ["Texture Addresser (percent)", PERCENTAGE, "mdi:chip", None, False],
    "shader_export": ["Shader Export (percent)", PERCENTAGE, "mdi:chip", None, False],
    "shader_interpolator": ["Shader Interpolator (percent)", PERCENTAGE, "mdi:chip", None, False],
    "primitive_assembly": ["Primitive Assembly (percent)", PERCENTAGE, "mdi:chip", None, False],
    "depth_block": ["Depth Block (percent)", PERCENTAGE, "mdi:chip", None, False],
    "colour_block": ["Colour Block (percent)", PERCENTAGE, "mdi:chip", None, False],
    "graphics_pipe": ["GPU use (percent)", PERCENTAGE, "mdi:chip", None, False]
}
