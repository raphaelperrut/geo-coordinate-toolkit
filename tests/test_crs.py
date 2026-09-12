import pytest

from geo_coordinate_toolkit.crs import inspect_crs


def test_inspect_wgs84() -> None:
    info = inspect_crs("EPSG:4326")

    assert info.name == "WGS 84"
    assert info.authority == "EPSG"
    assert info.code == "4326"
    assert info.is_geographic is True
    assert info.is_projected is False
    assert "degree" in info.unit_names


def test_inspect_sirgas_2000_utm_23s() -> None:
    info = inspect_crs("EPSG:31983")

    assert info.authority == "EPSG"
    assert info.code == "31983"
    assert info.is_geographic is False
    assert info.is_projected is True
    assert "metre" in info.unit_names


def test_invalid_crs() -> None:
    with pytest.raises(ValueError):
        inspect_crs("EPSG:INVALID")