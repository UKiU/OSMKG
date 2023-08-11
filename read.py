from lxml import etree
import xmltodict
from deal import *


# 读取数据
def iter_element(file_parsed, file_length, file_write, tag_type):
    current_line = 0
    try:
        for event, element in file_parsed:
            current_line += 1
            if current_line % 100 == 0:
                print(current_line / float(file_length))
            elem_data = etree.tostring(element)
            elem_dict = xmltodict.parse(elem_data, attr_prefix="", cdata_key="")
            if element.tag == tag_type:
                elem_jsonStr = json.dumps(elem_dict[tag_type])
                file_write.write(elem_jsonStr + "\n")
            # 每次读取之后进行一次清空
            element.clear()
            while element.getprevious() is not None:
                del element.getparent()[0]
    except:
        pass


if __name__ == '__main__':

    while (True):
        osmfile = input("put in the path of OSM file\n")
        osmfile = osmfile.replace("\\", "/")
        outfile = input("put in the path of output\n").replace(r'\\', "/")
        outfile = outfile.replace("\\", "/")
        print(outfile)

        path_node0 = str(outfile + '/node')
        path_way0 = str(outfile + '/way')
        path_relation0 = str(outfile + '/relation')
        path_KG0 = str(outfile + '/KG')

        check_path(path_node0)
        check_path(path_way0)
        check_path(path_relation0)
        check_path(path_KG0)
        path_node = str(outfile + '/node/')
        path_way = str(outfile + '/way/')
        path_relation = str(outfile + '/relation/')
        path_KG = str(outfile + '/KG/')

        # 读取node、way、relation
        file_length = -1
        for file_length, line in enumerate(open(osmfile, 'r', encoding='UTF-8')):
            pass
        file_length += 1
        print("length of the file:\t" + str(file_length))

        file_node = open(path_node + "node.json", "w+")
        file_parsed1 = etree.iterparse(osmfile, tag=["node"])
        iter_element(file_parsed1, file_length, file_node, "node")
        file_node.close()

        file_way = open(path_way + "way.json", "w+")
        file_parsed2 = etree.iterparse(osmfile, tag=["way"])
        iter_element(file_parsed2, file_length, file_way, "way")
        file_way.close()

        file_relation = open(path_relation + "relation.json", "w+")
        file_parsed3 = etree.iterparse(osmfile, tag=["relation"])
        iter_element(file_parsed3, file_length, file_relation, "relation")
        file_relation.close()

        # 处理node、way、relation
        check_path([path for path in [path_node0, path_way0, path_relation0]])
        node_deal(path_node, path_way)
        way_deal(path_node, path_way)
        relation_deal(path_relation)
        tag_deal(path_node, path_way, path_relation, path_KG)
        POI_find(path_node, path_way, path_relation)
        AOI_find(path_node, path_way, path_relation)
        relation_build(path_node, path_way, path_relation)
        data_build(path_node, path_way, path_relation)

    print(end - start)
