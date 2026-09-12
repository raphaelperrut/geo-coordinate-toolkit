from pyproj import CRS, Transformer
from pyproj.exceptions import CRSError


def transform_coordinate(
    x: float,
    y: float,
    source_crs: str,
    target_crs: str,
) -> tuple[float, float]:
    """
    Transform a coordinate pair between two coordinate reference systems.

    Parameters
    ----------
    x:
        X coordinate. For geographic CRS, normally longitude.
    y:
        Y coordinate. For geographic CRS, normally latitude.
    source_crs:
        Source CRS accepted by PyProj, for example ``EPSG:4326``.
    target_crs:
        Target CRS accepted by PyProj, for example ``EPSG:31983``.

    Returns
    -------
    tuple[float, float]
        Transformed X and Y coordinates.

    Raises
    ------
    ValueError
        If either CRS is invalid.
    """

    try:
        source = CRS.from_user_input(source_crs)
        target = CRS.from_user_input(target_crs)
    except CRSError as exc:
        raise ValueError(f"Invalid CRS: {exc}") from exc

    transformer = Transformer.from_crs(
        source,
        target,
        always_xy=True,
    )

    transformed_x, transformed_y = transformer.transform(x, y)

    return transformed_x, transformed_y