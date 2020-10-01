# Design

...

## Package installation

All required Python packages are listed in the file: `requirements.txt`. These can be installed via the command:

```
pip3 install -r requirements.txt
```

## Generating experiment configurations

The Python script `design.py` provides a way to generate both full and fractional factorial designs. It converts a JSON configuration file, containing the experiment factors and their levels, into a CSV file containing the optimal experiment configurations. Generating the design is done via the command:

```
python3 design.py -t [full|frac] -f path/to/factors.json -o path/to/output.csv
```
