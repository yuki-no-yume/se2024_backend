from itertools import chain

from django.http import HttpRequest
from django.views.decorators.http import require_GET
from django.db import transaction
from django.dispatch import receiver
from django.db.models.signals import post_save
from polymorphic.query import PolymorphicQuerySet
from utils.api import *

from utils.response_util import *
from ..models.announcement import *
from ..models.users import *


@require_GET
def get_unread_number(request: HttpRequest):
    id = request.GET.get("user_id")
    user = UserProfile.objects.filter(id=id).first()
    forewarn = ForewarnForUser.objects.filter(user_id=id,read=False).all()  # 订阅信息
    sysinfo = ApplicationForGlobal.objects.filter(read=False).all()
    admincorres = None
    if user.level == '2' or user.level == '3':
        admincorres = ForecastForAdmin.objects.filter(rec_id=id,read=False).all()
    size1 = len(forewarn) if forewarn else 0
    size2 = len(sysinfo) if sysinfo else 0
    size3 = len(admincorres) if admincorres else 0
    size = size1 + size2 + size3
    data = {"size":size}
    resp_body = {"status_code": StatusCode.OK.value, "message": 'SUCCESS', "data": data}
    return HttpResponse(status=200, content=json.dumps(resp_body), content_type="application/json")

@require_GET
def get_all_mails(request: HttpRequest):
    id = request.GET.get("user_id")
    user = UserProfile.objects.filter(id=id).first()
    forewarn = ForewarnForUser.objects.filter(user_id=id).all()  # 订阅信息
    sysinfo = ApplicationForGlobal.objects.all()
    admincorres = []
    if user.level == '2' or user.level == '3':
        admincorres = ForecastForAdmin.objects.filter(rec_id=id).all()
    result = list(chain(forewarn, sysinfo, admincorres))
    sorted_result = sorted(result, key=lambda x: x.time)
    return build_success_json_response(sorted_result)


@require_GET
def get_mail_by_id(request: HttpRequest):  # 判断该用户是否能获得该邮件
    id = request.GET.get("id")
    uid = request.GET.get('user_id')
    mail = Announcement.objects.filter(id=id).first()
    if isinstance(mail, QuerySet) or isinstance(mail, Model):
        if (isinstance(mail,ForecastForAdmin) and str(mail.rec.id)==uid) or \
                (isinstance(mail,ForewarnForUser) and str(mail.user.id) == uid):
            mail.read = True
            mail.save()
            return build_success_json_response(mail)
    return build_failed_json_response(StatusCode.NOT_FOUND, "该信息不存在")

def get_forecast_from_api(request:HttpRequest):
    get_period_forecast()
    return build_success_json_response()


def tackle_mail_by_id(request: HttpRequest):  # 2、3管理员功能
    body = json.loads(request.body)
    id = body.get("mid")
    mail = Announcement.objects.instance_of(ForecastForAdmin).filter(id=id).first()
    if (isinstance(mail, QuerySet) or isinstance(mail, Model)) and isinstance(mail, ForecastForAdmin):
        status = mail.status
        rec_id = mail.rec.id
        rec = UserProfile.objects.filter(id=rec_id).first()
        send_id = mail.send.id
        # send = UserProfile.objects.filter(id=send_id).first()
        disaster = mail.disaster
        if rec.level == '2':  # 发布管理员
            if status == '2':  # 被打回、修改或删除
                if body.get("mode") == 'expire':
                    return build_success_json_response()
                elif body.get("mode") == 'revise':  # 修改
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
                    mes = ForecastForAdmin.objects.create(status='3', send_id=rec_id, rec_id=send_id,
                                                          disaster_id=disaster.id)
                    if body.get("remark"):
                        mes.remark = body.get("remark")
                    mes.save()
                    return build_success_json_response()
        elif rec.level == "3":  # 审核
            if status == '3' or status == '1':  # 修改后提交
                if body.get('mode') == 'expire':
                    mes = ForecastForAdmin.objects.create(status='5', send_id=rec_id, rec_id=send_id,
                                                          disaster_id=disaster.id)
                    if body.get("remark"):
                        mes.remark = body.get("remark")
                    mes.save()
                    return build_success_json_response()
                elif body.get("mode") == 'revise':
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
                    mes = ForecastForAdmin.objects.create(status='4', send_id=rec_id, rec_id=send_id,
                                                          disaster_id=disaster.id)
                    if body.get("remark"):
                        mes.remark = body.get("remark")
                    mes.save()
                    publish(disaster.id)
                    return build_success_json_response()
                elif body.get("mode") == 'return':
                    if status == '1':
                        mes = ForecastForAdmin.objects.create(status='2', send_id=rec_id, rec_id=send_id,
                                                              disaster_id=disaster.id)
                        if body.get("remark"):
                            mes.remark = body.get("remark")
                        mes.save()
                        return build_success_json_response()
        return build_failed_json_response(StatusCode.BAD_REQUEST, "权限不足")
    return build_failed_json_response(StatusCode.NOT_FOUND, "该信息不存在")


def publish(did):
    disaster = AIDisasterForecast.objects.filter(id=did).first()
    if disaster:
        users = getSurroundings(disaster.disaster_location)
        for user in users:
            userMes = ForewarnForUser(disaster_id=did, user_id=user.id)
            userMes.save()


# 最长匹配
def getSurroundings(loc):
    users = []

    locs = loc.split("-")
    min_loc = [unit.strip() for unit in locs if unit.strip()][-1]
    subscribes = Subscribed.objects.all()
    for item in subscribes:
        unit = item.city
        tmp = unit.split("-")
        min_unit = [part.strip() for part in tmp if part.strip()][-1]
        if min_loc in unit or min_unit in loc:
            users.append(item.user)
    unique_list = list(set(users))
    return unique_list
