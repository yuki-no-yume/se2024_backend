from django.http import HttpRequest
from django.views.decorators.http import require_GET
import requests

from utils.response_util import *
from ..models.users import *
from ..models.announcement import *


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
        locs = get_location_by_address(body.get("location"))
        disaster.disaster_longitude = locs['lng']
        disaster.disaster_latitude = locs['lat']
    if body.get("description"):
        disaster.disaster_description = body.get("description")
    disaster.save()

    # 给审核的发一条消息
    auditor = UserProfile.objects.filter(level='3').first()

    mes = ForecastForAdmin.objects.create(status='1', send_id=aid, rec_id=auditor.id, disaster_id=disaster.id)
    if body.get("remark"):
        mes.remark = body.get("remark")
    mes.save()
    resp_body = {"status_code": StatusCode.OK.value, "message": 'SUCCESS'}
    return HttpResponse(status=200, content=json.dumps(resp_body), content_type="application/json")


def get_location_by_address(address):
    result = LocationAndAddress.objects.filter(name=address).first()
    if result:
        return {"lng": result.longitude, "lat": result.latitude}
    ak = 'riLHaKiDtfFXc8FU6qyzCMbjC2UDL9ga'
    url = f"http://api.map.baidu.com/geocoding/v3/?address={address}&output=json&ak={ak}"
    response = requests.get(url)
    result = response.json()
    if response.status_code == 200 and result.get('status') == 0:
        location = result.get('result').get('location')
        LocationAndAddress.objects.create(longitude=location['lng'],latitude=location['lat'],name=address)
        return location  # 返回形如 {'lng': 116.404, 'lat': 39.915} 的字典
    else:
        return {"lng": -1, "lat": -1}
