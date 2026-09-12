from pathlib import Path

import geopandas as gpd
import pytest
from shapely.geometry import Polygon

from geo_coordinate_toolkit.validate import validate_geometries


def test_validate_valid_dataset() -> None:
    result = validate_geometries(
        Path("examples/sample.geojson")
    )

    assert result.total == 2
    assert result.valid == 2
    assert result.invalid == 0
    assert result.empty == 0


def test_validate_invalid_geometry(tmp_path: Path) -> None:
    invalid_polygon = Polygon(
        [
            (0, 0),
            (1, 1),
            (1, 0),
            (0, 1),
            (0, 0),
        ]
    )

    data = gpd.GeoDataFrame(
        {"name": ["invalid"]},
        geometry=[invalid_polygon],
        crs="EPSG:4326",
    )

    input_path = tmp_path / "invalid.geojson"
    data.to_file(input_path)

    result = validate_geometries(input_path)

    assert result.total == 1
    assert result.valid == 0
    assert result.invalid == 1
    assert result.empty == 0


def test_validate_missing_file(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Input file does not exist"):
        validate_geometries(
            tmp_path / "missing.geojson"
        )

def test_validate_missing_geometry(tmp_path: Path) -> None:
    data = gpd.GeoDataFrame(
        {"name": ["missing"]},
        geometry=[None],
        crs="EPSG:4326",
    )

    input_path = tmp_path / "missing_geometry.geojson"
    data.to_file(input_path)

    result = validate_geometries(input_path)

    assert result.total == 1
    assert result.valid == 0
    assert result.invalid == 1
    assert result.empty == 0