import typer
from rich.console import Console
from rich.table import Table

from geo_coordinate_toolkit.transform import transform_coordinate
from geo_coordinate_toolkit.crs import inspect_crs

app = typer.Typer(
    name="geo-coord",
    help="Lightweight geospatial coordinate utilities.",
    no_args_is_help=True,
)

console = Console()


@app.callback()
def main() -> None:
    """Geo Coordinate Toolkit command-line interface."""


@app.command()
def inspect(
    crs: str = typer.Argument(
        ...,
        help="CRS to inspect, for example EPSG:4326.",
    ),
) -> None:
    """Inspect coordinate reference system metadata."""

    try:
        info = inspect_crs(crs)
    except ValueError as exc:
        console.print(f"[bold red]Error:[/bold red] {exc}")
        raise typer.Exit(code=1) from exc

    table = Table(title="CRS Information")

    table.add_column("Property", style="bold")
    table.add_column("Value")

    table.add_row("Name", info.name)

    authority_value = (
        f"{info.authority}:{info.code}"
        if info.authority and info.code
        else "Unknown"
    )

    table.add_row("Authority", authority_value)
    table.add_row("Type", info.type_name)
    table.add_row("Geographic", str(info.is_geographic))
    table.add_row("Projected", str(info.is_projected))
    table.add_row(
        "Axes",
        ", ".join(info.axis_names) if info.axis_names else "Unknown",
    )
    table.add_row(
        "Units",
        ", ".join(info.unit_names) if info.unit_names else "Unknown",
    )
    table.add_row(
        "Area of use",
        info.area_of_use or "Unknown",
    )

    console.print(table)

@app.command()
def transform(
    x: float = typer.Option(
        ...,
        "--x",
        help="Input X coordinate (longitude for geographic CRS).",
    ),
    y: float = typer.Option(
        ...,
        "--y",
        help="Input Y coordinate (latitude for geographic CRS).",
    ),
    source_crs: str = typer.Option(
        ...,
        "--from",
        help="Source CRS, for example EPSG:4326.",
    ),
    target_crs: str = typer.Option(
        ...,
        "--to",
        help="Target CRS, for example EPSG:31983.",
    ),
) -> None:
    """Transform one coordinate pair between two CRS."""

    try:
        transformed_x, transformed_y = transform_coordinate(
            x=x,
            y=y,
            source_crs=source_crs,
            target_crs=target_crs,
        )
    except ValueError as exc:
        console.print(f"[bold red]Error:[/bold red] {exc}")
        raise typer.Exit(code=1) from exc

    table = Table(title="Coordinate Transformation")

    table.add_column("Property", style="bold")
    table.add_column("Value")

    table.add_row("Source CRS", source_crs)
    table.add_row("Target CRS", target_crs)
    table.add_row("Input X", f"{x:.8f}")
    table.add_row("Input Y", f"{y:.8f}")
    table.add_row("Output X", f"{transformed_x:.3f}")
    table.add_row("Output Y", f"{transformed_y:.3f}")

    console.print(table)


if __name__ == "__main__":
    app()