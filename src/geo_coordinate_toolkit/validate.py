from dataclasses import dataclass
from pathlib import Path

import geopandas as gpd


@dataclass(frozen=True)
class GeometryValidationResult:
    """Summary of geometry validation for a vector dataset."""

    total: int
    valid: int
    invalid: int
    empty: int


def validate_geometries(
    input_path: Path,
) -> GeometryValidationResult:
    """
    Validate geometries in a vector dataset.

    Parameters
    ----------
    input_path:
        Path to the input vector dataset.

    Returns
    -------
    GeometryValidationResult
        Geometry validation summary.

    Raises
    ------
    ValueError
        If the input file does not exist.
    """

    if not input_path.exists():
        raise ValueError(f"Input file does not exist: {input_path}")

    data = gpd.read_file(input_path)

    total = len(data)

    empty_mask = data.geometry.is_empty
    invalid_mask = ~data.geometry.is_valid & ~empty_mask
    valid_mask = data.geometry.is_valid & ~empty_mask

    return GeometryValidationResult(
        total=total,
        valid=int(valid_mask.sum()),
        invalid=int(invalid_mask.sum()),
        empty=int(empty_mask.sum()),
    )