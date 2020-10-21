import pandas as pd
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


def compute_waiting_time(data_frame):
    """Compute the waiting time and service time from a sequence of job executions."""
    return pd.DataFrame([], columns=["compiler", "waiting time", "service time"])


def main():
    """Analysis the provided experiment results and quantify the effects of the factors"""

    # Parse arguments
    argument_parser = ArgumentParser()
    argument_parser.add_argument("-t", "--type", required=True, choices=["effects", "anova", "queue"], help="type of analysis")
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
    elif arguments.type == "queue":
        results = compute_waiting_time(data_frame)
    else:
        raise ValueError(f"Invalid analysis type: {arguments.type}")

    # Store results
    results.to_csv(arguments.output, index=False)
    print(results)


if __name__ == '__main__':
    main()
