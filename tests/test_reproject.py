from pathlib import Path

import geopandas as gpd
import pytest

from geo_coordinate_toolkit.reproject import reproject_vector


def test_reproject_geojson(tmp_path: Path) -> None:
    input_path = Path("examples/sample.geojson")
    output_path = tmp_path / "sample_31983.geojson"

    feature_count = reproject_vector(
        input_path=input_path,
        output_path=output_path,
        target_crs="EPSG:31983",
    )

    assert feature_count == 2
    assert output_path.exists()

    result = gpd.read_file(output_path)

    assert len(result) == 2
    assert result.crs is not None
    assert result.crs.to_epsg() == 31983


def test_reproject_missing_file(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Input file does not exist"):
        reproject_vector(
            input_path=tmp_path / "missing.geojson",
            output_path=tmp_path / "output.geojson",
            target_crs="EPSG:31983",
        )


def test_reproject_invalid_target_crs(tmp_path: Path) -> None:
    with pytest.raises(ValueError, match="Invalid target CRS"):
        reproject_vector(
            input_path=Path("examples/sample.geojson"),
            output_path=tmp_path / "output.geojson",
            target_crs="EPSG:INVALID",
        )