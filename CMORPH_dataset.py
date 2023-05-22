#!/usr/bin/env python
# coding: utf-8

# In[ ]:


import requests
import pandas as pd
import xarray as xr
import netCDF4 as nc

# Specify the base URL for CMORPH dataset (parameters: daily precipitation, year=2020, month=March)
base_url = 'https://www.ncei.noaa.gov/data/cmorph-high-resolution-global-precipitation-estimates/access/daily/0.25deg/2020/03'

# Initialize an empty list to store the downloaded datasets
datasets = []

# Loop through the dataset URLs
for url in dataset_urls:
    # Download the CMORPH dataset
    dataset = xr.open_dataset(url)

    # Append the downloaded dataset to the list
    datasets.append(dataset)
    
    # Merge the CMORPH datasets along the time dimension
    merged_dataset = xr.concat(datasets, dim='time')
    
    # Specify the path to save the merged dataset
    output_file = r'path_to_save.nc'
    
    # Save the merged dataset to a NetCDF file
    merged_dataset.to_netcdf(output_file)
    
    # Print the merged dataset information
    print(merged_dataset)

# Close the CMORPH datasets
for dataset in datasets:
    dataset.close()


# In[ ]:


#to read metadat and list of dataset varaibles
# path to the merged CMORPH data (NetCDF file)
file_path= r'path_to_saved_file.nc'

# Open the NetCDF file
dataset=xr.open_dataset(file_path)
# get & Print the list of variables of the dataset
variable_list = list(dataset.variables)
print("Variables in the NetCDF file:")
print(dataset)


# In[ ]:


#estimate the avaerage total rainfall from merged file
file= r'path_to_saved_file.nc'

# Define the latitude and longitude ranges for Santa Cruz province
latitude_range = slice(-53, -47)  # give a latitude range for Santa Cruz: -53 to -47 degrees
longitude_range = slice(-74, -68)  # give a longitude range for Santa Cruz: -74 to -68 degrees

dataset = nc.Dataset(file,'r')
rainfall = dataset['cmorph']
march_rainfall = rainfall[2, latitude_range, longitude_range]
total_rainfall = march_rainfall.sum()
average_rainfall = total_rainfall / march_rainfall.size
print("Average rainfall for March.2020:", average_rainfall, "mm")

# Close the CMORPH NetCDF file
dataset.close()

