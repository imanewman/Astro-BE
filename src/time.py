from datetime import datetime

import swisseph as swe


def get_julian_day(timestamp: datetime) -> float:
    """
    Returns the julian day float associated with the given time.

    :param timestamp: The time to use.

    :return: The julian day for that time.
    """

    hours = timestamp.hour + (timestamp.minute / 60)

    return swe.julday(timestamp.year, timestamp.month, timestamp.day, hours)