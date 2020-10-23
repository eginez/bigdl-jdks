import pandas as pd
import math
import numpy as np
import statsmodels.api as sm

from argparse import ArgumentParser
from statsmodels.formula.api import ols


def compute_effects(data_frame):
    """Compute the effect of the main factors."""

    # Prepare data
    factors = ["compiler", "nodes", "cores", "batch_size"]
    options = {factor: sorted(data_frame[factor].unique()) for factor in factors}
    effects = {factor: [0.0] for factor in factors}

    # Compute effects
    groups = data_frame.groupby(factors)
    for levels, group in groups:
        runtime = group["runtime"].mean()
        for factor, level in zip(factors, levels):
            effects[factor][0] += runtime * (2 * options[factor].index(level) - 1)

    return pd.DataFrame.from_dict(effects)


def perform_anova(data_frame):
    """Create an ANOVA table from the provided data."""
    model = ols("runtime ~ C(compiler)", data_frame).fit()
    return sm.stats.anova_lm(model, typ=1)


def perform_full_anova(data_frame):
    """Create an ANOVA table from the provided data."""
    data_frame = data_frame.groupby(["compiler", "nodes", "cores"]).tail(5)
    model = ols("runtime ~ C(compiler)*C(nodes)*C(cores)", data_frame).fit()
    return sm.stats.anova_lm(model, typ=1)


def compute_waiting_time(data_frame):
    """Compute the waiting time and service time from a sequence of job executions."""

    # Define trim function
    def trim(data):
        quarter = math.ceil(data.shape[0] / 4.0)
        return data[quarter:-quarter].mean()

    # Compute waiting and service times
    data_frame["waiting_time"] = data_frame["start_time"] - data_frame["arrival_time"]
    data_frame["service_time"] = data_frame["end_time"] - data_frame["start_time"]
    data_frame = data_frame.drop(columns=["arrival_time", "start_time", "end_time"], index=1)

    # Trim and average measurements
    groups = data_frame.groupby(["compiler", "nodes", "cores", "batch_size"])
    data_frame = groups.apply(func=trim)
    data_frame.rename(columns={"waiting_time": "mean_waiting_time", "service_time": "mean_service_time"}, inplace=True)

    return data_frame


def main():
    """Analysis the provided experiment results and quantify the effects of the factors"""

    # Parse arguments
    argument_parser = ArgumentParser()
    argument_parser.add_argument("-t", "--type", required=True, choices=["effects", "anova", "full-anova", "queue"], help="type of analysis")
    argument_parser.add_argument("-m", "--measurements", required=True, help="path to CSV file containing measurements")
    argument_parser.add_argument("-o", "--output", required=True, help="path to CSV output file")
    arguments = argument_parser.parse_args()

    # Load data
    data_frame = pd.read_csv(arguments.measurements)

    # Analyse data
    if arguments.type == "effects":
        results = compute_effects(data_frame)
    elif arguments.type == "anova":
        results = perform_anova(data_frame)
    elif arguments.type == "full-anova":
        results = perform_full_anova(data_frame)
    elif arguments.type == "queue":
        results = compute_waiting_time(data_frame)
    else:
        raise ValueError(f"Invalid analysis type: {arguments.type}")

    # Store results
    results.to_csv(arguments.output)


if __name__ == '__main__':
    main()
