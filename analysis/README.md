# Analysis

...

## Package installation

All required Python packages are listed in the file: `requirements.txt`. These can be installed via the command:

```
pip3 install -r requirements.txt
```

## Analysing experiment results

The Python script `analyse.py` provides a way to analyse experiment results. It converts a CSV file, containing the experiment results, into a CSV file containing the effect and significance of each factor. Analysing the experiments is done via the command:

```
python3 analyse.py -o path/to/effects.csv path/to/results.csv
```
