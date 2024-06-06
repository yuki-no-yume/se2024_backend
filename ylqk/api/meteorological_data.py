import requests
import numpy as npy
import geopandas as gpd
from django.http import HttpRequest
from django.views.decorators.http import require_GET, require_POST
from datetime import datetime, timedelta
from scipy import interpolate
from shapely.geometry import Point

from utils.api_key import *
from utils.response_util import *
from ylqk.models.interp_data import *
from ylqk.models.meteorological_data import *

element_params = {
    "prs": "PRS",
    "prs_sea": "PRS_Sea",
    "prs_max": "PRS_Max",
    "prs_min": "PRS_Min",
    "temp": "TEM",
    "temp_max": "TEM_MAX",
    "temp_min": "TEM_MIN",
    "rhu": "RHU",
    "rhu_min": "RHU_Min",
    "vap": "VAP",
    "pre_sum": "PRE_3h",
    "wind_sp_max": "WIN_S_MAX",
    "wind_inst_sp_max": "WIN_S_Inst_Max",
    "clo_cov": "CLO_Cov",
    "clo_cov_low": "CLO_Cov_Low",
}

_lng_cn = npy.linspace(73.67, 135.08, 174)
_lat_cn = npy.linspace(18.17, 53.5, 100)
_lng_cn2d, _lat_cn2d = npy.meshgrid(_lng_cn, _lat_cn)


def _valid(value: int | float) -> bool:
    return value != 999999 and value != 999998 and value != 999990


def _list2str(lst: list) -> str:
    result = ""
    if len(lst) == 0:
        return result
    else:
        result += str(lst[0])
    for i in range(1, len(lst)):
        result += f",{str(lst[i])}"
    return result


def _update_meteorological_data():
    # &timeRange=[20240404110000,20240411110000]&staIDs=54433,54399
    hours_delta = 3 if datetime.utcnow().hour % 3 == 0 else int(datetime.utcnow().hour % 3)
    update_time = (datetime.utcnow() - timedelta(hours=hours_delta)).strftime("%Y%m%d%H0000")
    basic_url = BASIC_URL + ALL_ELEMENTS + f"&timeRange=[{update_time},{update_time}]"
    stations = StationInfo.objects.all()
    index = 0
    while index < len(stations):
        station_sub_list = stations[index:index + 30]
        station_id_list = []
        for elm in station_sub_list:
            station_id_list.append(elm.station_id)
        cur_url = basic_url + f"&staIDs={_list2str(station_id_list)}"
        response = requests.get(cur_url)
        data = response.json()["DS"]
        for elm in data:
            datetime_str = str(elm["Datetime"])
            AllMeteorologicalData.objects.filter(Station_Id_C=elm["STATION_Id_C"]).update(
                Datetime=datetime(
                    year=int(datetime_str[0:4]),
                    month=int(datetime_str[4:6]),
                    day=int(datetime_str[6:8]),
                    hour=int(datetime_str[8:10]),
                    minute=int(datetime_str[10:12]),
                    second=int(datetime_str[12:14])
                ),
                PRS=elm["PRS"],
                PRS_Sea=elm["PRS_Sea"],
                PRS_Max=elm["PRS_Max"],
                PRS_Min=elm["PRS_Min"],
                TEM=elm["TEM"],
                TEM_MAX=elm["TEM_MAX"],
                TEM_MIN=elm["TEM_MIN"],
                RHU=elm["RHU"],
                RHU_Min=elm["RHU_Min"],
                VAP=elm["VAP"],
                PRE_3h=elm["PRE_3h"],
                WIN_S_Avg_2mi=elm["WIN_S_Avg_2mi"],
                WIN_D_Avg_2mi=elm["WIN_D_Avg_2mi"],
                WIN_S_MAX=elm["WIN_S_MAX"],
                WIN_D_S_Max=elm["WIN_D_S_Max"],
                WIN_S_Inst_Max=elm["WIN_S_Inst_Max"],
                WIN_D_INST_Max=elm["WIN_D_INST_Max"],
                CLO_Cov=elm["CLO_Cov"],
                CLO_Cov_Low=elm["CLO_Cov_Low"],
                CLO_COV_LM=elm["CLO_COV_LM"],
                VIS=elm["VIS"],
                WEP_Now=elm["WEP_Now"]
            )
        index += 30
    print(f"{datetime.now()} Finished updating origin meteorological data.")
    _process_meteorological_data()
    print(f"{datetime.now()} Finished updating interp meteorological data.")


