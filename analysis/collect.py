import pandas as pd
import re

from argparse import ArgumentParser
from google.cloud import storage


def parse_individual_jobs(blobs, folder):
    """Parse blobs as individual job measurements."""

    rows = []
    for blob in blobs:
        name = blob.name
        name_match = re.match(f"{folder}/([^-]+)-([^-]+)-([^-]+)-([^-]+)-.*", name)
        if name_match:
            compiler = name_match.group(1)
            nodes = int(name_match.group(2))
            cores = int(name_match.group(3))
            batch_size = int(name_match.group(4))

            data = blob.download_as_text()
            data_match = re.match("[^\\d]*(\\d+\\.\\d+)[^\\d]*(\\d+\\.\\d+)[^\\d]*", data)
            if data_match:
                runtime = float(data_match.group(1))
                accuracy = float(data_match.group(2))

                rows.append([compiler, nodes, cores, batch_size, runtime, accuracy])

    return pd.DataFrame(rows, columns=["compiler", "nodes", "cores", "batch_size", "runtime", "accuracy"])


def parse_job_sequences(blobs, folder):
    """Parse blobs as job sequence measurements."""

    rows = []
    for blob in blobs:

        name_match = re.match(f"{folder}/([^-]+)-([^-]+)-([^-]+)-([^-]+)-.*", blob.name)
        if name_match:
            compiler = name_match.group(1)
            nodes = int(name_match.group(2))
            cores = int(name_match.group(3))
            batch_size = int(name_match.group(4))

            data = blob.download_as_text()
            data_matches = re.finditer("[^\\d]*(\\d+\\.\\d+)[^\\d]*(\\d+\\.\\d+)[^\\d]*(\\d+\\.\\d+)[^\\d]*", data)
            for data_match in data_matches:
                arrival_time = float(data_match.group(1))
                start_time = float(data_match.group(2))
                end_time = float(data_match.group(2))
                rows.append([compiler, nodes, cores, batch_size, arrival_time, start_time, end_time])

    return pd.DataFrame(rows, columns=["compiler", "nodes", "cores", "batch_size", "arrival_time", "start_time", "end_time"])


def main():
    """Collect the data stored on the Google Cloud Platform and convert it to a CSV file."""

    # Parse arguments
    argument_parser = ArgumentParser()
    argument_parser.add_argument("-b", "--bucket", required=True, help="bucket from which to retrieve measurements")
    argument_parser.add_argument("-f", "--folder", required=True, help="folder from which to retrieve measurements")
    argument_parser.add_argument("-t", "--type", required=True, choices=["individual", "sequence"], help="type of measurements to retrieve")
    argument_parser.add_argument("-o", "--output", required=True, help="path to CSV output file")
    arguments = argument_parser.parse_args()

    # Read measurement files from Google Cloud
    storage_client = storage.Client(project=None)
    bucket = storage_client.get_bucket(arguments.bucket)
    blobs = bucket.list_blobs()

    # Parse measurements files
    if "individual" in arguments.type:
        data_frame = parse_individual_jobs(blobs, arguments.folder)
    elif "sequence" in arguments.type:
        data_frame = parse_job_sequences(blobs, arguments.folder)
    else:
        raise ValueError(f"Invalid measurement type: {arguments.type}")

    # Store parsed measurements
    data_frame.to_csv(arguments.output, index=False)


if __name__ == '__main__':
    main()
