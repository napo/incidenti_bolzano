#!/usr/bin/env python
# coding: utf-8
import geopandas as gpd
from owslib.wfs import WebFeatureService
import os
wfs_url="http://sit.comune.bolzano.it/geoserver/wfs?service=WFS"
wfs = WebFeatureService(url=wfs_url, version='2.0.0')
layers = list(wfs.contents)
incidenti = []
dest = "data"
docs = "docs"
for layer in layers:
    if layer.find('ciden') > -1:
        incidenti.append(layer)
for incidente in incidenti:
    response = wfs.getfeature(typename=incidente)
    data = gpd.read_file(response)
    data.crs="epsg:25832"
    data = data.to_crs(epsg=4326)
    data['DTINCID']=data['DTINCID'].astype(str)
    data['ANNOINC'] = data['ANNOINC'].astype(int)
    data['NRINCID'] = data['NRINCID'].astype(int)
    data.DTINCID =data.DTINCID.apply(lambda x: x.replace(' 00:00:00+00:00',""))
    data['lon'] = data.geometry.x
    data['lat'] = data.geometry.y
    data.fillna("informazione non disponibile",inplace=True)
    data['lon'] = data.geometry.x
    data['lat'] = data.geometry.y
    name = incidente.replace("Cartografia:view_","")
    data.to_file("data" + os.sep + name + ".geojson",driver="GeoJSON")
    del data['geometry']
    data.to_csv("data" + os.sep + name + ".csv",index=False)
    data.to_excel(dest + os.sep + name + ".xlsx",index=False)