def _interp2d(lng_list: list, lat_list: list, value_list: list, func: str = "multiquadric"):
    """
    The radial basis function, based on the radius, r, given by the norm
        (default is Euclidean distance); the default is 'multiquadric'::
            'multiquadric': sqrt((r/self.epsilon)**2 + 1)
            'inverse': 1.0/sqrt((r/self.epsilon)**2 + 1)
            'gaussian': exp(-(r/self.epsilon)**2)
            'linear': r
            'cubic': r**3
            'quintic': r**5
            'thin_plate': r**2 * log(r)
    """
    # 不排除个别数值不合理的情况
    f_interp = interpolate.Rbf(lng_list, lat_list, value_list, function=func)
    interp_list = f_interp(_lng_cn2d, _lat_cn2d)
    return interp_list


def _process_meteorological_data():
    longitude_list = []
    latitude_list = []
    temp_values = []
    prs_values = []
    rhu_values = []
    pre3h_values = []
    winds_values = []
    china = gpd.read_file("./utils/china.json").geometry.make_valid()
    origin_meteorological_data = AllMeteorologicalData.objects.all()
    for elm in origin_meteorological_data:
        elm.station_info = StationInfo.objects.filter(station_id=elm.Station_Id_C).first()
    for elm in origin_meteorological_data:
        longitude_list.append(elm.station_info.longitude)
        latitude_list.append(elm.station_info.latitude)
        if not _valid(elm.TEM):
            elm.TEM = 20.0
        temp_values.append(elm.TEM)
        if not _valid(elm.PRS):
            elm.PRS = 1000.0
        prs_values.append(elm.PRS)
        if not _valid(elm.RHU):
            elm.RHU = 80.0
        rhu_values.append(elm.RHU)
        if not _valid(elm.PRE_3h):
            elm.PRE_3h = 0.0
        pre3h_values.append(elm.PRE_3h)
        if not _valid(elm.WIN_S_Avg_2mi):
            elm.WIN_S_Avg_2mi = 0.0
        winds_values.append(elm.WIN_S_Avg_2mi)

    interp_temp_values = _interp2d(longitude_list, latitude_list, temp_values, func="inverse")
    interp_prs_values = _interp2d(longitude_list, latitude_list, prs_values, func="linear")
    interp_rhu_values = _interp2d(longitude_list, latitude_list, rhu_values, func="inverse")
    interp_pre3h_values = _interp2d(longitude_list, latitude_list, pre3h_values, func="inverse")
    interp_winds_values = _interp2d(longitude_list, latitude_list, winds_values, func="inverse")

    for i in range(0, len(_lng_cn2d)):
        for j in range(0, len(_lng_cn2d[i])):
            point = Point(_lng_cn2d[i][j], _lat_cn2d[i][j])
            if china.contains(point).any():
                if interp_temp_values[i][j] > 42:
                    interp_temp_values[i][j] = 42.0
                elif interp_temp_values[i][j] < -20:
                    interp_temp_values[i][j] = -20.0
                interp_temp_values[i][j] += 60  # 加上偏移
                if interp_prs_values[i][j] > 1013.25:
                    interp_prs_values[i][j] = 1013.25
                if interp_rhu_values[i][j] > 100:
                    interp_rhu_values[i][j] = 100.0
                elif interp_rhu_values[i][j] < 0:
                    interp_rhu_values[i][j] = 0.0
                if interp_pre3h_values[i][j] < 0.0:
                    interp_pre3h_values[i][j] = 0.0
                if interp_winds_values[i][j] < 0.0:
                    interp_winds_values[i][j] = 0.0
                # InterpData.objects.create(
                #     longitude=_lng_cn2d[i][j],
                #     latitude=_lat_cn2d[i][j],
                #     temp=interp_temp_values[i][j],
                #     prs=interp_prs_values[i][j],
                #     rhu=interp_rhu_values[i][j],
                #     pre3h=interp_pre3h_values[i][j],
                #     wind_s=interp_winds_values[i][j],
                # )
                InterpData.objects.filter(longitude=_lng_cn2d[i][j],
                                          latitude=_lat_cn2d[i][j]).update(
                    temp=interp_temp_values[i][j],
                    prs=interp_prs_values[i][j],
                    rhu=interp_rhu_values[i][j],
                    pre3h=interp_pre3h_values[i][j],
                    wind_s=interp_winds_values[i][j],
                )


