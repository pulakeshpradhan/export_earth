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

## Export time series to pandas DataFrame
import pandas as pd
import numpy as np
def export_time_series_to_df(
    collection,
    band_names,
    region=None,
    scale=1000,
    reducer='mean',
    roi=ee.Geometry.Rectangle([-180, -90, 180, 90])):
    """
    Convert Earth Engine image collection to pandas DataFrame with reducer option.

    Args:
    collection (ee.ImageCollection): The Earth Engine image collection to process.
    band_names (list): List of band names to include in the DataFrame.
    region (ee.Geometry, optional): Region to clip the images. Defaults to global 'roi' if None.
    scale (int): Resolution in meters for the reducer.
    reducer (str): Reducer to apply. Options: 'mean', 'sum', 'min', 'max', 'median'.

    Returns:
    pd.DataFrame: A pandas DataFrame containing the time series data.
    """
    if region is None:
        region = roi  # Ensure you have defined roi in your script

    # Select reducer
    if reducer == 'mean':
        ee_reducer = ee.Reducer.mean()
    elif reducer == 'sum':
        ee_reducer = ee.Reducer.sum()
    elif reducer == 'min':
        ee_reducer = ee.Reducer.min()
    elif reducer == 'max':
        ee_reducer = ee.Reducer.max()
    elif reducer == 'median':
        ee_reducer = ee.Reducer.median()
    else:
        raise ValueError(f"Unsupported reducer: {reducer}")

    def extract(img):
        stats = img.reduceRegion(ee_reducer, region, scale, maxPixels=1e13)
        return ee.Feature(None, stats).set('date', img.get('system:time_start'))

    features = collection.map(extract)
    data = features.getInfo()['features']

    # Convert the extracted data to a pandas DataFrame
    df = pd.DataFrame([
        {'date': pd.to_datetime(f['properties']['date'], unit='ms'),
         **{k: v for k, v in f['properties'].items() if k != 'date'}}
        for f in data
    ])

    # Add missing bands
    for band in band_names:
        if band not in df.columns:
            df[band] = np.nan

    return df





## Export time series to Google Drive as CSV
def export_time_series_to_drive(
    collection, 
    *,
    region, 
    scale=1000, 
    export_folder='RGEE', 
    export_filename='lst_day_monthly',
    reducer='mean'):
    """
    Extracts time series as FeatureCollection and exports to Google Drive as CSV.

    Args:
        collection (ee.ImageCollection): The Earth Engine image collection to process.
        region (ee.Geometry): Region to clip the images.
        scale (int): Resolution in meters for the reducer.
        export_folder (str): Google Drive folder to save the exported CSV.
        export_filename (str): Name of the exported CSV file.
        reducer (str): Reducer to apply. Options: 'mean', 'sum', 'min', 'max', 'median'.

    Returns:
        None
    """
    # Select reducer
    if reducer == 'mean':
        ee_reducer = ee.Reducer.mean()
    elif reducer == 'sum':
        ee_reducer = ee.Reducer.sum()
    elif reducer == 'min':
        ee_reducer = ee.Reducer.min()
    elif reducer == 'max':
        ee_reducer = ee.Reducer.max()
    elif reducer == 'median':
        ee_reducer = ee.Reducer.median()
    else:
        raise ValueError(f"Unsupported reducer: {reducer}")

    def extract(img):
        stats = img.reduceRegion(ee_reducer, region, scale, maxPixels=1e13)
        return ee.Feature(None, stats).set('date', img.date().format('YYYY-MM-dd'))
    
    timeseries_fc = collection.map(extract)
    task = ee.batch.Export.table.toDrive(
        collection=timeseries_fc,
        description=f'{export_filename}_CSV',
        folder=export_folder,
        fileNamePrefix=export_filename,
        fileFormat='CSV'
    )
    task.start()
    print(f"📤 Export task for {export_filename} started.")
