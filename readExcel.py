import pandas as pd

PCCity = ['惠州市', '苏州市', '天津市', '杭州市', '重庆市']
phoneCity = ['成都市', '武汉市', '上海市']


def getSheetKeys() -> list:
    sheet = pd.read_excel(r'./excel/data.xlsx', sheet_name=None)
    return list(sheet.keys())


def getSheetData(sheet_name: str):
    """
    :param sheet_name:
    :return: data form excel
    """
    data = pd.read_excel(r'./excel/data-new.xlsx', sheet_name=sheet_name)
    return data


def re(address: str) -> [float, float]:
    """
    todo transform :str address to :float address
    :param address: address in map, such as 北纬39°08',东经117°20'
    :returns [dimension(纬度) in map, longitude(经度) in map]
    """
    address = address.replace('°', '.')
    address = address.replace('\'', '')
    x, y = address.split(',')
    return eval(x[2:]), eval(y[2:]),


def getDifferentPointInMap():
    """
    task one:
    1. select factory to product phone & PC use different color to drew it.
    from sheet -> 站点信息
    logo: pentagram
    color: phone -> red, PC -> blue
    2. select delivery center to drew it.
    from sheet -> 站点信息
    logo: square
    color: green
    3. select costumer to drew it
    from sheet -> 客户信息
    logo: circle
    color: purple
    :param
    :return [pc factory point, phone factory point, delivery center point, costumer point]
    """
    # 1. drew factory
    siteInformation = getSheetData('站点信息')
    costumerInformation = getSheetData('客户信息')
    PCFactory = [re(_['坐标']) for idx, _ in siteInformation.iterrows() if _['类型'] == '工厂' and _['城市'] in PCCity]
    phoneFactory = [re(_['坐标']) for idx, _ in siteInformation.iterrows() if _['类型'] == '工厂' and _['城市'] in phoneCity]
    deliveryCenter = [re(_['坐标']) for idx, _ in siteInformation.iterrows() if _['类型'] == '配送中心']
    costumer = [re(_['坐标']) for idx, _ in costumerInformation.iterrows() if str(_['坐标']) != 'nan']
    return PCFactory, phoneFactory, deliveryCenter, costumer


def getMinDimensionAndLongitude() -> [float, float]:
    """
    todo get min dimension(纬度) & longitude(经度) in map
    result: (minDimension, minLongitude) -> (18.25, 75.99)
    """
    minDimension, minLongitude = 2 ** 30, 2 ** 30
    allPoint = getDifferentPointInMap()
    for _ in allPoint:
        for point in _:
            if point[0] < minDimension:
                minDimension = point[0]
            if point[1] < minLongitude:
                minLongitude = point[1]
    return minDimension, minLongitude


def func():
    sumConsumerOrderInformation = getSheetData('客户订单总')


if __name__ == '__main__':
    print(getMinDimensionAndLongitude())
