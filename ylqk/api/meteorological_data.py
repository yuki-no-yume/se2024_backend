from django.db.models import QuerySet, Model
from django.http import HttpRequest
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_GET, require_POST

from utils.response_util import *
from ylqk.models.pressure_data import PressureData
from ylqk.models.station_info import StationInfo


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
    data = PressureData.objects.all()
    for station in data:
        station.station_info = StationInfo.objects.filter(station_id=station.Station_Id_C).first()
    return build_success_json_response(data)
