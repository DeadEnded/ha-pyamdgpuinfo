# ha-pyamdgpuinfo

Home Asisstant Custom Component for AMDGPU sensors.<br>
This component is built from the [pyamdgpuinfo](https://github.com/mark9064/pyamdgpuinfo).<br>

## Installation

### Manual

Copy this folder to `<config_dir>/custom_components/ha-pyamdgpuinfo/`.

### HACS

Add the following as a custom component in HACS:

`https://github.com/DeadEnded/ha-pyamdgpuinfo`

## Configuration.yaml
Add the following entry in your `configuration.yaml`:

```yaml
sensor:
  # Full list of sensors - trim to your needs
  - platform: ha-pyamdgpuinfo
    resources:
      - gpu_temperature
      - vram_size
      - vram_usage
      - vram_percent
      - gtt_size
      - gtt_usage
      - gtt_percent
      - sclk_max
      - sclk_usage
      - sclk_percent
      - mclk_max
      - mclk_usage
      - mclk_percent
      - query_load
      - query_power
      - query_northbridge_voltage
      - query_graphics_voltage
      - texture_addresser
      - shader_export
      - shader_interpolator
      - primitive_assembly
      - depth_block
      - colour_block
      - graphics_pipe
```
