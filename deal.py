import json
import csv
import os
import random
import numpy as np
import pandas as pd
import datetime
from link import *
from config import *

node_tag=[]
way_tag=[]

#检查路径是否存在
def check_path(path):
    if not os.path.exists(path):
        os.makedirs(path)

#OSM数据结构中node处理
def node_deal(path_node,path_way):
    print("deal with node\n")

    #读取有name的node
    file_read=pd.read_json(path_node+ "node.json")
    #读取cor
    #读取标签
    # 闭环way含name
    file_write2 = open(path_node + 'NewYork_node2.json', mode='wb')
    with open(path_node + 'node.json', mode='rb') as file_read:
        count = 0
        for line in file_read:
            line = line.replace('\n'.encode(), ''.encode())
            info = json.loads(line)
            if 'tag' in info and type(info['tag']) is list and 'nd' in info and type(info['nd']) is list:
                ff = 0
                if info['nd'][0] == info['nd'][len(info['nd']) - 1]:
                    for item in info['tag']:
                        if 'name' in item.values():
                            ff = 1
                if ff == 1:
                    elem = json.dumps(info)
                    file_write2.write((elem + "\n").encode())
                count += 1
    file_write2.close()
    df = pd.read_json(path_node + 'NewYork_node2.json', encoding='utf-8', lines=True)
    df.to_csv(path_node + 'NewYork_node2.csv')

    #清除k,v,并获取tag
    file_write2 = open(path_node+'NewYork_node_clear.json', mode='wb')
    with open(path_node+'node.json', mode='rb') as file_read:
        count = 0
        for line in file_read:
            line = line.replace('\n'.encode(), ''.encode())
            info = json.loads(line)
            if 'tag' in info and type(info['tag']) is list:
                for item in info['tag']:
                    key= item['k']
                    val= item['v']
                    item.clear()
                    item[key]=val
            elem = json.dumps(info)
            file_write2.write((elem + "\n").encode())
    file_write2.close()
    df = pd.read_json(path_node+'NewYork_node_clear.json', encoding='utf-8', lines=True)
    df.to_csv(path_node+'NewYork_node_clear.csv')

    #仅包含cor
    file_write2 = open(path_node+'NewYork_node_cor.json', mode='wb')
    with open(path_node+'node.json', mode='rb') as file_read:
        count = 0
        for line in file_read:
            line = line.replace('\n'.encode(), ''.encode())
            info = json.loads(line)
            if 'tag' in info:
                info.pop('tag')
            elem = json.dumps(info)
            file_write2.write((elem + "\n").encode())
    file_write2.close()
    df = pd.read_json(path_node+'NewYork_node_cor.json', encoding='utf-8', lines=True)
    df.to_csv(path_node+'NewYork_node_cor.csv')

