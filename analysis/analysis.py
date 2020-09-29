import pandas as pd
import numpy as np

from argparse import ArgumentParser
from pyDOE import fullfact, ff2n, fracfact


def main():

    argument_parser = ArgumentParser()
    argument_parser.add_argument("-i", "--input", required=True, help="Path to input CSV file")
    argument_parser.add_argument("-o", "--output", required=False, help="Path to output CSV file")
    arguments = argument_parser.parse_args()

    message = f"Analysing \"{arguments.input}\" and outputting to "
    if arguments.output:
        message += f"\"{arguments.output}\""
    else:
        message += "console"
    message += "."
    print(message)


if __name__ == '__main__':
    main()
