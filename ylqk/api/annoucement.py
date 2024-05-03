from django.http import HttpRequest
from django.views.decorators.http import require_GET
from django.db import transaction
from django.dispatch import receiver
from django.db.models.signals import post_save
from polymorphic.query import PolymorphicQuerySet

from utils.response_util import *
from ..models.announcement import *
from ..models.users import *

@require_GET
def get_admins_all(request:HttpRequest):
    mails = ForecastForAdmin.objects.filter().all()
    if isinstance(mails,QuerySet) or isinstance(mails,Model):
        return build_success_json_response(mails)
    else:
        return build_failed_json_response(StatusCode.NOT_FOUND,"尚无灾害预测信息")

@require_GET
def get_users_all(request:HttpRequest):
    id = request.GET.get("user_id")
    mails = ForewarnForUser.objects.filter(user_id=id).filter().all()
    if isinstance(mails,QuerySet) or isinstance(mails,Model):
        return build_success_json_response(mails)
    else:
        return build_failed_json_response(StatusCode.NOT_FOUND,"尚无灾害预警信息")

def get_private_all(request:HttpRequest): #还可以有个已发送？
    id = request.GET.get("user_id")
    mails = NormalMessage.objects.filter(receiver_id=id).filter(),all()
    if isinstance(mails,QuerySet) or isinstance(mails,Model):
        return build_success_json_response(mails)
    else:
        return build_failed_json_response(StatusCode.NOT_FOUND,"尚无灾害预警信息")


@require_GET
def get_system_all(request:HttpRequest):
    mails = ApplicationForGlobal.objects.filter().all()
    if isinstance(mails, QuerySet) or isinstance(mails, Model):
        return build_success_json_response(mails)
    else:
        return build_failed_json_response(StatusCode.NOT_FOUND, "尚无系统信息")
## 可以查看

@require_GET
def get_mail_by_id(request:HttpRequest):
    id = request.GET.get("id")
    mail = Announcement.objects.instance_of(ForecastForAdmin).filter(id=id).first()
    if isinstance(mail, QuerySet) or isinstance(mail, Model):
        return build_success_json_response(mail)
    else:
        return build_failed_json_response(StatusCode.NOT_FOUND, "该信息不存在")


def tackle_mail_by_id(request:HttpRequest):
    id = request.POST.get("id")
    with transaction.atomic():
        mail = Announcement.objects.instance_of(Announcement).filter(id=id).filter().first()
        if isinstance(mail, QuerySet) or isinstance(mail, Model):
            if isinstance(mail, NormalMessage) and request.POST.get("confirm") == "True":  # 同意
                ob = UserProfile.objects.filter(id=mail.message_object.id)
                ob.level = '2'
                ob.save()
            elif isinstance(mail, ForecastForAdmin) and mail.confirmed == False:  # 尚未被确认
                mail.confirmed = True
                if request.POST.get("confirm") == 'True':
                    publish(mail.disaster.id)
            return build_success_json_response()

        else:
            return build_failed_json_response(StatusCode.NOT_FOUND, "该信息不存在")


def publish(did):
    disaster = AIDisasterForecast.objects.filter(id=did).first()
    if isinstance(disaster, QuerySet) or isinstance(disaster, Model):
        cities = getSurroundings(disaster.disaster_latitude,disaster.disaster_longitude)
        users = Subscribed.objects.filter(city__in=cities)
        for user in users:
            userMes = ForewarnForUser(disaster_id=did,user_id=user.id)
            userMes.save()

# 返回通知城市列表
def getSurroundings(la,long):
    cities = []
    return cities

#
#
# @receiver(post_save, sender=announcement.ApplicationForGlobal)
# def system_signal(sender, instance, created, **kwargs):
#     if created:
#         data = {
#             "id": instance.id,
#             "time": instance.datetime,
#             "content": instance.content,
#         }
#         return build_success_json_response(data)
