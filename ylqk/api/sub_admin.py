from django.http import HttpRequest
from django.views.decorators.http import require_GET

from utils.response_util import *
from ..models.users import *
from ..models.announcement import *
from ..api.annoucement import publish, getSurroundings


def admin_create_forewarn(request: HttpRequest):
    disaster = AIDisasterForecast.objects.create(disaster_type="-1", disaster_level=-1,
                                                 disaster_location="-1", disaster_longitude=-1, disaster_latitude=-1)
    body = json.loads(request.body)
    if body.get("type"):
        disaster.disaster_type = body.get("type")
    if body.get("level"):
        disaster.disaster_level = body.get("level")
    if body.get("location"):
        disaster.disaster_location = body.get("location")
    if body.get("longitude"):
        disaster.disaster_longitude = body.get("longitude")
    if body.get("latitude"):
        disaster.disaster_latitude = body.get("latitude")
    disaster.save()
    ForecastForAdmin.objects.create(disaster_id=disaster.id, confirmed=True)
    publish(disaster.id)
    resp_body = {"status_code": StatusCode.OK.value}
    return HttpResponse(status=200, content=json.dumps(resp_body), content_type="application/json")


def admin_modify_forewarn(request: HttpRequest):
    body = json.loads(request.body)
    fid = body.get("forecast_id") #
    did = ForecastForAdmin.objects.filter(id=fid).first().disaster_id


    if body.get("expire") == "True":
        AIDisasterForecast.objects.filter(id=did).delete()
        return build_success_json_response()
    disaster = AIDisasterForecast.objects.filter(disaster_id=did)
    if body.get("type"):
        disaster.disaster_type = body.get("type")
    if body.get("level"):
        disaster.disaster_level = body.get("level")
    if body.get("location"):
        disaster.disaster_location = body.get("location")
    if body.get("longitude"):
        disaster.disaster_longitude = body.get("longitude")
    if body.get("latitude"):
        disaster.disaster_latitude = body.get("latitude")
    disaster.save()
    resp_body = {"status_code": StatusCode.OK.value}
    return HttpResponse(status=200, content=json.dumps(resp_body), content_type="application/json")
