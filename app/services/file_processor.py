from pathlib import Path
import tempfile
import zipfile

import geopandas as gpd
from shapely.geometry import mapping


ALLOWED_EXTENSIONS = {".zip", ".kml"}


def validate_file(filename: str) -> None:
    extension = Path(filename).suffix.lower()

    if extension not in ALLOWED_EXTENSIONS:
        raise ValueError("Only .zip and .kml files are supported")


def read_geospatial_file(file_path: str) -> gpd.GeoDataFrame:
    path = Path(file_path)

    if path.suffix.lower() == ".kml":
        return gpd.read_file(path, driver="KML")

    if path.suffix.lower() == ".zip":
        return read_shapefile_from_zip(path)

    raise ValueError("Unsupported file format")


def read_shapefile_from_zip(zip_path: Path) -> gpd.GeoDataFrame:
    with tempfile.TemporaryDirectory() as temp_dir:
        temp_path = Path(temp_dir)

        try:
            with zipfile.ZipFile(zip_path, "r") as zip_file:
                for member in zip_file.namelist():
                    member_path = Path(member)

                    if member_path.is_absolute() or ".." in member_path.parts:
                        raise ValueError("Unsafe ZIP file")

                    zip_file.extract(member, temp_path)

        except zipfile.BadZipFile:
            raise ValueError("Invalid ZIP file")

        shapefiles = list(temp_path.rglob("*.shp"))

        if not shapefiles:
            raise ValueError("No Shapefile found inside ZIP")

        shapefile = shapefiles[0]

        base_name = shapefile.with_suffix("")

        required_files = [
            base_name.with_suffix(".shp"),
            base_name.with_suffix(".shx"),
            base_name.with_suffix(".dbf"),
        ]

        for required_file in required_files:
            if not required_file.exists():
                raise ValueError(
                    f"Missing required Shapefile component: {required_file.suffix}"
                )

        return gpd.read_file(shapefile)


def extract_features(gdf: gpd.GeoDataFrame) -> list[dict]:
    source_crs = gdf.crs.to_string() if gdf.crs else None

    features = []

    for index, row in gdf.iterrows():
        geometry = row.geometry

        properties = {}

        for column in gdf.columns:
            if column != gdf.geometry.name:
                value = row[column]

                if hasattr(value, "item"):
                    value = value.item()

                if value is None or isinstance(value, (str, int, float, bool)):
                    properties[column] = value
                else:
                    properties[column] = str(value)

        features.append(
            {
                "feature_id": int(index),
                "geometry_type": geometry.geom_type,
                "geometry": mapping(geometry),
                "crs": source_crs,
                "properties": properties,
            }
        )

    return features