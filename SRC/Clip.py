import os, glob
import whitebox
import rasterio
from rasterio.features import shapes as shp
import geopandas as gpd

wbt = whitebox.WhiteboxTools()

folder = '/media/cak/D/KD/KD/Basins/SHP/Havzalar/DEM'
hes = '/media/cak/D/KD/KD/Basins/SHP/DSI_Hes_ED50_edit.shp'


def raster2polygon(file, path):
    mask = None
    with rasterio.open(os.path.join(path, file)) as src:
        image = src.read(1)  # first band
        results = (
            {'properties': {'raster_val': v}, 'geometry': s}
            for i, (s, v)
            in enumerate(
            shp(image, mask=mask, transform=src.transform)))
    geoms = list(results)
    boundary = shp(geoms[0]['geometry'])
    gpd_polygonized_raster = gpd.GeoDataFrame.from_features(geoms)
    # Filter nodata value
    gpd_polygonized_raster = gpd_polygonized_raster[gpd_polygonized_raster['raster_val'] > 0]
    # Convert to geojson
    gpd_polygonized_raster.crs = 'epsg:23036'
    gpd_polygonized_raster.to_file(
        driver='ESRI Shapefile', filename=os.path.join(path, "basins.shp"))


# Recursively calculate flow direction, accumulation for all basins
def full_work_flow(folder):
    root_dir = os.path.abspath(folder)
    for item in os.listdir(root_dir):
        item_full_path = os.path.join(root_dir, item)
        wbt.set_working_dir(item_full_path)
        try:
            os.remove('dem.tif')
            os.remove('acc.tif')
            os.remove('dir.tif')
        except:
            pass

        files = glob.glob1(item_full_path, '*.tif')
        wbt.breach_depressions(os.path.join(item_full_path, files[0]), "DEM_breach.tif")
        wbt.fill_depressions("DEM_breach.tif", "DEM_fill.tif")
        wbt.flow_accumulation_full_workflow(
            "DEM_fill.tif", "DEM_out.tif", "Flow_dir.tif", "Flow_acc.tif", log=False)
        wbt.extract_streams("Flow_acc.tif", "streams.tif", threshold=-1)
        basin = glob.glob1(item_full_path, '*.shp')
        wbt.clip(hes, basin[0], 'at.shp')
        wbt.snap_pour_points('at.shp', "Flow_acc.tif",
                             "snap_point.shp", snap_dist=10000)
        wbt.watershed("Flow_dir.tif", "snap_point.shp", "Watershed.tif")
        raster2polygon("Watershed.tif", item_full_path)
        print(files[0])


full_work_flow(folder)
