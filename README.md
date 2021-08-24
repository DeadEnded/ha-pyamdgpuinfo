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

Add the following as a Custom Integration Repository in HACS:

`https://github.com/DeadEnded/ha-pyamdgpuinfo`

![image](https://github.com/DeadEnded/ha-pyamdgpuinfo/raw/config-flow/images/HACS-Add-Repository.png)

After you have added the custom repository you should see it as a new repository in the integrations screen:

![image](https://github.com/DeadEnded/ha-pyamdgpuinfo/raw/config-flow/images/HACS-New-Integration.png)


## Usage
Once the custom integration and pyamdgpuinfo wheel have been installed, you can install the component from the `Configuration - Integrations` screen:<br>
Add a new integration, and search for `AMD`:

![image](https://github.com/DeadEnded/ha-pyamdgpuinfo/raw/config-flow/images/Add-Integration.png)

Select `AMD GPU Info` and in the next screen select the sensors you want to add to Home Assistant:

![image](https://github.com/DeadEnded/ha-pyamdgpuinfo/raw/config-flow/images/Select-Sensors.png)

Once you have selected the sensors you want, click `Submit` and in a few seconds the new integration will be ready!

![image](https://github.com/DeadEnded/ha-pyamdgpuinfo/raw/config-flow/images/Integration-Added.png)

## Runtime Error

If you get an error like:<br>
`RuntimeError: Unknown query failure (an amdgpu call failed). This query may not be supported for this GPU.`<br>
then it is likely your GPU does not suppor that sensor.<br>
Simply click the `Configure` button on the integration, change your sensor selection, and click `Submit`.<br>
After changing the configuration, click the three dots on the bottom right of the integration, and select `Reload` to update Home Assistant with the new sensor selection.
