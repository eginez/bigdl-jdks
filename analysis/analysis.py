import pandas as pd
import numpy as np

from argparse import ArgumentParser
from pyDOE import fullfact, ff2n, fracfact


def main():

    argument_parser = ArgumentParser()
    argument_parser.add_argument("-i", "--input", required=True, help="Path to input CSV file")
    argument_parser.add_argument("-o", "--output", required=False, help="Path to output CSV file")
    arguments = argument_parser.parse_args()

    output = arguments.output if arguments.output else "console"
    print(f"Analysing \"{arguments.input}\" and outputting to {output}")


if __name__ == '__main__':
    main()
