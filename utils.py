import datetime
import iso8601
import time


def datetime_to_timestamp(datetime_obj):
    """Convert utc datetime object into milliseconds timestamp.

    :param datetime_obj:
    :type datetime_obj: datetime.datetime
    :returns: Number of milliseconds since epoch
    :rtype:int:
    """
    time_tuple = datetime_obj.timetuple()
    return int(time.mktime(time_tuple) * 1e3)


def timestamp_to_datetime(timestamp):
    """Converts timestamp in milliseconds to datetime.

    :param timestamp: Number of milliseconds since epoch
    :type timestamp: int
    :returns: Datetime object
    :rtype: datetime.datetime
    """
    dt = datetime.datetime.fromtimestamp(timestamp / 1e3)
    dt = dt.replace(microsecond=0)
    return dt


def parse_datetime(date_str):
    """Parse a datetime object from a string.
    :param date_str: String to parse
    :type date_str: String
    :return: Parse datetime object
    :rtype: datetime.datetime
    """
    return iso8601.parse_date(date_str)


def normalize_time(timestamp):
    """Normalize time in arbitrary timezone to UTC naive object.
    Taken from oslo.utils.timeutils
    """
    offset = timestamp.utcoffset()
    if offset is None:
        return timestamp
    return timestamp.replace(tzinfo=None) - offset
