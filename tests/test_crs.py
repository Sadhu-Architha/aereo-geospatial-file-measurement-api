import geopandas as gpd
from shapely.geometry import Point

from app.services.crs import get_measurement_gdf


def test_geographic_crs_is_transformed():
    gdf = gpd.GeoDataFrame(
        {"name": ["Test"]},
        geometry=[Point(78.45, 17.40)],
        crs="EPSG:4326"
    )

    transformed_gdf, measurement_crs = get_measurement_gdf(gdf)

    assert transformed_gdf.crs.is_projected
    assert measurement_crs != "EPSG:4326"