#OSM数据结构中way处理
def way_deal(path_node,path_way):
    print('deal with way\n')
    #闭环way含name
    file_write2 = open(path_way+'NewYork_way2.json', mode='wb')
    with open(path_way+'way.json', mode='rb') as file_read:
        count = 0
        for line in file_read:
            line = line.replace('\n'.encode(), ''.encode())
            info = json.loads(line)
            if 'tag' in info and type(info['tag']) is list and 'nd' in info and type(info['nd']) is list:
                ff = 0
                if info['nd'][0] == info['nd'][len(info['nd'])-1]:
                    for item in info['tag']:
                        if 'name' in item.values():
                            ff = 1
                if ff == 1:
                    elem = json.dumps(info)
                    file_write2.write((elem + "\n").encode())
                count += 1
    file_write2.close()
    df = pd.read_json(path_way+'NewYork_way2.json', encoding='utf-8', lines=True)
    df.to_csv(path_way+'NewYork_way2.csv')

    #闭环way仅name
    file_write2 = open(path_way+'NewYork_way_name.json', mode='wb')
    with open(path_way+'way.json', mode='rb') as file_read:
        count = 0
        for line in file_read:
            line = line.replace('\n'.encode(), ''.encode())
            info = json.loads(line)
            if 'tag' in info and type(info['tag']) is list:
                for item in info['tag']:
                    if 'name' in item.values():
                        info['name'] = item['v']
                        print(info['name'])
                        info.pop('tag')
                elem = json.dumps(info)
                file_write2.write((elem + "\n").encode())
            count += 1
    file_write2.close()
    df = pd.read_json(path_way+'NewYork_way_name.json', encoding='utf-8', lines=True)
    df.to_csv(path_way+'NewYork_way_name.csv')

    #nd转化为坐标序列
    #第0分别为标签和行号
    #1,2,3列为id，lat，lon
    f_node = open(path_node+r'NewYork_node_cor.csv', 'r',encoding='utf-8')
    node_reader = csv.reader(f_node)
    node_reader=list(node_reader)

    #第0行列为标签和序号
    #第1行开始为数据
    #2，3，4列为id，nd，name
    #[行][列][格中序号]
    f_way = open(path_way+'NewYork_way_name.csv', 'r', encoding='utf-8')
    way_reader =csv.reader(f_way)
    way_reader=list(way_reader)

    f= open(path_way+'NewYork_way_name_axis.csv', 'w', encoding='utf-8')
    writer = csv.writer(f)
    writer.writerow(way_reader[0])
    numall=0
    for i in range(1,len(way_reader)):
        nn = way_reader[i][3].split(',')
        numall+=len(nn)
    print(numall)

    num=0
    for i in range(1,len(way_reader)):
        #i对应的行
        nn = way_reader[i][3].split(',')
        lon_lat = []
        ff=0
        for node in nn:#读取每一个nd
            num+=1
            for j in range(1,len(node_reader)):
                if int(node_reader[j][1])==int(node):
                    lon_lat.append([node_reader[j][3],node_reader[j][2]])
                    print(num/numall)
                    break
                elif int(node_reader[j][1])>int(node):
                    print(node_reader[j][1],node)
                    print(num / numall)
                    ff=1
                    break
            if ff==1:
                break
        if ff==0:
            way_reader[i].append(lon_lat)
            writer.writerow(way_reader[i])
    f.close()
    f_way.close()
    f_node.close()

    file_node = pd.read_csv(path_node+r'NewYork_node_cor.csv')
    file_way = pd.read_csv(path_way+r'NewYork_way_area_name.csv')
    for i in range(file_way.shape[0]):
        file_way.at[i, 'nd'] = file_way['nd'][i].split(',')
    file_way['lon_lat'] = ''
    numall = 0
    num = 0
    for line in file_way['nd']:
            numall += len(line)
    print(numall)
    wcount = 0
    for line in file_way['nd']:
        for item in line:
            ff = 0
            lon_lat = []
            ncount = 0
            for nid in file_node['id']:
                if int(nid) == int(item):
                    lon_lat.append([file_node.loc[ncount, 'lon'], file_node.loc[ncount, 'lat']])
                    num += 1
                    print(num / numall)
                    break
                elif int(nid) > int(item):
                    print(nid, item)
                    ff = 1
                    break
                ncount += 1
            if ff == 1:
                break
        if ff == 0:
            print(num / numall)
            file_way.at[wcount, 'lon_lat'] = lon_lat
        wcount += 1
    file_way.to_csv(path_way+r'NewYork_way_area_name_axis.csv')

#OSM数据结构中relation处理
def relation_deal(path_relation):
    file_write2 = open(path_relation+r'NewYork_relation3.json', mode='wb')
    # with open(path_relation+r'relation.json', mode='rb') as file_read:
    #     count = 0
    #     for line in file_read:
    #         line = line.replace('\n'.encode(), ''.encode())
    #         info = json.loads(line)
    #         if 'tag' in info and type(info['tag']) is list:
    #             ff = 0
    #             for item in info['tag']:
    #                 if 'area' in item.values():
    #                     ff = 1
    #             if ff == 1:
    #                 elem = json.dumps(info)
    #                 file_write2.write((elem + "\n").encode())
    #             count += 1
    file_write2.close()
    # df = pd.read_json(path_node+'NewYork_relation3.json', encoding='utf-8', lines=True)
    # df.to_csv(path_node+'NewYork_relation3.csv')

#OSM数据结构中tag处理
def search_in_nodes(a,data):  # 寻找node_id
    res = []
    for i in data:
        for j in i['tag']:
            if j == a:
                res.append(i['id'])
    return res
def tag_deal(path_node,path_way,path_relation,path_KG):
    f1 = open(path_node+"NewYork_node2.json", 'r', encoding='UTF-8')
    f2 = open(path_way+"NewYork_way2.json", 'r', encoding='utf-8')
    data1 = []  # node数据列表
    data2 = []  # way数据列表
    tags = []  # 所有的tags
    element = []  # 目标csv中每一行的数据
    num = 0
    for i in f1.readlines():
        j1 = json.loads(i)
        data1.append(j1)
    nodes_length = data2.__len__()
    for i in f2.readlines():
        j2 = json.loads(i)
        data2.append(j2)
    ways_length = data2.__len__()
    data = data1 + data2
    length = data.__len__()
    for i in data:
        print('tags读取完成度', 100 * data.index(i) / length, '%')
        for j in i['tag']:  # j为tag列表中的元素，字典数据类型
            if j not in tags:
                tags.append(j)
    print(tags.__len__())

    header = ['tags_k', 'tags_v', 'node_in', 'way_in']
    print('开始写入csv文件')
    f3 = open(path_KG+"tags_based_on_k_and_v.csv", 'w', encoding='utf-8', newline='')
    writer = csv.writer(f3)
    writer.writerow(header)
    for i in tags:  # i类型为字典
        element = [i['k'], i['v']]
        if not search_in_nodes(i,data1):
            continue
        else:
            element.append(search_in_nodes(i,data1))
        if not search_in_nodes(i,data2):
            continue
        else:
            element.append(search_in_nodes(i,data2))
        writer.writerow(element)
        num = num + 1
        print('写入进程:', 100 * tags.index(i) / tags.__len__(), '%    已找到配对数：', num)
    f1.close()
    f2.close()
    f3.close()

