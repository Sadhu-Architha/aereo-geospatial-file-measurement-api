from pathlib import Path
from uuid import uuid4

from fastapi import APIRouter, File, HTTPException, UploadFile

from app.models.schemas import (
    FileDetailsResponse,
    FileUploadResponse,
    MeasurementsResponse,
)
from app.services.file_processor import (
    extract_features,
    read_geospatial_file,
    validate_file,
)
from app.services.crs import get_measurement_gdf
from app.services.measurement import calculate_measurement
from app.storage.repository import get_file, save_file


router = APIRouter(prefix="/api/files", tags=["files"])

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


@router.post("/", response_model=FileUploadResponse)
async def upload_file(file: UploadFile = File(...)):
    try:
        validate_file(file.filename)

        file_id = str(uuid4())
        extension = Path(file.filename).suffix.lower()

        file_path = UPLOAD_DIR / f"{file_id}{extension}"

        content = await file.read()

        with open(file_path, "wb") as output_file:
            output_file.write(content)

        gdf = read_geospatial_file(str(file_path))

        features = extract_features(gdf)

        source_crs = gdf.crs.to_string() if gdf.crs else None

        data = {
            "file_id": file_id,
            "filename": file.filename,
            "status": "COMPLETED",
            "source_crs": source_crs,
            "features": features,
            "gdf": gdf,
            "file_path": str(file_path),
        }

        save_file(file_id, data)

        return {
            "file_id": file_id,
            "filename": file.filename,
            "status": "COMPLETED",
        }

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to process file: {str(exc)}",
        )


@router.get("/{file_id}", response_model=FileDetailsResponse)
def get_file_details(file_id: str):
    data = get_file(file_id)

    if data is None:
        raise HTTPException(status_code=404, detail="File not found")

    return {
        "file_id": data["file_id"],
        "filename": data["filename"],
        "status": data["status"],
        "source_crs": data["source_crs"],
        "features": data["features"],
    }


@router.get("/{file_id}/measurements/", response_model=MeasurementsResponse)
def get_measurements(file_id: str):
    data = get_file(file_id)

    if data is None:
        raise HTTPException(status_code=404, detail="File not found")

    try:
        measurement_gdf, measurement_crs = get_measurement_gdf(data["gdf"])

        measurements = []

        for index, geometry in enumerate(measurement_gdf.geometry):
            value, unit = calculate_measurement(geometry)

            original_geometry_type = data["gdf"].geometry.iloc[index].geom_type

            measurements.append(
                {
                    "feature_id": index,
                    "geometry_type": original_geometry_type,
                    "measurement": value,
                    "unit": unit,
                }
            )

        return {
            "file_id": file_id,
            "source_crs": data["source_crs"],
            "measurement_crs": measurement_crs,
            "measurements": measurements,
        }

    except ValueError as exc:
        raise HTTPException(status_code=400, detail=str(exc))

    except Exception as exc:
        raise HTTPException(
            status_code=500,
            detail=f"Failed to calculate measurements: {str(exc)}",
        )