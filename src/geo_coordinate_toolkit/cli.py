from pathlib import Path

import typer
from rich.console import Console
from rich.table import Table

from geo_coordinate_toolkit.crs import inspect_crs
from geo_coordinate_toolkit.distance import calculate_distance
from geo_coordinate_toolkit.reproject import reproject_vector
from geo_coordinate_toolkit.transform import transform_coordinate
from geo_coordinate_toolkit.validate import validate_geometries

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
def reproject(
    input_path: Path = typer.Argument(
        ...,
        help="Input vector dataset.",
    ),
    target_crs: str = typer.Option(
        ...,
        "--to",
        help="Target CRS, for example EPSG:31983.",
    ),
    output_path: Path = typer.Option(
        ...,
        "--output",
        "-o",
        help="Output vector dataset.",
    ),
) -> None:
    """Reproject a vector dataset to another CRS."""

    try:
        feature_count = reproject_vector(
            input_path=input_path,
            output_path=output_path,
            target_crs=target_crs,
        )
    except ValueError as exc:
        console.print(f"[bold red]Error:[/bold red] {exc}")
        raise typer.Exit(code=1) from exc
    except Exception as exc:
        console.print(
            f"[bold red]Error while processing vector dataset:[/bold red] {exc}"
        )
        raise typer.Exit(code=1) from exc

    console.print(
        f"[bold green]Success:[/bold green] "
        f"{feature_count} feature(s) written to {output_path}"
    )

@app.command()
def distance(
    x1: float = typer.Option(
        ...,
        "--x1",
        help="X coordinate of the first point.",
    ),
    y1: float = typer.Option(
        ...,
        "--y1",
        help="Y coordinate of the first point.",
    ),
    x2: float = typer.Option(
        ...,
        "--x2",
        help="X coordinate of the second point.",
    ),
    y2: float = typer.Option(
        ...,
        "--y2",
        help="Y coordinate of the second point.",
    ),
    crs: str = typer.Option(
        ...,
        "--crs",
        help="CRS of the input coordinates, for example EPSG:4326.",
    ),
) -> None:
    """Calculate the distance between two points."""

    try:
        value, unit = calculate_distance(
            x1=x1,
            y1=y1,
            x2=x2,
            y2=y2,
            crs_input=crs,
        )
    except ValueError as exc:
        console.print(f"[bold red]Error:[/bold red] {exc}")
        raise typer.Exit(code=1) from exc

    table = Table(title="Distance")

    table.add_column("Property", style="bold")
    table.add_column("Value")

    table.add_row("CRS", crs)
    table.add_row("Point 1", f"{x1}, {y1}")
    table.add_row("Point 2", f"{x2}, {y2}")
    table.add_row("Distance", f"{value:.3f}")
    table.add_row("Unit", unit)

    console.print(table)

@app.command()
def validate(
    input_path: Path = typer.Argument(
        ...,
        help="Input vector dataset.",
    ),
) -> None:
    """Validate geometries in a vector dataset."""

    try:
        result = validate_geometries(input_path)
    except ValueError as exc:
        console.print(f"[bold red]Error:[/bold red] {exc}")
        raise typer.Exit(code=1) from exc
    except Exception as exc:
        console.print(
            f"[bold red]Error while validating vector dataset:[/bold red] {exc}"
        )
        raise typer.Exit(code=1) from exc

    table = Table(title="Geometry Validation")

    table.add_column("Property", style="bold")
    table.add_column("Value")

    table.add_row("Dataset", str(input_path))
    table.add_row("Total geometries", str(result.total))
    table.add_row("Valid geometries", str(result.valid))
    table.add_row("Invalid geometries", str(result.invalid))
    table.add_row("Empty geometries", str(result.empty))

    console.print(table)

    if result.invalid > 0:
        raise typer.Exit(code=2)

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