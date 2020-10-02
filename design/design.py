import json
import numpy as np
import pandas as pd

from argparse import ArgumentParser
from pyDOE2 import fullfact, ff2n, fracfact_by_res


def generate_full(factors):
    """Generate a full factorial design"""

    # Compute the number of levels
    levels = [len(values) for _, values in factors.items()]

    # Perform full factorial design
    design = fullfact(levels)

    # Convert indices to integers
    design = [map(int, indices) for indices in design]

    return design


def min_max(levels):
    """Compute the minimum and maximum of the given levels"""
    if not levels:
        raise ValueError("Cannot determine minimum value of empty list")
    if type(levels[0]) == str:
        return 0, -1
    return levels.index(min(levels)), levels.index(max(levels))


def generate_frac(factors):
    """Generate a fractional factorial design with the highest resolution possible"""

    # TODO: Exclude categorical factors from the fractional design.

    # Compute the number of factors
    n = len(factors)

    # Perform fractional factorial design with the greatest possible resolution
    design = None
    for resolution in [6, 5, 4, 3]:
        try:
            design = fracfact_by_res(n, resolution)
        except ValueError:
            continue

    # Perform full fractional if none of the target resolutions can be achieved
    if design is None:
        design = ff2n(n)

    # Normalize the design such that it corresponds to level indices
    min_indices, max_indices = zip(*[min_max(levels) for _, levels in factors.items()])
    for i in range(len(design)):
        for j in range(len(design[i])):
            if design[i][j] < 0:
                design[i][j] = min_indices[j]
            else:
                design[i][j] = max_indices[j]

    # Convert indices to integers
    design = [map(int, indices) for indices in design]

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
    if "full" in arguments.type:
        design = generate_full(factors)
    elif "frac" in arguments.type:
        design = generate_frac(factors)
    else:
        raise ValueError(f"Invalid design type: {arguments.type}")

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
