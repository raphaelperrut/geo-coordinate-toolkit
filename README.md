# Geo Coordinate Toolkit

[![Tests](https://github.com/raphaelperrut/geo-coordinate-toolkit/actions/workflows/tests.yml/badge.svg)](https://github.com/raphaelperrut/geo-coordinate-toolkit/actions/workflows/tests.yml)
![Python](https://img.shields.io/badge/python-3.12%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)

A lightweight Python toolkit for coordinate transformation, CRS inspection, vector reprojection, geodesic distance calculation, and geometry validation.

Designed as a small, reproducible geospatial command-line application built on top of PyProj, GeoPandas, Shapely, Typer, and Rich.

## Features

- Inspect coordinate reference system metadata
- Transform coordinate pairs between CRS
- Reproject vector datasets
- Calculate geodesic or projected distances
- Validate vector geometries
- Command-line interface with structured output
- Automated tests with pytest
- Continuous integration with GitHub Actions

## Requirements

- Python 3.12 or newer

## Installation

Clone the repository:

```bash
git clone https://github.com/raphaelperrut/geo-coordinate-toolkit.git
cd geo-coordinate-toolkit
```

Create a virtual environment.

### Windows

```powershell
py -3.12 -m venv .venv
.\.venv\Scripts\Activate.ps1
```

### Linux / macOS

```bash
python3.12 -m venv .venv
source .venv/bin/activate
```

Install the package:

```bash
python -m pip install --upgrade pip
pip install -e .
```

For development and testing:

```bash
pip install -e ".[dev]"
```

After installation, the CLI is available as:

```bash
geo-coord --help
```

## Commands

### Inspect a CRS

Inspect metadata such as CRS name, authority, type, axes, units, and area of use.

```bash
geo-coord inspect EPSG:4326
```

Example:

```text
CRS Information

Name          WGS 84
Authority     EPSG:4326
Type          Geographic 2D CRS
Geographic    True
Projected     False
Axes          Geodetic latitude, Geodetic longitude
Units         degree
Area of use   World
```

Another example:

```bash
geo-coord inspect EPSG:31983
```

### Transform coordinates

Transform a coordinate pair between two coordinate reference systems.

```bash
geo-coord transform \
  --from EPSG:4326 \
  --to EPSG:31983 \
  --x -47.8825 \
  --y -15.7942
```

The transformation engine uses PyProj with explicit XY axis ordering.

For geographic CRS:

- X represents longitude
- Y represents latitude

For projected CRS:

- X normally represents easting
- Y normally represents northing

### Reproject a vector dataset

Reproject a vector dataset using GeoPandas.

```bash
geo-coord reproject \
  examples/sample.geojson \
  --to EPSG:31983 \
  --output sample_31983.geojson
```

Example output:

```text
Success: 2 feature(s) written to sample_31983.geojson
```

The output format is inferred from the output file extension.

### Calculate distance

Calculate the distance between two points.

For geographic CRS, the toolkit calculates a geodesic distance using the CRS ellipsoid.

```bash
geo-coord distance \
  --x1 -47.8825 \
  --y1 -15.7942 \
  --x2 -49.2643 \
  --y2 -16.6869 \
  --crs EPSG:4326
```

Example result:

```text
Distance: 177707.727
Unit: metre
```

For projected CRS, Euclidean distance is calculated in the CRS linear unit.

```bash
geo-coord distance \
  --x1 100 \
  --y1 100 \
  --x2 400 \
  --y2 500 \
  --crs EPSG:31983
```

Result:

```text
Distance: 500.000
Unit: metre
```

### Validate geometries

Validate geometries in a vector dataset.

```bash
geo-coord validate examples/sample.geojson
```

Example:

```text
Geometry Validation

Total geometries    2
Valid geometries    2
Invalid geometries  0
Empty geometries    0
```

The command uses the following exit codes:

| Exit code | Meaning |
|---|---|
| `0` | Validation completed and no invalid geometries were found |
| `1` | Execution or input error |
| `2` | One or more invalid geometries were found |

Missing geometries are treated as invalid.

## Testing

Run the complete test suite with:

```bash
pytest -v
```

The test suite covers:

- CRS inspection
- Valid and invalid CRS input
- Coordinate transformation
- Identity transformations
- Non-finite coordinate rejection
- Geographic geodesic distance
- Projected Euclidean distance
- Vector reprojection
- Missing input datasets
- Geometry validation
- Invalid geometries
- Missing geometries

Tests are also executed automatically on GitHub Actions for pushes and pull requests targeting `main`.

## Project structure

```text
geo-coordinate-toolkit/
├── .github/
│   └── workflows/
│       └── tests.yml
├── examples/
│   └── sample.geojson
├── src/
│   └── geo_coordinate_toolkit/
│       ├── __init__.py
│       ├── cli.py
│       ├── crs.py
│       ├── distance.py
│       ├── reproject.py
│       ├── transform.py
│       └── validate.py
├── tests/
│   ├── test_crs.py
│   ├── test_distance.py
│   ├── test_reproject.py
│   ├── test_transform.py
│   └── test_validate.py
├── LICENSE
├── pyproject.toml
└── README.md
```

## Technology stack

- [PyProj](https://pyproj4.github.io/pyproj/) — CRS and coordinate transformations
- [GeoPandas](https://geopandas.org/) — vector geospatial data processing
- [Shapely](https://shapely.readthedocs.io/) — geometry operations and validation
- [Typer](https://typer.tiangolo.com/) — command-line interface
- [Rich](https://rich.readthedocs.io/) — terminal output
- [pytest](https://docs.pytest.org/) — automated testing
- GitHub Actions — continuous integration

## Design principles

This project intentionally keeps its scope small.

Core geospatial operations are implemented separately from the command-line presentation layer, making the functionality easier to test and reuse.

The toolkit favors:

- explicit CRS handling
- predictable XY coordinate ordering
- reproducible transformations
- clear CLI behavior
- automated testing
- minimal dependencies and architecture

## Example dataset

The repository includes:

```text
examples/sample.geojson
```

which can be used to test reprojection and geometry validation commands.

## Development

Install development dependencies:

```bash
pip install -e ".[dev]"
```

Run tests:

```bash
pytest -v
```

## Roadmap

Potential future improvements include:

- additional vector input/output options
- geometry validation diagnostics
- batch coordinate transformation
- configurable distance output units
- package publication to PyPI

These features are intentionally outside the initial `0.1.x` scope.

## License

This project is licensed under the MIT License.
