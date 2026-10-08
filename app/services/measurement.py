def calculate_measurement(geometry):
    geometry_type = geometry.geom_type

    if geometry_type == "Polygon":
        return geometry.area, "m²"

    if geometry_type == "MultiPolygon":
        return geometry.area, "m²"

    if geometry_type == "LineString":
        return geometry.length, "m"

    if geometry_type == "MultiLineString":
        return geometry.length, "m"

    if geometry_type in ["Point", "MultiPoint"]:
        return None, None

    return None, None