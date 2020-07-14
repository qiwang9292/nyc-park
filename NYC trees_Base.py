#!/usr/bin/env python
# coding: utf-8

# #NYC trees mapping

# In[1]:


import pandas as pd
import matplotlib
import numpy as np
import folium

from scipy.stats import mode
import sys
get_ipython().run_line_magic('matplotlib', 'notebook')
import matplotlib.pyplot as plt
from scipy.io import loadmat
import time
#import json


# In[2]:


df = pd.read_csv('D:/QWANG/Coding/LANGUAGES/Pandas/NYC TREES/2015-street-tree-census-tree-data.csv')
df.head(3)
df.shape


# In[3]:


###clean up the data

df=df.fillna('unknown')
df=df.replace(to_replace = 'nan', value = 'unknown')

#drop 'created_at' info
#df =df.drop(columns= ['created_at'])
#df.sample(40)


# In[4]:


center = [df['latitude'].mean(),df['longitude'].mean()]
print(center)


# ###CREATE THE MAP

# In[5]:


map_NYC = folium.Map(location = center, tiles = 'Stamen TonerBackground',zoom_start = 12)
#display(map_NYC)


# In[6]:


import branca.colormap as cm
clr = ['green','yellow','red']
linear  = cm.LinearColormap(clr,vmin=0,vmax=30000)
linear


# #read neighborhood GeoJson (TBD)

# In[7]:


###read nyc neighborhood 
data_url = 'D:/QWANG/Coding/PROJECT/NYC TREES/data/'
nyc_neighbor = f'{data_url}Neighborhood Tabulation Areas (NTA).geojson'

#import json file as geopandas dataframe
import geopandas
gdf_ne = geopandas.read_file(nyc_neighbor)
gdf_ne=gdf_ne.rename(columns={'geometry':'boundary'}).set_geometry('boundary')


#reproject to a crs
gdf_ne = gdf_ne.to_crs(epsg=4326)

#get centroid of all neighborhood
gdf_ne['centroid']=gdf_ne.centroid
#gdf_ne = gdf_ne.set_geometry('centroid')
gdf_ne.centroid

# def get_xy(pt):
#     return (pt.x,pt.y)
# ne_center=map(get_xy,gdf_ne.centroid)
# ne_center

gdf_ne["x"] = gdf_ne.centroid.map(lambda p: p.x)
gdf_ne["y"] = gdf_ne.centroid.map(lambda p: p.y)
# #gdf_ne.plot()
# #gdf_ne.geometry.name


# In[ ]:





#  ADD VECTOR LAYERS ON THE MAP

# In[13]:


###add street tree sample 
df1 = df.sample (500)

###create a group for layers
feature_group = folium.FeatureGroup(name='layers')

### add tree info as dots to feature group
for index,row in df1.iterrows():
    folium.CircleMarker([row['latitude'],row['longitude']],radius =2,fill=True,popup = row['spc_common'],
                        color=linear(row['tree_id']),fill_color=linear(row['tree_id'])
                       ).add_to(feature_group)

    
#add name label for all neighborhoods     
from folium.features import DivIcon
for index,row in gdf_ne.iterrows():
    folium.map.Marker(
        [row['y'],row['x']],
        icon=DivIcon(
            icon_size=(150,36),
            icon_anchor=(0,0),
            html='<div style="font-size: 8pt;background-color:black;color:white">%s</div>'%row['ntaname'],
            )
        ).add_to(feature_group)


###define neighbhorhood boundary style
def nei_style(feature):
    return {
        'fillOpacity':0.5,
        'fill':False,
        'weight':1.5,
        'color': 'magenta'
    }

### add neighborhood GeoJson to group
neighborhood = folium.GeoJson(
    nyc_neighbor,
    name = 'nyc neighborhood',
    style_function=nei_style,
    
    )
neighborhood.add_to(feature_group)





## add feature group to the map
feature_group.add_to(map_NYC)


# ### test add a pop up
# 
# 
# folium.Marker (center,
#               popup='this is NYC',
#               tooltip = '<strong>what is this</strong>'
#              ).add_to(map_NYC)
# 

# plot map as html

# In[14]:


#folium.LayerControl().add_to(map_NYC)
map_NYC


# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[ ]:





# In[10]:


map_NYC.save('nyc_tree.html')

