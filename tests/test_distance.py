import pytest

from geo_coordinate_toolkit.distance import calculate_distance


def test_projected_distance() -> None:
    distance, unit = calculate_distance(
        x1=100.0,
        y1=100.0,
        x2=400.0,
        y2=500.0,
        crs_input="EPSG:31983",
    )

    assert distance == pytest.approx(500.0)
    assert unit == "metre"


def test_geographic_distance() -> None:
    distance, unit = calculate_distance(
        x1=-47.8825,
        y1=-15.7942,
        x2=-49.2643,
        y2=-16.6869,
        crs_input="EPSG:4326",
    )

    assert distance == pytest.approx(177707.727, abs=0.01)
    assert unit == "metre"


def test_zero_distance() -> None:
    distance, unit = calculate_distance(
        x1=-47.8825,
        y1=-15.7942,
        x2=-47.8825,
        y2=-15.7942,
        crs_input="EPSG:4326",
    )

    assert distance == pytest.approx(0.0)
    assert unit == "metre"


def test_invalid_crs() -> None:
    with pytest.raises(ValueError, match="Invalid CRS"):
        calculate_distance(
            x1=0.0,
            y1=0.0,
            x2=1.0,
            y2=1.0,
            crs_input="EPSG:INVALID",
        )