#判断内外关系
def judge_in(path_node,path_way,path_KG):
    f1 = open(path_node+"NewYork_node2.json", 'r', encoding='UTF-8')
    f2 = open(path_way+"NewYork_way_save_keys_building_clear_cor.json", 'r', encoding='UTF-8')
    data1 = []  # node
    data2 = []  # way
    for i in f1.readlines():
        j1 = json.loads(i)
        data1.append(j1)
    length = data1.__len__()
    success_node = 0
    for i in f2.readlines():
        j2 = json.loads(i)
        data2.append(j2)
    for j1 in data1:
        j1['in_ways_id'] = []
        lat = j1['lat']
        lon = j1['lon']
        print('完成度:', 100 * data1.index(j1) / length, '%')
        for j2 in data2:
            if isInRegion_lon_lat(lat, lon, j2['cor']) == True:
                j1['in_ways_id'].append(j2['id'])
                print('找到一个所在区域')
                success_node += 1

    f1.close()
    f2.close()
    f1 = open(path_KG+"NewYork_way_save_keys_building_clear_cor_judge.json", 'w', encoding='UTF-8')
    for i in data1:
        json.dump(i, f1)
        f1.write('\n')
    f1.close()
    print('共有', length, '个节点')
    print('共有', data2.__len__(), '个区域')
    print('成功匹配了', success_node, '个地区')
