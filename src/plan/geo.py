import requests


class LocationMeta:
    def __init__(self, pname: str, pcode: int, mname: str, mcode: int, lat: float, lon: float):
        self.pname = pname
        self.pcode = pcode
        self.mname = mname
        self.mcode = mcode
        self.lat = lat
        self.lon = lon


def convert_geo_to_location(lat: float, lon: float) -> LocationMeta:
    params = {
        "lat": lat,
        "lon": lon,
        "json": True,
    }
    res = requests.get(url="http://www.finds.jp/ws/rgeocode.php", params=params)
    res = res.json()
    result = res.get('result')
    if result is None:
        return None

    pre = result.get('prefecture')
    if pre is None:
        return None

    mun = result.get('municipality')
    if mun is None:
        return None

    return LocationMeta(pre.get('pname'), pre.get('pcode'), mun.get('mname'), mun.get('mcode'), lat, lon)

# Usage
# l = convert_geo_to_location(34.6848759, 135.1982840)
# print(l.pname, l.pcode, l.mname, l.mcode, l.lat, l.lon)
