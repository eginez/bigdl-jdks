# Analysis

...

## Package installation

All required Python packages are listed in the file: `requirements.txt`. These can be installed via the command:

```shell script
pip3 install -r requirements.txt
```

## Collecting measurement data

Collecting data from the Google Cloud Platform requires a user to provide proper authentication. The simplest approach is to install the `gcloud` utility and use that to authenticate.
```shell script
sudo snap install gcloud
gcloud auth login
```

After install and authenticating using the gcloud utility, it is possible to retrieve the measurement data using the provided python script.
```shell script
python3 collect.py -b qpecs-output -o measurements.csv
```

## Analysing experiment results

To analyse the experiment results, we perform ANOVA analysis and compute the main effects of the factors experimented with. The following command should suffice.

```shell script
python3 analyse.py -m measurements.csv
```