#提取POI
def POI_find(path_node,path_way,path_relation,path_KG):
    # 分割tag
    keys = way_save_keys
    print(keys)
    way_keys = pd.DataFrame()
    with open(path_way + r'NewYork_way2.json', 'r') as f:
        for line in f.readlines():
            info = json.loads(line)
            ff = 0
            if 'tag' in info:
                for item in info['tag']:
                    for key in keys:
                        if key in item.values():
                            ff = 1
            if ff == 1:
                df_nested_list = pd.json_normalize(info, record_path=['tag'])
                info.pop('tag')
                df = dict(zip(df_nested_list['k'], df_nested_list['v']))
                d = {**info, **df}
                elem = json.dumps(d)
                df_new = pd.json_normalize(elem)
                way_keys = way_keys.append(df_new, ignore_index=True)
    way_keys.drop_duplicates(inplace=True)
    way_keys.tocsv(path_way + r'NewYork_way_save_keys_clear.csv')


    # 清理k, v
    file_write2 = open(r'D:\Program\osm\test\output\node\judged nodes\judge_clear0.json', 'wb')
    with open(r'D:\Program\osm\test\output\node\judged nodes\judge_clear.json', 'rb') as file:
        count = 0
        for line in file:
            line = line.replace('\n'.encode(), ''.encode())
            info = json.loads(line)
            if 'tag' in info:
                for item in info['tag']:
                    if 'k' in item.values():
                        key = item['k']
                        val = item['v']
                        item.clear()
                        item[key] = val
                        ff = 1
            elem = json.dumps(info)
            file_write2.write((elem + "\n").encode())
            count += 1
            print(count)
    file_write2.close
    df = pd.read_json(r'D:\Program\osm\test\output\node\judged nodes\judge_clear0.json', encoding='utf-8', lines=True)
    df.to_csv(r'D:\Program\osm\test\output\node\judged nodes\judge_clear0.csv')

    # 对way清理
    file_write2 = open(r'D:\Program\osm\test\output\node\judged nodes\way_clear.json', 'wb')
    with open(r'D:\Program\osm\test\easy_deal\NewYork_way_save_keys.json', 'rb') as file:
        count = 0
        for line in file:
            line = line.replace('\n'.encode(), ''.encode())
            info = json.loads(line)
            if 'tag' in info:
                for item in info['tag']:
                    if 'k' in item.keys():
                        key = item['k']
                        val = item['v']
                        item.clear()
                        item[key] = val
            elem = json.dumps(info)
            file_write2.write((elem + "\n").encode())
            count += 1
            print(count)
    file_write2.close
    df = pd.read_json(r'D:\Program\osm\test\output\node\judged nodes\way_clear.json', encoding='utf-8', lines=True)
    df.to_csv(r'D:\Program\osm\test\output\node\judged nodes\way_clear.csv')

    # 展开tag
    with open(r'D:\Program\osm\test\easy_deal\NewYork_way_save_keys.json', 'rb') as file:
        count = 0
        for line in file:
            line = line.replace('\n'.encode(), ''.encode())
            info = json.loads(line)
            df_nested_list = pd.json_normalize(info, record_path=['tag'])
            print(df_nested_list)

    # json转csv
    df = pd.read_json(r'D:\Program\osm\test\output\way\NewYork_way_save_keys_historic_clear_cor.json', lines=True)
    data_csv = pd.DataFrame()
    data_csv['id'] = df['id']
    data_csv['cor'] = df['cor']
    print(data_csv)
    data_csv.to_csv(r'D:\Program\osm\test\output\way\NewYork_way_save_keys_historic_clear_cor.csv')
    print(df)
    print(df)
    dnf = pd.read_json(r'D:\Program\osm\test\NewYork_node2.json', lines=True)
    dnf.to_csv(r'D:\Program\osm\test\NewYork_node4.csv')
    print(dnf)


    # 清理k, v
    file_write2 = open(r'D:\Program\osm\test\output\node\judged nodes\judge_clear0.json', 'wb')
    with open(r'D:\Program\osm\test\output\node\judged nodes\judge_clear.json', 'rb') as file:
        count = 0
        for line in file:
            line = line.replace('\n'.encode(), ''.encode())
            info = json.loads(line)
            if 'tag' in info:
                for item in info['tag']:
                    if 'k' in item.values():
                        key = item['k']
                        val = item['v']
                        item.clear()
                        item[key] = val
                        ff = 1
            elem = json.dumps(info)
            file_write2.write((elem + "\n").encode())
            count += 1
            print(count)
    file_write2.close
    df = pd.read_json(r'D:\Program\osm\test\output\node\judged nodes\judge_clear0.json', encoding='utf-8', lines=True)
    df.to_csv(r'D:\Program\osm\test\output\node\judged nodes\judge_clear0.csv')

    # 对way清理
    file_write2 = open(r'D:\Program\osm\test\output\node\judged nodes\way_clear.json', 'wb')
    with open(r'D:\Program\osm\test\easy_deal\NewYork_way_save_keys.json', 'rb') as file:
        count = 0
        for line in file:
            line = line.replace('\n'.encode(), ''.encode())
            info = json.loads(line)
            if 'tag' in info:
                for item in info['tag']:
                    if 'k' in item.keys():
                        key = item['k']
                        val = item['v']
                        item.clear()
                        item[key] = val
            elem = json.dumps(info)
            file_write2.write((elem + "\n").encode())
            count += 1
            print(count)
    file_write2.close
    df = pd.read_json(r'D:\Program\osm\test\output\node\judged nodes\way_clear.json', encoding='utf-8', lines=True)
    df.to_csv(r'D:\Program\osm\test\output\node\judged nodes\way_clear.csv')

    # 展开tag
    with open(r'D:\Program\osm\test\easy_deal\NewYork_way_save_keys.json', 'rb') as file:
        count = 0
        for line in file:
            line = line.replace('\n'.encode(), ''.encode())
            info = json.loads(line)
            df_nested_list = pd.json_normalize(info, record_path=['tag'])
            print(df_nested_list)

    # json转csv
    df = pd.read_json(r'D:\Program\osm\test\output\way\NewYork_way_save_keys_historic_clear_cor.json', lines=True)
    data_csv = pd.DataFrame()
    data_csv['id'] = df['id']
    data_csv['cor'] = df['cor']
    print(data_csv)
    data_csv.to_csv(r'D:\Program\osm\test\output\way\NewYork_way_save_keys_historic_clear_cor.csv')
    print(df)
    print(df)
    dnf = pd.read_json(r'D:\Program\osm\test\NewYork_node2.json', lines=True)
    dnf.to_csv(r'D:\Program\osm\test\NewYork_node4.csv')
    print(dnf)

    # 合并json文件
    with open(r"D:\Program\osm\test\output\way\1.txt", "r") as f:
        file_list = list(f.read().split())
        print(file_list)
    for name in file_list:
        name_json = 'D:/Program/osm/test/output/node/judged nodes/NewYork_node_in_' + name + '_area.json'
        name_json2 = 'D:/Program/osm/test/output/node/judged nodes/NewYork_node_in_' + name + '_area0.json'
        file_write = open(name_json2, 'wb')
        with open(name_json, 'r') as f:
            for line in f.readlines():
                info = json.loads(line)
                df_nested_list = pd.json_normalize(info, record_path=['tag'])
                info.pop('tag')
                df = dict(zip(df_nested_list['k'], df_nested_list['v']))
                info['name'] = df['name']
                df.pop('name')

                d = {**info, **df}
                elem = json.dumps(d)
                file_write.write((elem + "\n").encode())
        file_write.close()
        cd = pd.read_json(name_json2, lines=True)
        print(cd)
        name_csv = 'D:/Program/osm/test/output/node/judged nodes/NewYork_node_in_' + name + '_area.csv'
        cd.to_csv(name_csv)
    file_write = open('D:/Program/osm/test/output/node/judged nodes/judge_normalize.json', 'wb')
    with open('D:/Program/osm/test/output/node/judged nodes/judge.json', 'rb') as f:
        for line in f.readlines():
            info = json.loads(line)
            df_nested_list = pd.json_normalize(info, record_path=['tag'])
            info.pop('tag')
            df = dict(zip(df_nested_list['k'], df_nested_list['v']))
            info['name'] = df['name']
            df.pop('name')
            d = {**info, **df}
            elem = json.dumps(d)
            file_write.write((elem + "\n").encode())
    file_write.close()
    cd = pd.read_json('D:/Program/osm/test/output/node/judged nodes/judge_normalize.json', lines=True)
    print(cd)
    name_csv = 'D:/Program/osm/test/output/node/judged nodes/judge_normalize.csv'
    cd.to_csv(name_csv)

    # 读取第一个JSON文件
    ab = pd.read_json(r'D:\Program\osm\test\output\way\amenity.json', lines=True)
    for name in file_list:
        name_str = 'D:/Program/osm/test/output/way/' + name + '.json'
        cd = pd.read_json(name_str, lines=True)
        mn = pd.concat([ab, cd], ignore_index=True)
        ab = mn
        print(name_str)
    mn.to_json(r'D:\Program\osm\test\output\way\way_cor.json')
    mn.to_csv(r'D:\Program\osm\test\output\way\way_cor.csv')

    df = pd.read_csv(r'D:\Program\osm\test\output\way\way_cor.csv')
    print(df)
    dd = pd.DataFrame()
    dd['id'] = df['id']
    dd['cor'] = df['cor']
    dd.to_csv(r'D:\Program\osm\test\output\way\way_cor_clear.csv')

    for name in file_list:
        name_json = 'D:/Program/osm/test/output/node/judged nodes/NewYork_node_in_' + name + '_area.json'
        cd = pd.read_json(name_json, lines=True)
        print(cd)
        name_csv = 'D:/Program/osm/test/output/node/judged nodes/NewYork_node_in_' + name + '_area.csv'
        cd.to_csv(name_csv)
