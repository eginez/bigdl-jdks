import json
import pandas as pd

from argparse import ArgumentParser
from pyDOE2 import fullfact, ff2n, fracfact_by_res


def frac_by_max_res(factor_count, target_resolution=6):
    """Generate fractional factorial design sign table with maximum resolution"""
    try:
        if target_resolution >= 3:
            return fracfact_by_res(factor_count, target_resolution)
        return ff2n(factor_count)
    except ValueError:
        return frac_by_max_res(factor_count, target_resolution - 1)


def min_max(levels):
    """Compute minimum and maximum of given levels"""
    if not levels:
        raise ValueError("Cannot determine minimum value of empty list")
    if type(levels[0]) == str:
        return 0, -1
    return levels.index(min(levels)), levels.index(max(levels))


def generate_frac(factors):
    """Generate a fractional factorial design with maximum resolution"""

    # Generate sign table
    design = frac_by_max_res(len(factors))

    # Replace signs with min and max indices
    min_indices, max_indices = zip(*[min_max(levels) for _, levels in factors.items()])
    for i in range(len(design)):
        for j in range(len(design[i])):
            if design[i][j] < 0:
                design[i][j] = min_indices[j]
            else:
                design[i][j] = max_indices[j]

    return design


def generate_full(factors):
    """Generate a full factorial design"""
    levels = [len(values) for _, values in factors.items()]
    design = fullfact(levels)
    return design


def main():
    """Generate experiment configurations from the provided factors and store them in a CSV file"""

    # Parse arguments
    argument_parser = ArgumentParser()
    argument_parser.add_argument("-t", "--type", metavar="TYPE", choices=["full", "frac"], required=True, help="type of experiment design")
    argument_parser.add_argument("-f", "--factors", metavar="PATH", required=True, help="path to JSON configuration file")
    argument_parser.add_argument("-o", "--output", metavar="PATH", required=True, help="path to CSV output file")
    arguments = argument_parser.parse_args()

    # Load factors
    with open(arguments.factors) as file:
        factors = json.load(file)

    # Generate design
    if "frac" in arguments.type:
        design = generate_frac(factors)
    elif "full" in arguments.type:
        design = generate_full(factors)
    else:
        raise ValueError(f"Invalid design type: {arguments.type}")

    # Convert indices to integers
    design = [map(int, indices) for indices in design]

    # Generate configurations
    configurations = []
    for indices in design:
        configuration = []
        for factor, index in zip(factors, indices):
            configuration.append(factors[factor][index])
        configurations.append(configuration)

    # Store configurations
    data_frame = pd.DataFrame(data=configurations, columns=list(map(str.lower, factors.keys())))
    data_frame.to_csv(arguments.output, index_label="index")


if __name__ == '__main__':
    main()
