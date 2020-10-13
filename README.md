# FACT Plug-in: dtb_finder 

A [FACT](https://github.com/fkie-cad/FACT_core) analysis plug-in for extracting Flattend Device Trees (.dtb files) from the firmware.

### Add Plugin to your project:
```sh
$ git submodule add https://gitlab.sba-research.org/autohoney-i-iot/processor-database/dtb_finder.git src/plugins/analysis/dtb_finder
$ ./src/install.py -B
``` 

If you add more than one additional plug-in, ```./install.py -B``` must be run just once after you added the last plug-in.

In the "restaccess" folder there is an example python script to access and save the .dtb files using FACT's REST API.

In the "test_files" folder are firmwares/files which include one or more Flattened Device Trees to test the plugin.