#提取AOI
def AOI_find(path_node,path_way,path_relation):
    # 分割tag
    keys = way_save_keys
    print(keys)
    way_keys = pd.DataFrame()
    with open(path_way + r'NewYork_way2.json', 'r') as f:
        for line in f.readlines():
            info = json.loads(line)
            ff = 0
            if 'tag' in info:
                for item in info['tag']:
                    for key in keys:
                        if key in item.values():
                            ff = 1
            if ff == 1:
                df_nested_list = pd.json_normalize(info, record_path=['tag'])
                info.pop('tag')
                df = dict(zip(df_nested_list['k'], df_nested_list['v']))
                d = {**info, **df}
                elem = json.dumps(d)
                df_new = pd.json_normalize(elem)
                way_keys = way_keys.append(df_new, ignore_index=True)
    way_keys.drop_duplicates(inplace=True)
    way_keys.tocsv(path_way + r'NewYork_way_save_keys_clear.csv')
    # mn = pd.read_json(r'D:\Program\osm\test\output\way\way_cor_clear.json')
    # lat = []
    # lon = []
    # num = 0
    # for line in mn['cor']:
    #     cor = []
    #     for item in line:
    #         item = tuple(item)
    #         cor.append(item)
    #     if len(cor) < 4:
    #         x, y = 0, 0
    #         n = 0
    #         for item in cor:
    #             x += float(item[0])
    #             y += float(item[1])
    #             n += 1
    #         x, y = x / n, y / n
    #         print(x, y)
    #         num += 1
    #         lat.append(x)
    #         lon.append(y)
    #     else:
    #         num += 1
    #         poly = Polygon(cor)
    #         center = poly.centroid
    #         lat.append(center.x)
    #         lon.append(center.y)
    # mn['lon']=lon
    # mn['lat']=lat
    # mn.to_csv(r'D:\Program\osm\test\output\way\way_cor_clear0.csv')
