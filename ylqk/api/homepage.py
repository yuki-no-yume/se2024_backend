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

def submit_more_info(request:HttpRequest): #选定管理员并申请
    if request.method == 'GET': #获取管理员列表
        admins = UserProfile.objects.filter(level='2').all()
        if isinstance(admins, QuerySet) or isinstance(admins, Model):
            return build_success_json_response(admins)
        else:
            return build_failed_json_response(StatusCode.NOT_FOUND, "尚无管理员")
    if request.method == 'POST': #向管理员提交更多信息
        uid = request.POST.get("user_id")
        aid = request.POST.get("admin_id")
        if uid and aid:
            user = UserProfile.objects.filter(id=uid).first()
            # 添加新信息,只是一段示例
            user.realname = request.POST.get("realname")
            user.age = request.POST.get("age")
            user.save()
            privateMessage = NormalMessage(sender_id=uid, receiver_id=aid, message_object_id=uid)
            privateMessage.save()
            return build_success_json_response()
        return build_failed_json_response(StatusCode.BAD_REQUEST,"人员id错误")

@require_GET
def get_all_published_disasters(request:HttpRequest):
    forecasts = ForecastForAdmin.objects.filter(confirmed=True).all()
    ids = forecasts.values_list('disaster_id', flat=True)
    disasters = AIDisasterForecast.objects.filter(id__in=ids)
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
    try:
        Subscribed.objects.filter(user_id=uid,city=city).delete()
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

def delete_test(request:HttpRequest):
    UserProfile.objects.filter().delete()
    return build_success_json_response()


