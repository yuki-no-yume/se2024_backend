import requests
from django.http import HttpRequest
from django.views.decorators.http import require_GET, require_POST
from datetime import datetime, timedelta

from utils.response_util import *
from ylqk.models.meteorological_data import *


USER_ID = "714756904471BoKJR"
PWD = "AhKNgEJ"
API = f"http://api.data.cma.cn:8090/api?userId={USER_ID}&pwd={PWD}" \
      "&dataFormat=json&interfaceId=getSurfEleByTimeRangeAndStaID&dataCode=SURF_CHN_MUL_HOR_3H" \
      "&elements=STATION_Id_C,Datetime,PRS,PRS_Sea,PRS_Max,PRS_Min," \
      "TEM,TEM_MAX,TEM_MIN," \
      "RHU,RHU_Min,VAP,PRE_3h," \
      "WIN_S_Avg_2mi,WIN_D_Avg_2mi,WIN_S_MAX,WIN_D_S_Max,WIN_S_Inst_Max,WIN_D_INST_Max," \
      "CLO_Cov,CLO_Cov_Low,CLO_COV_LM," \
      "VIS,WEP_Now"


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
    update_time = (datetime.utcnow()-timedelta(hours=hours_delta)).strftime("%Y%m%d%H0000")
    basic_url = API + f"&timeRange=[{update_time},{update_time}]"
    stations = StationInfo.objects.all()
    index = 0
    while index < len(stations):
        station_sub_list = stations[index:index+30]
        station_id_list = []
        for elm in station_sub_list:
            station_id_list.append(elm.station_id)
        cur_url = basic_url + f"&staIDs={_list2str(station_id_list)}"
        response = requests.get(cur_url)
        print(response.json())
        data = response.json()["DS"]
        for elm in data:
            print(elm["STATION_Id_C"])
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


@require_GET
def get_station_info(request: HttpRequest):
    station_id = request.GET.get("station_id")
    station = StationInfo.objects.filter(station_id=station_id).first()
    if isinstance(station, QuerySet) or isinstance(station, Model):
        return build_success_json_response(station)
    else:
        return build_failed_json_response(StatusCode.NOT_FOUND, "站点id不存在")


@require_GET
def get_all_station_info(request: HttpRequest):
    stations = StationInfo.objects.all()
    return build_success_json_response(stations)


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
    # 此处加入管理员权限认证
    _update_meteorological_data()
    return build_success_json_response()
