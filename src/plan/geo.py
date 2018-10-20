import requests
from typing import Optional


class LocationMeta:
    def __init__(self, p_name: str, p_code: int, m_name: str, m_code: int, lat: float, lon: float):
        """
        位置情報をまとめたクラス
        :param p_name: 都道府県名
        :param p_code: 都道府県コード
        :param m_name: 市区町村名
        :param m_code: 市区町村コード
        :param lat: 緯度
        :param lon: 経度
        """
        self.p_name = p_name
        self.p_code = p_code
        self.m_name = m_name
        self.m_code = m_code
        self.lat = lat
        self.lon = lon


def convert_geo_to_location(lat: float, lon: float) -> Optional[LocationMeta]:
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
