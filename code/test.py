import numpy as np
import pandas as pd
from config import *
import math
KG='..//data//'


def match():
    safegraph=pd.read_csv(KG+'raw//New York')
    poi=pd.read_json(KG+'poi.json')
    aoi=pd.read_json(KG+'aoi.json')
    print(safegraph .head(),poi.head())


def poi_save():
    poi=pd.read_json(KG+'poi.json')

    name,addr,lat,lon= [], [], [], []
    cate, oid = [], []

    poi_save=pd.DataFrame()

    name=poi['name']
    lat=poi['latitude']
    lon=poi['longitude']
    for line in poi['categories']:
        value=list(line.values())
        value=';'.join(value)
        cate.append(value)
    oid=poi['id']
    inside=poi['in']
    for line in poi['tag']:
        addr_str = ''
        for item in line.keys():
            if item in addr_keys:
                addr_str = addr_str + line[item] + ' '
        addr.append(addr_str)
    poi_save["name"] = name
    poi_save['address'] = addr
    poi_save['latitude'] = lat
    poi_save['longitude'] = lon
    poi_save['categories'] = cate
    poi_save['id'] = oid
    poi_save['in']= inside
    poi_save.to_csv(KG+'poi_save.csv')
    poi_save.to_json(KG+'poi_save.json')

def node_only_cor():
    data=pd.read_json(r"D:\Program\osm\node\node.json",lines=True)
    data_save=pd.DataFrame()
    data_save['id']=data['id']
    data_save['lat']=data['lat']
    data_save['lon']=data['lon']
    data_save.to_json(r"D:\Program\osm\node\node_only_cor.json")
    data_save.to_excel(r"D:\Program\osm\node\node_only_cor.xlsx")
    print(data_save.head())

def aoi_save():
    aoi = pd.read_json(KG + 'aoi.json')
    name, addr, lat, lon = [], [], [], []
    cate, oid = [], []
    aoi_save = pd.DataFrame()

    name = aoi['name']
    # cov = aoi['coverage']
    # cor_only=pd.read_json(r"D:\Program\osm\node\node_only_cor.json")
    # for line in cov:
    #     id=[]
    #     for dictionary in line :
    #         id.append(','.join(list(dictionary.values())))
    #     latt = cor_only[cor_only['id'].isin(id)]['lat']
    #     print(latt)
    #     lonn = cor_only[cor_only['id'].isin(id)]['lon']
    #     lat.append(np.average(latt))
    #     lon.append(np.average(lonn))
    for line in aoi['categories']:
        value = list(line.values())
        value = ';'.join(value)
        cate.append(value)
    oid = aoi['id']
    for line in aoi['tag']:
        addr_str = ''
        for item in line.keys():
            if item in addr_keys:
                addr_str = addr_str + line[item] + ' '
        addr.append(addr_str)
    aoi_save["name"] = name
    aoi_save['address'] = addr
    # aoi_save['latitude'] = lat
    # aoi_save['longitude'] = lon
    aoi_save['categories'] = cate
    aoi_save['id'] = oid

    aoi_save.to_csv(KG + 'aoi_save.csv')
    aoi_save.to_json(KG + 'aoi_save.json')

def SafeGraph():
    data= pd.read_csv(KG+'SafeGraph.csv')
    SG_save = pd.DataFrame()
    inside=data['parent_placekey']
    name = data['location_name']
    lat = data['latitude']
    lon = data['longitude']
    cate= data['top_category']
    addr= data['street_address']
    oid = data['placekey']


    SG_save["name"] = name
    SG_save['address'] = addr
    SG_save['latitude'] = lat
    SG_save['longitude'] = lon
    SG_save['categories'] = cate
    SG_save['id'] = oid
    SG_save['in'] =inside

    SG_save.to_csv(KG + 'SG_save.csv')
    SG_save.to_json(KG + 'SG_save.json')

if __name__ == '__main__':
    match()
    #poi_save()
    #node_only_cor()
    #aoi_save()
    #SafeGraph()
