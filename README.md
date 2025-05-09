# gee_export_utils

A package for exporting and downloading Earth Engine images.

## Installation

To install the package, run:

```
pip install git+https://github.com/pulakeshpradhan/geepack.git
```

## Usage

```python
import ee
import geemap
from gee_export_utils import export_image_to_drive, download_image_single, download_image_tiles

# Initialize Earth Engine
ee.Initialize()

## Example usage

```python
import ee
import geemap
from gee_export_utils import export_image_to_drive

# Initialize Earth Engine
ee.Initialize()

# Define an image and a region
image = ee.Image('USGS/SRTMGL1_003')
region = ee.Geometry.Rectangle([-122.092, 37.42, -122.08, 37.43])

# Export the image to Google Drive
export_image_to_drive(image, region, scale=30, description='srtm_export')

# Download the image as a single GeoTIFF
# download_image_single(image, region, scale=30, output_dir='./downloads')

# Download the image as tiles
# download_image_tiles(image, region, scale=30, output_dir='./tiles', rows=2, cols=2)
```