@require_GET
def get_station_info(request: HttpRequest):
    response = []
    station_id_list = request.GET.getlist("id")
    for station_id in station_id_list:
        station = StationInfo.objects.filter(station_id=int(station_id)).first()
        if station is not None:
            response.append(station)
    return build_success_json_response(response)


@require_GET
def get_all_station_info(request: HttpRequest):
    stations = StationInfo.objects.all()
    return build_success_json_response(stations)


@require_GET
def get_origin_meteorological_data(request: HttpRequest):
    import time
    t0 = time.time()
    data_type = request.GET.get("type")
    response: QuerySet
    if data_type == "all":
        response = AllMeteorologicalData.objects.all()
    elif data_type == "temp":
        response = TemperatureData.objects.all()
    elif data_type == "prs":
        response = PressureData.objects.all()
    elif data_type == "hum":
        response = HumidityData.objects.all()
    elif data_type == "wind":
        response = WindData.objects.all()
    elif data_type == "cloud":
        response = CloudData.objects.all()
    elif data_type == "other":
        response = OtherMeteorologicalData.objects.all()
    else:
        return build_failed_json_response(StatusCode.BAD_REQUEST)
    print(time.time() - t0)
    for elm in response:
        elm.station_info = StationInfo.objects.filter(station_id=elm.Station_Id_C).first()
    print(time.time() - t0)
    return build_success_json_response(response)


@require_GET
def get_all_pressure_data(request: HttpRequest):
    pressure_data = PressureData.objects.all()
    for elm in pressure_data:
        elm.station_info = StationInfo.objects.filter(station_id=elm.Station_Id_C).first()
    return build_success_json_response(pressure_data)


@require_GET
def get_all_temperature_data(request: HttpRequest):
    temperature_data = TemperatureData.objects.all()
    for elm in temperature_data:
        elm.station_info = StationInfo.objects.filter(station_id=elm.Station_Id_C).first()
    return build_success_json_response(temperature_data)


@require_GET
def get_all_humidity_data(request: HttpRequest):
    humidity_data = HumidityData.objects.all()
    for elm in humidity_data:
        elm.station_info = StationInfo.objects.filter(station_id=elm.Station_Id_C).first()
    return build_success_json_response(humidity_data)


@require_GET
def get_all_wind_data(request: HttpRequest):
    wind_data = WindData.objects.all()
    for elm in wind_data:
        elm.station_info = StationInfo.objects.filter(station_id=elm.Station_Id_C).first()
    return build_success_json_response(wind_data)


@require_GET
def get_all_cloud_data(request: HttpRequest):
    cloud_data = CloudData.objects.all()
    for elm in cloud_data:
        elm.station_info = StationInfo.objects.filter(station_id=elm.Station_Id_C).first()
    return build_success_json_response(cloud_data)


@require_GET
def get_all_other_meteorological_data(request: HttpRequest):
    other_weather_data = OtherMeteorologicalData.objects.all()
    for elm in other_weather_data:
        elm.station_info = StationInfo.objects.filter(station_id=elm.Station_Id_C).first()
    return build_success_json_response(other_weather_data)


