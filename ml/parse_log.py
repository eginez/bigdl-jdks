import pandas as pd
import re

from argparse import ArgumentParser


def main():
    """Collect the inter-arrival times and service times from a log file and store them in a CSV file."""

    # Parse arguments
    argument_parser = ArgumentParser()
    argument_parser.add_argument("-l", "--log", required=True, help="path to log file to be parsed")
    argument_parser.add_argument("-m", "--measurements", required=True, help="path to measurements file to be generated")
    arguments = argument_parser.parse_args()

    # Retrieve measurements from log
    rows = []
    with open(arguments.log) as log_file:
        content = "".join(log_file.readlines())
        for match in re.finditer(".*,([\\d.])+,([\\d.]+),([\\d.]+).*", content):
            arrival_time = float(match.group(1))
            start_time = float(match.group(2))
            end_time = float(match.group(3))
            rows.append([arrival_time, start_time, end_time])

    # Create and store dataframe
    data_frame = pd.DataFrame(rows, columns=["arrival time", "start time", "end time"])
    data_frame.to_csv(arguments.measurements)


if __name__ == '__main__':
    main()
