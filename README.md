# Geospatial File Measurement API

A FastAPI-based backend API for processing geospatial files and calculating measurements such as **polygon area** and **line length**.

The API accepts:

* `.kml` files
* `.zip` files containing a Shapefile

It extracts feature information such as geometry, geometry type, CRS, and properties, and provides measurement results through REST APIs.

---

## Features

* Upload KML files.
* Upload ZIP files containing Shapefiles.
* Extract feature ID, geometry type, geometry, CRS, and properties.
* Calculate polygon area.
* Calculate LineString length.
* Handle Point geometries without calculating a measurement.
* Handle unsupported geometry types gracefully.
* Detect geographic CRS such as EPSG:4326.
* Transform geographic CRS into a suitable projected CRS before measurement.
* Validate uploaded file types.
* Handle invalid ZIP files and ZIP files without Shapefiles.
* REST APIs documented using FastAPI Swagger UI.
* Automated tests using Pytest.

---

## Technologies Used

* **Python**
* **FastAPI** – REST API development
* **GeoPandas** – reading and processing geospatial data
* **Shapely** – geometry operations and measurements
* **PyProj** – coordinate reference system handling
* **Fiona** – geospatial file support
* **Uvicorn** – application server
* **Pytest** – automated testing
* **HTTPX** – API testing

---

## Project Structure

```text
Aereo assignment/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── api/
│   │   ├── __init__.py
│   │   └── files.py
│   │
│   ├── models/
│   │   ├── __init__.py
│   │   └── schemas.py
│   │
│   ├── services/
│   │   ├── __init__.py
│   │   ├── file_processor.py
│   │   ├── measurement.py
│   │   └── crs.py
│   │
│   └── storage/
│       ├── __init__.py
│       └── repository.py
│
├── tests/
│   ├── __init__.py
│   ├── test_upload.py
│   ├── test_measurements.py
│   └── test_crs.py
│
├── uploads/
│
├── .gitignore
├── README.md
├── requirements.txt
└── run.py
```

---

## Architecture

The application is divided into different layers so that file processing, measurement logic, API handling, and storage remain separate.

```text
Client
   |
   v
FastAPI API Layer
   |
   v
File Processing Service
   |
   +---- KML Reader
   |
   +---- ZIP / Shapefile Reader
   |
   v
Feature Extraction
   |
   v
In-Memory Repository
   |
   v
Measurement Service
   |
   v
CRS Transformation
   |
   v
Area / Length Calculation
```

### Main Components

**API Layer**

`app/api/files.py`

Handles file uploads, file details,
