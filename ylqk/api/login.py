import json

from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from ..models.users import UserProfile
from django.conf import settings
from django.core.mail import send_mail
import random
# from celery import shared_task
import datetime
from django.utils import timezone

import jwt

from utils.response_util import *


class Login(APIView):
    authentication_classes = []

    # @csrf_exempt
    # @api_view(['POST'])
    def post(self, request, *args, **kwargs):
        body_data = request.body.decode('utf-8')  # 解码请求体数据为字符串
        try:
            data_dict = json.loads(body_data)  # 将字符串解析为字典
            name = data_dict.get('username')
            pwd = data_dict.get('password')
            user_object = UserProfile.objects.filter(username=name).first()
            if (not user_object) or (user_object.confirmed==False):
                return build_failed_json_response(StatusCode.OK,"用户不存在")
            elif not user_object.password == pwd:
                return build_failed_json_response(StatusCode.OK, "密码错误")
        except Exception as e:
            return build_failed_json_response(StatusCode.BAD_REQUEST, "请提供有效的用户名密码")
        payload = {
            'user_id': user_object.id,
            'username': user_object.username,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=900)
        }
        result = user_object.to_dict()
        access_token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm='HS256')
        result['access_token'] = access_token
        refresh_payload = payload.copy()
        refresh_payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=5)
        refresh_token = jwt.encode(payload=refresh_payload, key=settings.SECRET_KEY, algorithm='HS256')
        result['refresh_token'] = refresh_token
        return build_success_json_response(result)


class Register(APIView):
    authentication_classes = []

    # @csrf_exempt
    # @api_view(['POST'])
    def post(self, request, *args, **kwargs):
        body_data = request.body.decode('utf-8')  # 解码请求体数据为字符串
        data_dict = json.loads(body_data)

        try :
            if data_dict.get("register_type") == 'get_verification_code':
                user_email = data_dict.get('email')
                user = UserProfile.objects.filter(email=user_email).first()
                if user:
                    if user.confirmed:
                        return build_failed_json_response(StatusCode.NOT_FOUND, '该邮箱已注册')
                else:
                    user = UserProfile.objects.create(email=user_email)
                    user.save()
                res_code = send_sms_code(user_email)
                if res_code:
                    user.ver_code = res_code
                    user.time = timezone.now()
                    user.save()
                    resp_body = {"status_code": StatusCode.OK.value, "message": 'SUCCESS'}
                    return HttpResponse(status=200, content=json.dumps(resp_body), content_type="application/json")
                else:
                    return build_failed_json_response(StatusCode.BAD_REQUEST, "发送邮件失败，请稍后再试")

            elif data_dict.get("register_type") == 'confirm':
                mail = data_dict.get("email")
                user = UserProfile.objects.filter(email=mail).first()
                if not user:
                    return build_failed_json_response(StatusCode.NOT_FOUND, '用户邮箱错误')
                if user.confirmed:
                    return build_failed_json_response(StatusCode.BAD_REQUEST, "用户已成功注册")
                user_code = data_dict.get("user_code")
                print(user.to_dict())
                dif = timezone.now() - user.time
                print(dif)
                if not user_code == user.ver_code:
                    return build_failed_json_response(StatusCode.BAD_REQUEST, "验证码无效")
                if dif > datetime.timedelta(minutes=10):
                    return build_failed_json_response(StatusCode.BAD_REQUEST, "验证码过期，请重新获取")
                user.confirmed = True
                if data_dict.get('username'):  # 默认是邮件
                    user.username = data_dict.get('username')
                if data_dict.get('password'):  # 默认是111111
                    user.password = data_dict.get('password')
                user.save()

                # 成功创建用户
                payload = {
                    'user_id': user.id,
                    'username': user.username,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=150)
                }
                result = user.to_dict()
                access_token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm='HS256')
                result['access_token'] = access_token
                refresh_payload = payload.copy()
                refresh_payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(hours=12)
                refresh_token = jwt.encode(payload=refresh_payload, key=settings.SECRET_KEY, algorithm='HS256')
                result['refresh_token'] = refresh_token
                return build_success_json_response(result)
        except Exception as e:
            return build_failed_json_response(StatusCode.BAD_REQUEST,e.__cause__)
        return build_failed_json_response(StatusCode.BAD_REQUEST, '缺少必填字段')


class Retrieve(APIView):
    authentication_classes = []

    # @csrf_exempt
    # @api_view(['POST'])
    def post(self, request, *args, **kwargs):
        body_data = request.body.decode('utf-8')  # 解码请求体数据为字符串
        data_dict = json.loads(body_data)

        try :
            if data_dict.get("retrieve_type") == 'get_verification_code':
                user_email = data_dict.get('email')
                user = UserProfile.objects.filter(email=user_email).first()
                if (not user) or (user.confirmed == False):
                    return build_failed_json_response(StatusCode.NOT_FOUND, '该邮箱尚未注册')
                res_code = send_sms_code(user_email)
                if res_code:
                    user.ver_code = res_code
                    user.time = timezone.now()
                    user.save()
                    resp_body = {"status_code": StatusCode.OK.value, "message": 'SUCCESS'}
                    return HttpResponse(status=200, content=json.dumps(resp_body), content_type="application/json")
                else:
                    return build_failed_json_response(StatusCode.BAD_REQUEST, "发送邮件失败，请稍后再试")

            if data_dict.get("retrieve_type") == 'confirm':
                mail = data_dict.get("email")
                user = UserProfile.objects.filter(email=mail).first()
                if not user:
                    return build_failed_json_response(StatusCode.NOT_FOUND,'用户邮箱错误')
                user_code = data_dict.get("user_code")
                dif = timezone.now() - user.time
                if not user_code == user.ver_code:
                    return build_failed_json_response(StatusCode.BAD_REQUEST,"验证码无效")
                if dif > datetime.timedelta(minutes=10):
                    return build_failed_json_response(StatusCode.BAD_REQUEST, "验证码过期，请重新获取")
                new_pwd = data_dict.get('new_password')
                user.password = new_pwd
                user.save()
                payload = {
                    'user_id': user.id,
                    'username': user.username,
                    'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=150)
                }
                result = user.to_dict()
                access_token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm='HS256')
                result['access_token'] = access_token
                refresh_payload = payload.copy()
                refresh_payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(hours=12)
                refresh_token = jwt.encode(payload=refresh_payload, key=settings.SECRET_KEY, algorithm='HS256')
                result['refresh_token'] = refresh_token
                return build_success_json_response(result)
        except Exception as e:
            return build_failed_json_response(StatusCode.BAD_REQUEST,'缺少必填字段')
        return build_failed_json_response(StatusCode.BAD_REQUEST,'缺少必填字段')


# @shared_task
def send_sms_code(to_email):
    sms_code = '%06d' % random.randint(0, 999999)
    EMAIL_FROM = "se2024_ylqk@163.com"  # 邮箱来自
    email_title = '账号激活'
    email_body = "【云岚乾坤】验证码 {0} 用于邮箱验证，10分钟内有效，请勿泄露和转发。如非本人操作，请忽略此邮件。".format(sms_code)
    send_status = send_mail(email_title, email_body, EMAIL_FROM, [to_email])
    if send_status:
        send_status = sms_code
    return send_status