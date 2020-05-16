import os,glob
import whitebox

wbt = whitebox.WhiteboxTools()

folder = '/media/cak/D/KD/KD/Basins/SHP/Havzalar/Havza_ED50'

wbt.set_working_dir(folder)
files = glob.glob1(folder,'*.shp')
dem = '/media/cak/D/KD/KD/Basins/SHP/Havzalar/DEM_ED50_re.tif'
pol = '/media/cak/D/KD/KD/Basins/SHP/Havzalar/Havza_ED50/Havza_Ad_Akarçay Havzası.shp'



wbt.clip_raster_to_polygon(dem,pol,'at.tif',maintain_dimensions=False)