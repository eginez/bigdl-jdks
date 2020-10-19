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
    inter_arrival_times = []
    service_times = []
    with open(arguments.log) as log_file:
        content = "".join(log_file.readlines())
        for match in re.finditer(".*Waiting ([\\d.]+) seconds for new job.*", content):
            inter_arrival_time = float(match.group(1))
            inter_arrival_times.append(inter_arrival_time)
        for match in re.finditer(".*ended with status.*,[\\d.]+,([\\d.]+),([\\d.]+)\n.*", content):
            start_time = float(match.group(1))
            end_time = float(match.group(2))
            service_time = end_time - start_time
            service_times.append(service_time)

    # Create and store dataframe
    data = list(zip(inter_arrival_times, service_times))
    data_frame = pd.DataFrame(data, columns=["inter-arrival time", "service time"])
    data_frame.to_csv(arguments.measurements)


if __name__ == '__main__':
    main()
