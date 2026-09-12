from pathlib import Path

import geopandas as gpd
from pyproj import CRS
from pyproj.exceptions import CRSError


def reproject_vector(
    input_path: Path,
    output_path: Path,
    target_crs: str,
) -> int:
    """
    Reproject a vector dataset to a target CRS.

    Parameters
    ----------
    input_path:
        Path to the input vector dataset.
    output_path:
        Path where the reprojected dataset will be written.
    target_crs:
        Target CRS accepted by PyProj, for example ``EPSG:31983``.

    Returns
    -------
    int
        Number of features written.

    Raises
    ------
    ValueError
        If the input file does not exist, has no CRS, or the target CRS
        is invalid.
    """

    if not input_path.exists():
        raise ValueError(f"Input file does not exist: {input_path}")

    try:
        target = CRS.from_user_input(target_crs)
    except CRSError as exc:
        raise ValueError(f"Invalid target CRS: {target_crs}") from exc

    data = gpd.read_file(input_path)

    if data.crs is None:
        raise ValueError("Input dataset has no CRS.")

    reprojected = data.to_crs(target)

    output_path.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    reprojected.to_file(output_path)

    return len(reprojected)