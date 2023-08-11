def isInRegion_lat_lon(lat, lon, region_1):
    '''
    判断点[lat, lon] 是否在区域 region_1内
    :param lat: 输入点的 纬度
    :param lon: 输入点的 经度
    :param region_1: region1是一个list，其格式为：[[40.695,-74.035],[ 40.694,-74.036]...] 其内层list中第一个元素代表纬度，第二个代表经度
    :return: True则在所选区域内  False则不在
    '''
    count = 0
    lat = float(lat)
    lon = float(lon)

    for i in range(len(region_1)):
        # 如果是最后一个元素，那么必然是和第一个一样的，就啥也不干
        if i+1 == len(region_1):
            break
        # 如果不是最后一个元素，那么需要和后一个元素一起判断给定点是否在区域内
        la_1, lo_1= region_1[i]
        la_2, lo_2= region_1[i + 1]

        la_1, lo_1, la_2, lo_2 = float(la_1), float(lo_1), float(la_2), float(lo_2)
        # print((lo_1, la_1))
        # # 以纬度确定位置，沿纬度向右作射线，看交点个数
        if lat < min(la_1, la_2):
            # print('点高度小于线段', (lo_1, la_1))
            continue
        if lat > max(la_1, la_2):
            # print('点高度大于线段', (lo_1, la_1))
            continue
        # 如果和某一个共点那么直接返回true
        if (lat, lon) == (la_1, lo_1) or (lat, lon) == (la_2, lo_2):
            # print('在线段顶点上', (lo_1, la_1))
            return True
        # 如果和两点共线
        if lat == la_1 == la_2:
            # print('两点共线', (lo_1, la_1))
            continue

        # 接下来只需考虑射线穿越的情况，该情况下的特殊情况是射线穿越顶点
        # 求交点的经度
        cross_lon = (lat - la_1) * (lo_2 - lo_1) / (la_2 - la_1 or 0.000000000000000000000001) + lo_1
        # 无所谓在交点在点的左右 方向向上的边不包括其终止点  方向向下的边不包括其开始点
        if lat == max(la_1, la_2):
            continue
        # 其他情况
        elif cross_lon > lon:
            count += 1

    # print(count)
    if count%2 == 0:
        return False
    return True

def isInRegion_lon_lat(lon, lat, region_1):
    '''
    判断点[lon, lat] 是否在区域 region_1内
    :param lon: 输入点的 经度
    :param lat: 输入点的 纬度
    :param region_1: region1是一个list，其格式为：[[-74.035, 40.695],[-74.036, 40.694]...] 其内层list中第一个元素代表经度，第二个代表纬度
    :return: True则在所选区域内  False则不在
    '''
    count = 0
    lat = float(lat)
    lon = float(lon)

    for i in range(len(region_1)):
        # 如果是最后一个元素，那么必然是和第一个一样的，就啥也不干
        if i+1 == len(region_1):
            break
        # 如果不是最后一个元素，那么需要和后一个元素一起判断给定点是否在区域内
        lo_1, la_1 = region_1[i]
        lo_2, la_2 = region_1[i + 1]

        la_1, lo_1, la_2, lo_2 = float(la_1), float(lo_1), float(la_2), float(lo_2)
        # print((lo_1, la_1))
        # # 以纬度确定位置，沿纬度向右作射线，看交点个数
        if lat < min(la_1, la_2):
            # print('点高度小于线段', (lo_1, la_1))
            continue
        if lat > max(la_1, la_2):
            # print('点高度大于线段', (lo_1, la_1))
            continue
        # 如果和某一个共点那么直接返回true
        if (lat, lon) == (la_1, lo_1) or (lat, lon) == (la_2, lo_2):
            # print('在线段顶点上', (lo_1, la_1))
            return True
        # 如果和两点共线
        if lat == la_1 == la_2:
            # print('两点共线', (lo_1, la_1))
            continue

        # 接下来只需考虑射线穿越的情况，该情况下的特殊情况是射线穿越顶点
        # 求交点的经度
        cross_lon = (lat - la_1) * (lo_2 - lo_1) / (la_2 - la_1 or 0.000000000000000000000001) + lo_1
        # 无所谓在交点在点的左右 方向向上的边不包括其终止点  方向向下的边不包括其开始点
        if lat == max(la_1, la_2):
            continue
        # 其他情况
        elif cross_lon > lon:
            count += 1

    # print(count)
    if count%2 == 0:
        return False
    return True
