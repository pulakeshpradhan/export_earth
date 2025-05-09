# gee_export_utils

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
```




## Usage

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
