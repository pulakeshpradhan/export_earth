# 💾 7. Export and Download Utilities (Standardized)
# --------------------------------------------------
import ee
import geemap
import os

def export_image_to_drive(image, region, scale, crs='EPSG:4326', description='export'):
    """
    Export an Earth Engine image to Google Drive.

    Args:
        image (ee.Image): The Earth Engine image to export.
        region (ee.Geometry, optional): Export region. Defaults to global 'roi' if None.
        description (str): Export task name and output filename prefix.
        scale (int): Resolution in meters.
        crs (str): Coordinate reference system. Defaults to 'EPSG:4326'.
    """
    if region is None:
        region = ee.Geometry.Rectangle([-180, -90, 180, 90])  # Default to global ROI

    task = ee.batch.Export.image.toDrive(
        image=image.clip(region),
        description=description,
        folder='GEE_Exports',
        fileNamePrefix=description,
        region=region.bounds(),
        scale=scale,
        crs=crs,
        maxPixels=1e13
    )
    task.start()
    print(f"📤 Export started: {description}")

def download_image_single(image, region, scale, crs='EPSG:4326', output_dir='./'):
    """
    Download a single Earth Engine image as GeoTIFF.

    Args:
        image (ee.Image): The Earth Engine image to download.
        region (ee.Geometry, optional): Clipping region. Defaults to global 'roi' if None.
        filename (str): Output file name.
        output_dir (str): Directory to save the downloaded image.
        scale (int): Resolution in meters.
        crs (str): Coordinate reference system. Defaults to 'EPSG:4326'.
    """

    os.makedirs(output_dir, exist_ok=True)
    
    geemap.download_ee_image(
        image=image.clip(region),
        region=region,
        scale=scale,
        crs=crs,
        filename="output.tif"
    )
    print(f"📥 Image Downloaded Successfully.")

def download_image_tiles(image, region, scale, crs='EPSG:4326', output_dir='./', prefix="Image_", rows=2, cols=2, delta=0):
    """
    Download image tiles from an Earth Engine image using a mesh grid.

    Args:
        image (ee.Image): Earth Engine image to download.
        region (ee.Geometry): Region to generate the mesh over.
        output_dir (str): Directory to save tiles.
        prefix (str): Prefix for tile file names. If None, use image id or description.
        scale (int): Resolution in meters.
        crs (str): Coordinate reference system. Defaults to 'EPSG:4326'.
        rows (int): Number of rows in the mesh grid.
        cols (int): Number of columns in the mesh grid.
        delta (float): Optional padding for tiles.
    """
    grids = geemap.fishnet(region, rows=rows, cols=cols, delta=delta)

    tiles_dir = os.path.join(os.path.abspath(output_dir), "tiles")
    #os.makedirs(tiles_dir, exist_ok=True)

    geemap.download_ee_image_tiles(
        image=image,
        features=grids,
        out_dir=tiles_dir,
        prefix=prefix,
        crs=crs,
        scale=scale
    )
    print(f"📥 Image tiles saved to: {tiles_dir}")
