from dataclasses import dataclass

from pyproj import CRS
from pyproj.exceptions import CRSError


@dataclass(frozen=True)
class CRSInfo:
    """Relevant metadata describing a coordinate reference system."""

    name: str
    authority: str | None
    code: str | None
    type_name: str
    is_geographic: bool
    is_projected: bool
    axis_names: tuple[str, ...]
    unit_names: tuple[str, ...]
    area_of_use: str | None


def inspect_crs(crs_input: str) -> CRSInfo:
    """
    Inspect a coordinate reference system.

    Parameters
    ----------
    crs_input:
        CRS accepted by PyProj, for example ``EPSG:4326``.

    Returns
    -------
    CRSInfo
        Structured CRS metadata.

    Raises
    ------
    ValueError
        If the CRS cannot be parsed.
    """

    try:
        crs = CRS.from_user_input(crs_input)
    except CRSError as exc:
        raise ValueError(f"Invalid CRS: {crs_input}") from exc

    authority = crs.to_authority()

    axis_names = tuple(axis.name for axis in crs.axis_info)

    unit_names = tuple(
        dict.fromkeys(
            axis.unit_name
            for axis in crs.axis_info
            if axis.unit_name
        )
    )

    return CRSInfo(
        name=crs.name,
        authority=authority[0] if authority else None,
        code=authority[1] if authority else None,
        type_name=crs.type_name,
        is_geographic=crs.is_geographic,
        is_projected=crs.is_projected,
        axis_names=axis_names,
        unit_names=unit_names,
        area_of_use=crs.area_of_use.name if crs.area_of_use else None,
    )