@require_POST
def update_meteorological_data_by_admin(request: HttpRequest):
    # TODO: 此处加入管理员权限认证
    _update_meteorological_data()
    return build_success_json_response()


@require_GET
def get_interp_meteorological_data(request: HttpRequest):
    data_type = request.GET.get("type")
    origin_interp_data = InterpData.objects.all()
    response = []
    if data_type == "temp":
        for elm in origin_interp_data:
            meta = {
                "geometry": {
                    "type": "Point",
                    "coordinates": [elm.longitude, elm.latitude]
                },
                "properties": {
                    "count": elm.temp,
                }
            }
            response.append(meta)
    elif data_type == "prs":
        for elm in origin_interp_data:
            meta = {
                "geometry": {
                    "type": "Point",
                    "coordinates": [elm.longitude, elm.latitude]
                },
                "properties": {
                    "count": elm.prs,
                }
            }
            response.append(meta)
    elif data_type == "rhu":
        for elm in origin_interp_data:
            meta = {
                "geometry": {
                    "type": "Point",
                    "coordinates": [elm.longitude, elm.latitude]
                },
                "properties": {
                    "count": elm.rhu,
                }
            }
            response.append(meta)
    elif data_type == "pre3h":
        for elm in origin_interp_data:
            meta = {
                "geometry": {
                    "type": "Point",
                    "coordinates": [elm.longitude, elm.latitude]
                },
                "properties": {
                    "count": elm.pre3h,
                }
            }
            response.append(meta)
    elif data_type == "wind":
        for elm in origin_interp_data:
            meta = {
                "geometry": {
                    "type": "Point",
                    "coordinates": [elm.longitude, elm.latitude]
                },
                "properties": {
                    "count": elm.wind_s,
                }
            }
            response.append(meta)
    else:
        return build_failed_json_response(StatusCode.BAD_REQUEST)
    return build_success_json_response(response)


@require_GET
def get_history_meteorological_data(request: HttpRequest):
    station_id = request.GET.get("station_id")
    data_type = request.GET.get("data_type")
    if data_type not in element_params.keys():
        return build_failed_json_response(status_code=StatusCode.BAD_REQUEST)
    from_time = (datetime.utcnow() - timedelta(days=7)).strftime("%Y%m%d000000")
    to_time = datetime.utcnow().strftime("%Y%m%d000000")
    url = BASIC_URL + f"&staIDs={station_id}&timeRange=[{from_time},{to_time}]" \
                      f"&elements=Datetime,{element_params[data_type]}"
    data = requests.get(url).json()["DS"]

    flag_date = from_time[0:8]
    cnt = 0
    value = 0
    dates = []
    values = []
    for elm in data:
        cur_date = elm["Datetime"][0:8]
        if cur_date == flag_date:
            if _valid(float(elm[element_params[data_type]])):
                value += float(elm[element_params[data_type]])
                cnt += 1
        else:
            dates.append(flag_date)
            if data_type == "pre_sum":
                values.append(value)
            else:
                values.append(value / cnt if cnt != 0 else 0)
            flag_date = cur_date
            cnt = 0
            value = 0
    result = []
    for i in range(0, len(dates)):
        result.append({
            "date": dates[i],
            "value": values[i],
        })
    return build_success_json_response(result)


@require_GET
def get_current_city_weather(request: HttpRequest):
    longitude = request.GET.get('longitude')
    latitude = request.GET.get('latitude')
    url = 'https://api.seniverse.com/v3/weather/now.json?'
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) '
                      'CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1 Edg/117.0.0.0'
    }
    params = {'key': 'SN_H868TafuTTtyLb', 'language': 'zh-Hans', 'unit': 'c', 'location': latitude + ":" + longitude}
    response = requests.get(url=url, params=params, headers=headers)
    data = response.json()
    data = data['results'][0]['now']
    return build_success_json_response(data)
