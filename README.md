# drone-rf

You will need `hackrf` and `plotsweep`

## Example Usage

```
hackrf_sweep -f 2430:2450 -l 32 -g 32 -w 100000 > sweep.csv
plotsweep sweep.csv  sweep.png --power-min -55 --power-max -30
python sweep-check.py sweep.png
```

This was tested against a Snaptain Mini, monitoring the frequencies produced at 2443 MHz. The goal is to map power levels against distances, which should have an inverse square relationship per Friis' transmission equation.