#!/usr/bin/env python
# coding: utf-8

# In[ ]:


from sentinelsat import SentinelAPI, read_geojson

# Set up the SentinelAPI with your Copernicus Open Access Hub credentials
api = SentinelAPI('username', 'password', 'https://scihub.copernicus.eu/dhus')

# Define the AoI as a GeoJSON file (polygon)
aoi_geojson = r'path_to_saved_file.geojson'
footprint = read_geojson(aoi_geojson)

# Define the search parameters for the Sentinel-2 image
start_date = '2020-01-11'
end_date = '2020-30-11'
product_type = 'S2MSI2A'    # if you choose S2MSI1C, then atmospheric correction need to be considered (i.e., SR)!
cloud_cover = (0, 5)  # Maximum allowed cloud cover percentage

# Search for available Sentinel-2 scenes that match the search parameters
products = api.query(footprint, date=(start_date, end_date), platformname='Sentinel-2', producttype=product_type, cloudcoverpercentage=cloud_cover)

# Download the first available scene (modify as needed for multiple scenes)
if len(products) > 0:
    # Get the product ID of the first scene
    product_id = list(products.keys())[0]

    # Download the product
    api.download(product_id, directory_path='path_to_save.jpg2')
    print("Download completed.")
else:
    print("No scenes founded")



# In[ ]:


import rasterio
import numpy as np

# Specify the paths to the NIR and RED bands of Sentinel-2 imagery, considering having only one imagery 
# (one scence or multiple merged scences for big areas)
nir_path = r'path_to_saved_file.jp2'
red_path = r'path_to_saved_file.jp2'

# Open the NIR and RED bands using rasterio
with rasterio.open(nir_path) as nir_dataset, rasterio.open(red_path) as red_dataset:
    nir_band = nir_dataset.read(1)
    red_band = red_dataset.read(1)

# Calculate NDVI
ndvi = (nir_band - red_band) / (nir_band + red_band)

# Mask out invalid or no-data values
ndvi = np.ma.masked_invalid(ndvi)

# Apply threshold to identify barren land
barren_mask = ndvi < 0.1

# Calculate the total area of "barren" land
total_barren_area = np.sum(barren_mask) * 10* 10/ 1000000  # in square kilometers

# Calculate the average total area of "barren" land 
average_barren_area = total_barren_area / np.count_nonzero(barren_mask)

print(average_barren_area)

#save the NDVI image to a file
output_path = r'path_to_sav.jpg2'
with rasterio.open(output_path, 'w', nir_dataset.profile) as output_dataset:
    output_dataset.write(ndvi, 1)

