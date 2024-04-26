from django.http import HttpRequest
from django.views.decorators.http import require_GET

from utils.response_util import *
from ylqk.models import *


@require_GET
def get_station_info(request: HttpRequest):
    station_id = request.GET.get("station_id")
    station_info = StationInfo.objects.filter(station_id=station_id).first()
    if isinstance(station_info, QuerySet) or isinstance(station_info, Model):
        return build_success_json_response(station_info)
    else:
        return build_failed_json_response(StatusCode.NOT_FOUND, "站点id不存在")


@require_GET
def get_all_station_info(request: HttpRequest):
    station_info = StationInfo.objects.all()
    return build_success_json_response(station_info)


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
