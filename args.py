import argparse
import utils


def check_datetime(date_str):
    """Parse iso8601 datetime strings.
    :param date_str: String from a datetime argument.
    :type date_str: String
    :returns: Normalized datetime object
    :rtype: datetime.datetime
    """
    try:
        dt = utils.parse_datetime(date_str)
        dt = utils.normalize_time(dt)
    except Exception:
        raise argparse.ArgumentTypeError(
            "{} is an invalid iso8601 datetime string.".format(date_str)
        )
    return dt


parser = argparse.ArgumentParser(description="Some alarm reporting things.")
parser.add_argument(
    '--start',
    type=check_datetime,
    required=True,
    help="ISO8601 Report Start Date and Time. Example: '2017-12-01T00:00:00'"
)
parser.add_argument(
    '--stop',
    type=check_datetime,
    required=True,
    help="ISO8601 Report Stop Date and Time. Example: '2018-01-01T00:00:00'"
)

parser.add_argument(
    '--output',
    type=str,
    required=True,
    help="Name of the output file."
)
