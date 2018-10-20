import requests


class LocationMeta:
    def __init__(self, pname: str, pcode: int, mname: str, mcode: int, lat: float, lon: float):
        """
        位置情報をまとめたクラス
        :param pname: 都道府県名
        :param pcode: 都道府県コード
        :param mname: 市区町村名
        :param mcode: 市区町村コード
        :param lat: 緯度
        :param lon: 経度
        """
        self.pname = pname
        self.pcode = pcode
        self.mname = mname
        self.mcode = mcode
        self.lat = lat
        self.lon = lon


def convert_geo_to_location(lat: float, lon: float) -> LocationMeta:
    """
    https://www.finds.jp/rgeocode/index.html.ja
    を参考に，逆ジオコーディングする関数
    :param lat: 緯度
    :param lon: 経度
    :return: LocationMeta
    """
    params = {
        "lat": lat,
        "lon": lon,
        "json": True,
    }
    res = requests.get(url="http://www.finds.jp/ws/rgeocode.php", params=params)

    if res.status_code != 200:
        return None

    res = res.json()
    pre = res['result']['prefecture']
    mun = res['result']['municipality']

    return LocationMeta(pre['pname'], pre['pcode'], mun['mname'], mun['mcode'], lat, lon)

# Usage
# l = convert_geo_to_location(34.6848759, 135.1982840)
# print(l.pname, l.pcode, l.mname, l.mcode, l.lat, l.lon)
