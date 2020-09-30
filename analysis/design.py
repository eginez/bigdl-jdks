import json

from argparse import ArgumentParser
from pyDOE import fullfact, fracfact


def main():

    # Parse arguments
    argument_parser = ArgumentParser()
    argument_parser.add_argument("-t", "--type", required=True, help="Experiment design type")
    argument_parser.add_argument("-f", "--factors", required=True, help="Factors JSON config file")
    argument_parser.add_argument("-o", "--output", required=True, help="Design JSON output file")
    arguments = argument_parser.parse_args()

    # Print welcome message
    output = arguments.output if arguments.output else "console"
    print(f"Generating \"{arguments.type}\" and outputting to {output}")

    # Validate type
    options = ["fractional", "factorial"]
    if arguments.type not in options:
        raise ValueError(f"Invalid type: {arguments.type}")

    # Load factors
    with open(arguments.factors) as file:
        factors = json.load(file)

    # Generate experiments
    if "full" in arguments.type:
        experiments = []
    elif "frac" in arguments.type:
        experiments = []
    else:
        raise ValueError(f"Unsupported experiment design type: {arguments.type}")

    # Store experiment configurations
    with open(arguments.output) as file:
        pass


if __name__ == '__main__':
    main()
