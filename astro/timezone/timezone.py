import datetime

import googlemaps

from astro.schema.timezone import TimezoneQuerySchema, TimezoneSchema
from ._api_keys import google_api_key

gmaps = googlemaps.Client(key=google_api_key)


def calculate_timezone(query: TimezoneQuerySchema) -> TimezoneSchema:
    """
    Calculates the UTC date for a local time and location.

    :param query: The information used to calculate the correct UTC date.
    :return: The calculated timezone and UTC date.
    """
    timezone = TimezoneSchema(**query.dict(), utc_date=query.local_date)

    get_geocode(timezone)
    get_timezone(timezone)

    return timezone


def get_geocode(timezone: TimezoneSchema):
    """
    Returns the latitude and longitude of a specific location.

    - sets the `timezone.locationName` To the full location address.
    - sets the `timezone.latitude` To the location's latitude.
    - sets the `timezone.longitude` To the location's longitude.

    :param timezone: The timezone details with the timezone name.
    """
    geocode = gmaps.geocode(timezone.location_name)[0]

    timezone.location_name = geocode["formatted_address"]
    timezone.latitude = geocode["geometry"]["location"]["lat"]
    timezone.longitude = geocode["geometry"]["location"]["lng"]


def get_timezone(timezone: TimezoneSchema):
    """
    Returns the latitude and longitude of a specific location.

    - sets the `timezone.time_zone_id` To the timezone's ID.
    - sets the `timezone.time_zone_name` To the timezone's name.
    - sets the `timezone.dst_offset` To the timezone's DST offset in milliseconds.
    - sets the `timezone.rawOffset` To the timezone's UTC offset in milliseconds.

    :param timezone: The timezone details with the local date and geolocation.
    """
    tz = gmaps.timezone(
        location=f"{timezone.latitude},{timezone.longitude}",
        timestamp=timezone.local_date
    )

    timezone.time_zone_id = tz["timeZoneId"]
    timezone.time_zone_name = tz["timeZoneName"]
    timezone.dst_offset = tz["dstOffset"]
    timezone.raw_offset = tz["rawOffset"]

    time_offset = timezone.dst_offset + timezone.raw_offset
    offset_hours = int(time_offset / 60 / 60)
    utc_date_ms = timezone.local_date.timestamp() - time_offset

    # Generate the UTC time by applying the timezone offset to the local time.
    timezone.utc_offset = f"UTC{offset_hours}.00"
    timezone.utc_date = datetime.datetime.fromtimestamp(utc_date_ms, tz=datetime.timezone.utc)

