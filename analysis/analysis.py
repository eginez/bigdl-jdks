import json
import pandas as pd

from argparse import ArgumentParser


def main():

    # Parse arguments
    argument_parser = ArgumentParser()
    argument_parser.add_argument("-d", "--design", required=True, help="Design JSON input file")
    argument_parser.add_argument("-m", "--measurements", required=True, help="Measurements CSV input file")
    argument_parser.add_argument("-o", "--output", required=False, help="ANOVA output file")
    arguments = argument_parser.parse_args()

    # Print welcome message
    output = arguments.output if arguments.output else "console"
    print(f"Analysing \"{arguments.input}\" and outputting to {output}")

    # Load design and measurements
    with open(arguments.design) as file:
        design = json.load(file)
    measurements = pd.read_csv(arguments.measurements)

    # ...

    # Store ANOVA table
    with open(arguments.output) as file:
        pass


if __name__ == '__main__':
    main()
