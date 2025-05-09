# gee_export

A package for exporting and downloading Earth Engine images.

## Installation

To install the package, run:

```
pip install git+https://github.com/pulakeshpradhan/export_earth.git
```
## Import Libraris 

```
from pulakesh import export_image_to_drive
from pulakesh import download_image_single
from pulakesh import download_image_tiles

from pulakesh import export_time_series_to_df
from pulakesh import export_time_series_to_drive
```




## Image Export 

```
import ee
import geemap


# Initialize Earth Engine
ee.Authenticate()
ee.Initialize(project='your-user-id')

# Define an image and a region
image = ee.Image('USGS/SRTMGL1_003')
region = ee.Geometry.Rectangle([-122.092, 37.42, -122.08, 37.43])

# Export the image to Google Drive
# export_image_to_drive(image, region, scale=30, description='srtm_export')

# Download the image as a single GeoTIFF
# download_image_single(image, region, scale=30, output_dir='./downloads')

# Download the image as tiles
download_image_tiles(image, region, scale=30, output_dir='./tiles', rows=2, cols=2)
```

## CSV Export

```
import ee
import pandas as pd
import numpy as np

# Initialize Earth Engine
ee.Authenticate()
ee.Initialize(project='pulakeshpradhan')

# --------------------------------------
# 2. Define Region of Interest and Time Range
# --------------------------------------
roi = ee.Geometry.Rectangle([91.0, 22.0, 92.0, 23.0])  # Example: Chittagong area
start_date = '2001-01-01'
end_date = '2022-12-31'

# --------------------------------------
# 3. Load and Scale MODIS LST Day Data
# --------------------------------------
modis_lst = ee.ImageCollection('MODIS/006/MOD11A2') \
    .select('LST_Day_1km') \
    .filterDate(start_date, end_date) \
    .map(lambda img: img.multiply(0.02)
         .copyProperties(img, img.propertyNames())
         .set('system:time_start', img.get('system:time_start')))
modis_lst

# Export to Google Drive as CSV 
export_time_series_to_drive(
    modis_lst, 
    roi, 
    scale=1000, 
    export_folder='GEE_exports', 
    export_filename='modis_lst_day_monthly'
)

# Export to directly pandas DataFrame (df)
df = export_time_series_to_df(modis_lst, ['LST_Day_1km'], region=roi, scale=1000)
df.to_csv('modis_lst_day_monthly.csv', index=False)
df

```
