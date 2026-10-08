import geopandas as gpd


def get_measurement_gdf(gdf: gpd.GeoDataFrame):
    if gdf.crs is None:
        raise ValueError("Input file does not contain a CRS")

    if not gdf.crs.is_geographic:
        return gdf, gdf.crs.to_string()

    representative_point = gdf.geometry.union_all().centroid

    utm_crs = gpd.GeoDataFrame(
        geometry=[representative_point],
        crs=gdf.crs
    ).estimate_utm_crs()

    if utm_crs is None:
        raise ValueError("Could not determine a suitable projected CRS")

    transformed_gdf = gdf.to_crs(utm_crs)

    return transformed_gdf, utm_crs.to_string()