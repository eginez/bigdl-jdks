import pandas as pd
import re

from argparse import ArgumentParser
from google.cloud import storage
from re import RegexFlag


def main():
    """Collect the data stored on the Google Cloud Platform and convert it to a CSV file."""

    # Parse arguments
    argument_parser = ArgumentParser()
    argument_parser.add_argument("-b", "--bucket", required=True, help="bucket from which to retrieve measurements")
    argument_parser.add_argument("-o", "--output", required=True, help="path to CSV output file")
    arguments = argument_parser.parse_args()

    # Read measurements files from Google Cloud
    storage_client = storage.Client(project=None)
    bucket = storage_client.get_bucket(arguments.bucket)
    blobs = bucket.list_blobs()
    rows = []
    for blob in blobs:

        name_match = re.match("([^-]+)-([^-]+)-([^-]+)-([^-]+)-.*", blob.name)
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

    # Create and store dataframe
    data_frame = pd.DataFrame(rows, columns=["compiler", "nodes", "cores", "batch_size", "runtime", "accuracy"])
    data_frame.to_csv(arguments.output)


if __name__ == '__main__':
    main()
