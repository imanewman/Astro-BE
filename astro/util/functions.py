def convert_to_degrees(degrees: int, minutes: int, seconds: int) -> float:
    """
    Converts degrees given in whole numbers to the float equivalent.

    :param degrees: The current degrees out of 360.
    :param minutes: The current minutes out of 60.
    :param seconds: The current seconds out of 60.

    :return: The combined degrees as a float.
    """

    return degrees + (minutes / 60) + (seconds / 60 / 60)