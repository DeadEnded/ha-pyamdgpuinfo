[![hacs_badge](https://img.shields.io/badge/HACS-Custom-orange.svg)](https://github.com/custom-components/hacs)

# ha-pyamdgpuinfo

Home Asisstant Custom Component for AMDGPU sensors.<br>
This component is built from the [pyamdgpuinfo](https://github.com/mark9064/pyamdgpuinfo).<br>

## Pass GPU to Container

For this component to work, you need to pass your GPU through to the HA container.<br>
This can be done by adding the following to your docker run command:<br>

```
--device=/dev/dri:/dev/dri
```

Or for docker compose:<br>
```
devices:
  - /dev/dri:/dev/dri
```

## Installation

### Manual

Copy this folder to `<config_dir>/custom_components/ha-pyamdgpuinfo/`.

### HACS

Add the following as a custom component in HACS:

`https://github.com/DeadEnded/ha-pyamdgpuinfo`

## Usage
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

## Runtime Error

If you get an error like:<br>
`RuntimeError: Unknown query failure (an amdgpu call failed). This query may not be supported for this GPU.`<br>
then it is likely your GPU does not suppor that sensor.<br>
Simply remove it from your `configuration.yaml` file and restart.