#关系构建
def relation_build(path_node,path_way,path_relation):
    isInRegion_lat_lon(0, 0, 0)
    df = pd.read_json(r'D:\Program\osm\test\NewYork_way_area_name.json', lines=True)
    df = df.astype({'nd': 'string', 'name': 'string'})
    print(df.dtypes)
    df.to_csv(r'D:\Program\osm\test\NewYork_way_area_name.csv')
    df = pd.read_csv(r'D:\Program\osm\test\NewYork_way_area_name.csv')
    print(df.dtypes)
    print(type(df.loc[:, 'nd']))
    for i in range(1326):
        df.loc[i, 'nd'] = df.loc[i, 'nd'].replace('[', '').replace(']', '').replace('"', '').replace('"', '').replace(
            "'", '').replace('{', '').replace('}', '').replace('ref:', '')
    print(df.loc[:, 'nd'])
    df.to_csv(r'D:\Program\osm\test\NewYork_way_area_name.csv')

    # 获取addr和cate

    with open(r"D:\Program\osm\test\output\node\addr.txt", "r") as f:
        addr_list = list(f.read().split())
        print(addr_list)
    with open(r"D:\Program\osm\test\output\node\cate.txt", "r") as f:
        cate_list = list(f.read().split())
        print(cate_list)
    with open(r"D:\Program\osm\test\output\node\cate2.txt", "r") as f:
        cate_list2 = list(f.read().split())
        print(cate_list2)

    # 处理node
    data_csv = pd.DataFrame()
    data_json = pd.read_json(r'D:\Program\osm\test\output\node\judged nodes\judge_clear0.json', lines=True)
    addr = []
    cate = []
    name = []
    nid = []
    tag = data_json['tag']
    num = 0
    bool_list = ['yes', 'no']
    for line in tag:
        addr_str = ''
        cate_str = ''
        f = 0
        for item in line:
            key = list(item.keys())
            if key[0] == 'name':
                name.append(item[key[0]])
            if key[0] in addr_list:
                addr_str = addr_str + item[key[0]] + ' '
            if key[0] in cate_list and item[key[0]] not in bool_list and cate_str != item[key[0]] + ' ':
                cate_str = cate_str + item[key[0]] + ' '
                f += 1
                num += 1
        for item in line:
            key = list(item.keys())
            if key[0] in cate_list2 and item[key[0]] not in bool_list and cate_str != item[key[0]] + ' ' and f == 0:
                cate_str = cate_str + item[key[0]] + ' '
                f += 1
                num += 1
        addr.append(addr_str)
        cate.append(cate_str)
        if f >= 2:
            print(cate_str)
    for item in data_json['id']:
        nid.append('OSM-' + str(item))
    data_csv['h_name'] = name
    data_csv['h_address'] = addr
    data_csv['h_latitude'] = data_json['lat']
    data_csv['h_longitude'] = data_json['lon']
    data_csv['h_categories'] = cate
    data_csv['h_id'] = nid
    data_csv['in'] = data_json['in_ways_id']
    # print(data_csv.head(10))
    data_csv.to_csv(r'D:\Program\osm\test\output\node\judged nodes\judge_node2.csv')
    print(num)

    # 处理way
    data_json = pd.read_json(r'D:\Program\osm\test\output\node\judged nodes\way_clear.json', lines=True)
    data_csv = pd.DataFrame()

    addr = []
    cate = []
    name = []
    id = []
    tag = data_json['tag']
    num = 0
    bool_list = ['yes', 'no']
    for line in tag:
        addr_str = ''
        cate_str = ''
        f = 0
        for item in line:
            key = list(item.keys())
            if key[0] == 'name':
                name.append(item[key[0]])
            if key[0] in addr_list:
                addr_str = addr_str + item[key[0]] + ' '
            if key[0] in cate_list and item[key[0]] != 'yes':
                cate_str = cate_str + item[key[0]] + ' '
                f += 1
                num += 1
        for item in line:
            key = list(item.keys())
            if key[0] in cate_list2 and item[key[0]] not in bool_list and cate_str != item[key[0]] + ' ' and f == 0:
                cate_str = cate_str + item[key[0]] + ' '
                f += 1
                num += 1
        addr.append(addr_str)
        cate.append(cate_str)
        if f > 1:
            print(cate_str)
    for item in data_json['id']:
        id.append('OSM-' + str(item))
    print(num)
    data_csv['h_name'] = name
    data_csv['h_address'] = addr
    # data_csv['h_latitude']=data_json['lat']
    # data_csv['h_longitude']=data_json['lon']
    data_csv['h_categories'] = cate
    data_csv['h_id'] = id
    data_csv.to_csv(r'D:\Program\osm\test\output\node\judged nodes\way_clear0.csv')

    data1 = pd.read_csv(r'D:\Program\osm\test\output\node\judged nodes\way_clear0.csv')
    data2 = pd.read_csv(r'D:\Program\osm\test\output\way\way_cor_clear0.csv')
    data0 = pd.DataFrame()
    name, addr, cate, oid = [], [], [], []
    id2 = data2['id']
    for item in id2:
        n = 0
        f = 0
        for id1 in data1['h_id']:
            if str(id1) == ('OSM-' + str(item)):
                name.append(data1['h_name'][n])
                addr.append(data1['h_address'][n])
                cate.append(data1['h_categories'][n])
                oid.append('OSM-' + str(item))
                f = 1
            n += 1
        if f == 0:
            oid.append('OSM-' + str(item))
            name.append(data1['h_name'][n])
            addr.append(data1['h_address'][n])
            cate.append(data1['h_categories'][n])
            print(f)
    data0["h_name"] = name
    data0['h_address'] = addr
    data0['h_latitude'] = data2['lat']
    data0['h_longitude'] = data2['lon']
    data0['h_categories'] = cate
    data0['h_id'] = oid
    data0.to_csv(r'D:\Program\osm\test\output\node\judged nodes\way_cor.csv')

    judge_node = pd.read_csv(path_node + 'judge_node.csv')
    node = pd.read_csv(path_node + 'judge_node.csv')
    way = pd.read_csv(path_way + 'judge_way.csv')
    judge0 = pd.DataFrame()

    # 筛选cate
    m=0
    for item in judge_node['h_categories']:
        if type(item) is str:
            judge0.loc[m] = judge_node.loc[n]
            print(item, type(item))
            m += 1
        n += 1
    judge0['h_name'] = node['h_name']
    judge0['h_address'] = node['h_address']
    judge0['h_latitude'] = node['h_latitude']
    judge0['h_longitude'] = node['h_longitude']
    judge0['h_categories'] = node['h_categories']
    judge0['h_id'] = node['h_id']
    judge0['in'] = node['in']
    judge0.to_csv(path_node + 'judge_node_cate.csv')

    # 判断关系0, 1, 2, 3
    h_name, h_address, h_latitude, h_longitude, h_categories, h_id, h_in = [], [], [], [], [], [], []
    t_name, t_address, t_latitude, t_longitude, t_categories, t_id, relation = [], [], [], [], [], [], []
    m = 0
    for item in node['in']:
        if len(item) > 2:
            item = item.replace('[', '').replace(']', '').replace("'", '').replace("'", '')
            li = list(item.split(','))
            for osmid in li:
                n = 0
                for wayid in way['h_id']:
                    if str(wayid) == ('OSM-' + str(osmid)):
                        h_name.append(node['h_name'][m])
                        h_address.append(node['h_address'][m])
                        h_latitude.append(node['h_latitude'][m])
                        h_longitude.append(node['h_longitude'][m])
                        h_categories.append(node['h_categories'][m])
                        h_id.append(node['h_id'][m])

                        t_name.append(way['h_name'][n])
                        t_address.append(way['h_address'][n])
                        t_latitude.append(way['h_latitude'][n])
                        t_longitude.append(way['h_longitude'][n])
                        t_categories.append(way['h_categories'][n])
                        t_id.append(way['h_id'][n])
                        if node['h_name'][m] == way['h_name'][n] and node['h_categories'][m] == way['h_categories'][n]:
                            relation.append(1)
                        else:
                            relation.append(2)
                    n += 1
        m += 1
    for nname in node['h_name']:
        n = 0
        for wname in way['h_name']:
            if str(nname) == str(wname) and node['h_categories'][m] != way['h_categories'][n]:
                h_name.append(node['h_name'][m])
                h_address.append(node['h_address'][m])
                h_latitude.append(node['h_latitude'][m])
                h_longitude.append(node['h_longitude'][m])
                h_categories.append(node['h_categories'][m])
                h_id.append(node['h_id'][m])

                t_name.append(way['h_name'][n])
                t_address.append(way['h_address'][n])
                t_latitude.append(way['h_latitude'][n])
                t_longitude.append(way['h_longitude'][n])
                t_categories.append(way['h_categories'][n])
                t_id.append(way['h_id'][n])
                relation.append(3)
            n += 1
        m += 1

    h_name, h_address, h_latitude, h_longitude, h_categories, h_id, h_in = [], [], [], [], [], [], []
    t_name, t_address, t_latitude, t_longitude, t_categories, t_id, relation = [], [], [], [], [], [], []
    m = 0
    for item in node['in']:
        if len(item) > 2:
            item = item.replace('[', '').replace(']', '').replace("'", '').replace("'", '')
            li = list(item.split(','))
        n = 0
        for wid in way['h_id']:
            if abs(way['h_latitude'][n] - node['h_latitude'][m]) < 0.001 and abs(
                    way['h_longitude'][n] - node['h_longitude'][m]) < 0.001:
                if wid not in li and way['h_name'][n] != node['h_name'][m]:
                    h_name.append(node['h_name'][m])
                    h_address.append(node['h_address'][m])
                    h_latitude.append(node['h_latitude'][m])
                    h_longitude.append(node['h_longitude'][m])
                    h_categories.append(node['h_categories'][m])
                    h_id.append(node['h_id'][m])

                    t_name.append(way['h_name'][n])
                    t_address.append(way['h_address'][n])
                    t_latitude.append(way['h_latitude'][n])
                    t_longitude.append(way['h_longitude'][n])
                    t_categories.append(way['h_categories'][n])
                    t_id.append(way['h_id'][n])
                    relation.append(0)
            n += 1
        m += 1
    judge0['h_name'] = h_name
    judge0['h_address'] = h_address
    judge0['h_latitude'] = h_latitude
    judge0['h_longitude'] = h_longitude
    judge0['h_categories'] = h_categories
    judge0['h_id'] = h_id
    judge0['t_name'] = t_name
    judge0['t_address'] = t_address
    judge0['t_latitude'] = t_latitude
    judge0['t_longitude'] = t_longitude
    judge0['t_categories'] = t_categories
    judge0['t_id'] = t_id
    judge0['relation'] = relation
    judge0.to_csv(path_node + 'relation-12.csv')
    judge0.to_csv(path_node + 'relation-3.csv')
    judge0.to_csv(path_node + 'relation-0(0.001).csv')

    relation0 = pd.read_csv(path_node + 'relation-0(0.001).csv')
    relation12 = pd.read_csv(path_node + 'relation-12.csv')
    relation3 = pd.read_csv(path_node + 'relation-3.csv')
    relation123 = pd.concat([relation12, relation3])
    relation0123 = pd.concat([relation0, relation123])
    relation123 = relation123.drop(['Unnamed: 0'], axis=1)
    relation0123 = relation0123.drop(['Unnamed: 0'], axis=1)
    relation123.to_csv(path_node + 'relation123.csv')
    relation0123.to_csv(path_node + 'relation0123.csv')
