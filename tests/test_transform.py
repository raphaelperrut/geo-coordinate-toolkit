import pytest

from geo_coordinate_toolkit.transform import transform_coordinate


def test_transform_wgs84_to_sirgas_2000_utm_23s() -> None:
    x, y = transform_coordinate(
        x=-47.8825,
        y=-15.7942,
        source_crs="EPSG:4326",
        target_crs="EPSG:31983",
    )

    assert x == pytest.approx(191171.363, abs=0.01)
    assert y == pytest.approx(8251713.127, abs=0.01)


def test_identity_transform() -> None:
    x, y = transform_coordinate(
        x=-47.8825,
        y=-15.7942,
        source_crs="EPSG:4326",
        target_crs="EPSG:4326",
    )

    assert x == pytest.approx(-47.8825)
    assert y == pytest.approx(-15.7942)


def test_invalid_crs() -> None:
    with pytest.raises(ValueError):
        transform_coordinate(
            x=-47.8825,
            y=-15.7942,
            source_crs="EPSG:INVALID",
            target_crs="EPSG:4326",
        )

@pytest.mark.parametrize(
    ("x", "y"),
    [
        (float("nan"), 0.0),
        (float("inf"), 0.0),
        (0.0, float("-inf")),
    ],
)
def test_non_finite_coordinates(x: float, y: float) -> None:
    with pytest.raises(
        ValueError,
        match="Coordinates must be finite numbers",
    ):
        transform_coordinate(
            x=x,
            y=y,
            source_crs="EPSG:4326",
            target_crs="EPSG:31983",
        )