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
