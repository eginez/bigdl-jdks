import pandas as pd
import researchpy as rp
import statsmodels.api as sm

from argparse import ArgumentParser
from statsmodels.formula.api import ols


def perform_anova(data_frame):
    """Create an ANOVA table from the provided data."""

    # Create model
    model = ols("runtime ~ C(compiler)*C(nodes)*C(cores)*C(batch_size)", data_frame).fit()

    # Review model
    print("Model Significance")
    print(f"F({model.df_model: .0f},{model.df_resid: .0f}) = {model.fvalue: .3f}")
    print(f"p(p = {model.f_pvalue: .4f})")
    print()
    print("Model Summary")
    print(model.summary())
    print()

    # Create ANOVA table
    table = sm.stats.anova_lm(model, typ=1)

    # Print ANOVA table
    print("ANOVA table")
    print(table)
    print()


def compute_main_effects(data_frame):
    """Compute the effect of the main factors."""

    # Summarise data
    print("Data Summary")
    print(rp.summary_cont(data_frame.groupby(["compiler", "nodes", "cores", "batch_size"]))["runtime"])
    print()

    # Compute effects
    # ...


def main():
    """Analysis the provided experiment results and quantify the effects of the factors"""

    # Parse arguments
    argument_parser = ArgumentParser()
    argument_parser.add_argument("-t", "--type", required=True, choices=["anova", "effect"], help="type of analysis")
    argument_parser.add_argument("-m", "--measurements", required=True, help="path to CSV file containing measurements")
    arguments = argument_parser.parse_args()

    # Load data
    data_frame = pd.read_csv(arguments.measurements)

    # Analyse data
    if arguments.type == "anova":
        perform_anova(data_frame)
    elif arguments.type == "effect":
        compute_main_effects(data_frame)
    else:
        raise ValueError(f"Invalid analysis type: {arguments.type}")


if __name__ == '__main__':
    main()
