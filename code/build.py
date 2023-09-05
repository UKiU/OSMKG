import pandas as pd
from lxml import etree
import xmltodict
from tool import *


class OsmKG:
    def __init__(self, osmfile, outway='../data'):
        self.poi = pd.DataFrame()
        self.aoi = pd.DataFrame()
        self.cate = {}
        self.tag = {}

        osm = osmfile.replace("\\", "/")
        out = outway.replace("\\", "/")
        self.osmfile = osm
        self.outway = out

        path_node0 = str(self.outway + '/node')
        path_way0 = str(self.outway + '/way')
        path_relation0 = str(self.outway + '/relation')
        path_KG0 = str(self.outway + '/KG')

        check_path(path_node0)
        check_path(path_way0)
        check_path(path_relation0)
        check_path(path_KG0)
        self.path_node = str(self.outway + '/node/')
        self.path_way = str(self.outway + '/way/')
        self.path_relation = str(self.outway + '/relation/')
        self.path_KG = str(self.outway + '/KG/')

    def osm_deconstruction(self):
        # 读取node、way、relation
        file_length = -1
        for file_length, line in enumerate(open(osmfile, 'r', encoding='UTF-8')):
            pass
        file_length += 1
        print("length of the file:\t" + str(file_length))

        file_node = open(self.path_node + "node.json", "w+")
        file_parsed1 = etree.iterparse(osmfile, tag=["node"])
        iter_element(file_parsed1, file_length, file_node, "node")
        file_node.close()

        file_way = open(self.path_way + "way.json", "w+")
        file_parsed2 = etree.iterparse(osmfile, tag=["way"])
        iter_element(file_parsed2, file_length, file_way, "way")
        file_way.close()

        file_relation = open(self.path_relation + "relation.json", "w+")
        file_parsed3 = etree.iterparse(osmfile, tag=["relation"])
        iter_element(file_parsed3, file_length, file_relation, "relation")
        file_relation.close()

    # def poi_extract(self):
    #     print("deal with node\n")
    #     # 读取有name的node
    #     file_read = pd.read_json(self.path_node + "node.json")
    #
    #     # 闭环way含name9
    #     file_write2 = open(self.path_node + 'NewYork_node2.json', mode='wb')
    #     with open(self.path_node + 'node.json', mode='rb') as file_read:
    #         count = 0
    #         for line in file_read:
    #             line = line.replace('\n'.encode(), ''.encode())
    #             info = json.loads(line)
    #             if 'tag' in info and type(info['tag']) is list and 'nd' in info and type(info['nd']) is list:
    #                 ff = 0
    #                 if info['nd'][0] == info['nd'][len(info['nd']) - 1]:
    #                     for item in info['tag']:
    #                         if 'name' in item.values():
    #                             ff = 1
    #                 if ff == 1:
    #                     elem = json.dumps(info)
    #                     file_write2.write((elem + "\n").encode())
    #                 count += 1
    #     file_write2.close()
    #     df = pd.read_json(path_node + 'NewYork_node2.json', encoding='utf-8', lines=True)
    #     df.to_csv(path_node + 'NewYork_node2.csv')
    #
    #     # 清除k,v,并获取tag
    #     file_write2 = open(path_node + 'NewYork_node_clear.json', mode='wb')
    #     with open(path_node + 'node.json', mode='rb') as file_read:
    #         count = 0
    #         for line in file_read:
    #             line = line.replace('\n'.encode(), ''.encode())
    #             info = json.loads(line)
    #             if 'tag' in info and type(info['tag']) is list:
    #                 for item in info['tag']:
    #                     key = item['k']
    #                     val = item['v']
    #                     item.clear()
    #                     item[key] = val
    #             elem = json.dumps(info)
    #             file_write2.write((elem + "\n").encode())
    #     file_write2.close()
    #     df = pd.read_json(path_node + 'NewYork_node_clear.json', encoding='utf-8', lines=True)
    #     df.to_csv(path_node + 'NewYork_node_clear.csv')
    #
    #     # 仅包含cor
    #     file_write2 = open(path_node + 'NewYork_node_cor.json', mode='wb')
    #     with open(path_node + 'node.json', mode='rb') as file_read:
    #         count = 0
    #         for line in file_read:
    #             line = line.replace('\n'.encode(), ''.encode())
    #             info = json.loads(line)
    #             if 'tag' in info:
    #                 info.pop('tag')
    #             elem = json.dumps(info)
    #             file_write2.write((elem + "\n").encode())
    #     file_write2.close()
    #     df = pd.read_json(path_node + 'NewYork_node_cor.json', encoding='utf-8', lines=True)
    #     df.to_csv(path_node + 'NewYork_node_cor.csv')
    #
    # def aoi_extract(self):
    #
    # def cate_extract(self):
    #
    # def tag_extract(self):


# 读取数据
if __name__ == '__main__':

    while (True):
        osmfile = input("put in the path of OSM file\n")
        outway = input("put in the path to store output data\n").replace(r'\\', "/")
        new = OsmKG(osmfile=osmfile, outway=outway)
        print(new.outway)
