import ee
import geemap
from gee_export_utils import export_image_to_drive, download_image_single, download_image_tiles

# Initialize Earth Engine
try:
    ee.Initialize()
    print("Earth Engine initialized successfully.")
except Exception as e:
    print(f"Error initializing Earth Engine: {e}")

# Example usage (replace with your actual image and region)
# image = ee.Image('USGS/SRTMGL1_003')
# region = ee.Geometry.Rectangle([-122.092, 37.42, -122.08, 37.43])
# export_image_to_drive(image, region, scale=30, description='test_export')

# download_image_single(image, region, scale=30, output_dir='./downloads')

# download_image_tiles(image, region, scale=30, output_dir='./tiles')
