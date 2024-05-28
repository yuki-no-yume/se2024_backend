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
    aid = body.get("user_id")
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
    if body.get("description"):
        disaster.disaster_description = body.get("description")
    disaster.save()
    # 给审核的发一条消息
    auditor = UserProfile.objects.filter(level='3').first()

    mes = ForecastForAdmin.objects.create(status='1',send_id=aid,rec_id=auditor.id,disaster_id=disaster.id)
    if body.get("remark"):
        mes.remark = body.get("remark")
    mes.save()
    resp_body = {"status_code": StatusCode.OK.value, "message": 'SUCCESS'}
    return HttpResponse(status=200, content=json.dumps(resp_body), content_type="application/json")
