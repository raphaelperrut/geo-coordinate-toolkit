from math import hypot

from pyproj import CRS, Geod
from pyproj.exceptions import CRSError


def calculate_distance(
    x1: float,
    y1: float,
    x2: float,
    y2: float,
    crs_input: str,
) -> tuple[float, str]:
    """
    Calculate the distance between two points.

    For geographic CRS, the distance is geodesic and returned in metres.
    For projected CRS, the distance is Euclidean and returned in the
    CRS linear unit.
    """

    try:
        crs = CRS.from_user_input(crs_input)
    except CRSError as exc:
        raise ValueError(f"Invalid CRS: {crs_input}") from exc

    if crs.is_geographic:
        geod = crs.get_geod()

        _, _, distance = geod.inv(
            x1,
            y1,
            x2,
            y2,
        )

        return abs(distance), "metre"

    if crs.is_projected:
        unit_name = (
            crs.axis_info[0].unit_name
            if crs.axis_info and crs.axis_info[0].unit_name
            else "unknown"
        )

        distance = hypot(
            x2 - x1,
            y2 - y1,
        )

        return distance, unit_name

    raise ValueError(
        f"Unsupported CRS type for distance calculation: {crs.type_name}"
    )