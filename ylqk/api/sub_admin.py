from django.http import HttpRequest
from django.views.decorators.http import require_GET

from utils.response_util import *
from ..models.users import *
from ..models.announcement import *
from ..api.annoucement import publish,getSurroundings

def create_forewarn(request:HttpRequest):
    disaster = AIDisasterForecast.objects.create()

    if request.POST.get("type"):
        disaster.disaster_type = request.POST.get("type")
    if request.POST.get("level"):
        disaster.disaster_level = request.POST.get("level")
    if request.POST.get("location"):
        disaster.disaster_location = request.POST.get("location")
    if request.POST.get("longitude"):
        disaster.disaster_longitude = request.POST.get("longitude")
    if request.POST.get("latitude"):
        disaster.disaster_latitude = request.POST.get("latitude")
    disaster.save()
    ForecastForAdmin.objects.create(disaster_id=disaster.id,confirmed=True)
    publish(disaster.id)
    return build_success_json_response()

def modify_forewarn(request:HttpRequest):
    fid = request.POST.get("forewarn_id")
    did = ForewarnForUser.objects.filter(id=fid).first().disaster_id

    if request.POST.get("expire") == "True":
        ForewarnForUser.objects.filter(disaster_id=did).delete()
        return build_success_json_response()
    disaster = AIDisasterForecast.objects.filter(disaster_id=did)
    if request.POST.get("type"):
        disaster.disaster_type = request.POST.get("type")
    if request.POST.get("level"):
        disaster.disaster_level = request.POST.get("level")
    if request.POST.get("location"):
        disaster.disaster_location = request.POST.get("location")
    if request.POST.get("longitude"):
        disaster.disaster_longitude = request.POST.get("longitude")
    if request.POST.get("latitude"):
        disaster.disaster_latitude = request.POST.get("latitude")
    disaster.save()
    return build_success_json_response()