#数据集构建
def data_build(path_node,path_way,path_relation):
    train = pd.DataFrame()
    test = pd.DataFrame()
    valid = pd.DataFrame()
    m = 0
    file = pd.read_csv((path_node + 'relation0123.csv'))
    file = file.drop(['Unnamed: 0'], axis=1)
    print(file)
    rows = file.shape[0]
    for num, da in [(int(6 * rows / 10), train), (int(2 * rows / 10), test), (int(2 * rows / 10), valid)]:
        h_name, h_address, h_latitude, h_longitude, h_categories, h_id, h_in = [], [], [], [], [], [], []
        t_name, t_address, t_latitude, t_longitude, t_categories, t_id, relation = [], [], [], [], [], [], []
        for count in range(num):
            row = file.shape[0]
            if count % 1000 == 0:
                print(row)
            n = random.randint(0, row - 1)
            h_name.append(file['h_name'][n])
            h_address.append(file['h_address'][n])
            h_latitude.append(file['h_latitude'][n])
            h_longitude.append(file['h_longitude'][n])
            h_categories.append(file['h_categories'][n])
            h_id.append(file['h_id'][n])

            t_name.append(file['t_name'][n])
            t_address.append(file['t_address'][n])
            t_latitude.append(file['t_latitude'][n])
            t_longitude.append(file['t_longitude'][n])
            t_categories.append(file['t_categories'][n])
            t_id.append(file['t_id'][n])
            relation.append(file['relation'][n])

            file.drop(index=[n], inplace=True)
            file = file.reset_index(drop=True)

        da['h_name'] = h_name
        da['h_address'] = h_address
        da['h_latitude'] = h_latitude
        da['h_longitude'] = h_longitude
        da['h_categories'] = h_categories
        da['h_id'] = h_id
        da['t_name'] = t_name
        da['t_address'] = t_address
        da['t_latitude'] = t_latitude
        da['t_longitude'] = t_longitude
        da['t_categories'] = t_categories
        da['t_id'] = t_id
        da['relation'] = relation

        list = ['train', 'test', 'valid']
        da.to_csv(path_node + list[m] + '.csv')
        m += 1


