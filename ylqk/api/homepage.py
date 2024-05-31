from django.http import HttpRequest
from django.views.decorators.http import require_GET

from utils.response_util import *
from ..models.users import *
from ..models.announcement import *

@require_GET
def get_subscriced_all(request:HttpRequest):
    uid = request.GET.get('user_id')
    cities = Subscribed.objects.filter(user_id=uid).all()
    if isinstance(cities, QuerySet) or isinstance(cities, Model):
        return build_success_json_response(cities)
    else:
        return build_failed_json_response(StatusCode.NOT_FOUND, "用户id不存在")

@require_GET
def get_all_published_disasters(request:HttpRequest):
    begin_time = datetime(1970,1,1,12,0,0,tzinfo=timezone.utc)
    if request.GET.get("begin_time"):
        begin_time = request.GET.get("begin_time")
        begin_time = datetime.strptime(begin_time,'%Y%m%d%H%M%S')
    disasters = AIDisasterForecast.objects.filter(datatime__gte=begin_time).all()
    if isinstance(disasters, QuerySet) or isinstance(disasters, Model):
        return build_success_json_response(disasters)
    else:
        return build_failed_json_response(StatusCode.NOT_FOUND, "尚无灾害预警")

def add_subscribe_city(request:HttpRequest):
    request_body = json.loads(request.body)
    uid = request_body.get("user_id")
    city = request_body.get("city")
    existing_subscription = Subscribed.objects.filter(user_id=uid, city=city).first()
    if existing_subscription:
        return build_failed_json_response(StatusCode.CONFLICT,"该订阅已经存在")
    subscribe_info = Subscribed.objects.create(user_id=uid,city=city)
    subscribe_info.save()
    resp_body = {"status_code": StatusCode.OK.value}
    return HttpResponse(status=200, content=json.dumps(resp_body), content_type="application/json")

def del_subscribe_city(request:HttpRequest):
    request_body = json.loads(request.body)
    uid = request_body.get("user_id")
    city = request_body.get("city")
    print(city)
    try:
        Subscribed.objects.filter(user_id=uid, city=city).delete()
    except Exception as e:
        build_failed_json_response(StatusCode.BAD_REQUEST,"failed to delete")
    resp_body = {"status_code": StatusCode.OK.value}
    return HttpResponse(status=200, content=json.dumps(resp_body), content_type="application/json")

def reset_password(request:HttpRequest):
    request_body = json.loads(request.body)
    uid = request_body.get("user_id")
    pwd = request_body.get('new_password')
    try:
        user = UserProfile.objects.filter(id=uid).first()
        user.password=pwd
        user.save()
    except Exception as e:
        build_failed_json_response(StatusCode.BAD_REQUEST,"用户id错误")
    return build_success_json_response()

def reset_username(request:HttpRequest):
    request_body = json.loads(request.body)
    uid = request_body.get("user_id")
    name = request_body.get('new_name')
    try:
        user = UserProfile.objects.filter(id=uid).first()
        user.username = name
        user.save()
    except Exception as e:
        build_failed_json_response(StatusCode.BAD_REQUEST, "用户id错误")
    return build_success_json_response()

def test(request:HttpRequest):
    import requests
    from ylqk.api.sub_admin import get_location_by_address
    url = "https://api.seniverse.com/v3/weather/alarm.json"
    headers = {
        'User-Agent': 'Mozilla/5.0 (iPad; CPU OS 13_3 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) CriOS/87.0.4280.77 Mobile/15E148 Safari/604.1 Edg/117.0.0.0'
    }
    param = {
        'key': 'SN_H868TafuTTtyLb',  # 私钥！！！
        'detail': 'more',
    }
    response = requests.get(url=url, params=param, headers=headers)
    data = response.json()
    for item in data['results']:
        loc = item['location']['path']
        locs = loc.split(',')
        num = len(locs)
        if num == 3:  # 直辖市
            province = locs[1]
            city = locs[1]
            district = locs[0]
        if num == 4:  # 省 or 自治区
            province = locs[2]
            city = locs[1]
            district = locs[0]
        location = province + "-" + city + "-" + ("" if city == district else district) # 省级预警不知道api什么格式、市区级预警。
        for forecast in item['alarms']:
            addr = get_location_by_address(location)
            print(loc,addr,location)
    return build_success_json_response()


