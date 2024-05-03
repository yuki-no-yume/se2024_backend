from django.views.decorators.csrf import csrf_exempt
from rest_framework.decorators import api_view
from rest_framework.views import APIView
from ..models.users import UserProfile
from django.conf import settings

import jwt
import datetime

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
            user_object = UserProfile.objects.filter(username=name, password=pwd).first()
            if not user_object:
                return build_failed_json_response(StatusCode.NOT_FOUND, "用户名或密码错误")
        except Exception as e:
            return build_failed_json_response(StatusCode.BAD_REQUEST, "请提供有效的用户名密码")
        payload = {
            'user_id': user_object.id,
            'username': name,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        }
        token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm='HS256')
        resp_body = {"status_code": StatusCode.OK.value, "message": 'SUCCESS', "data": {'token':token}}
        return HttpResponse(status=200, content=json.dumps(resp_body), content_type="application/json")


class Register(APIView):
    authentication_classes = []

    # @csrf_exempt
    # @api_view(['POST'])
    def post(self, request, *args, **kwargs):
        body_data = request.body.decode('utf-8')  # 解码请求体数据为字符串
        try:
            data_dict = json.loads(body_data)  # 将字符串解析为字典
            name = data_dict.get('username')
            pwd = data_dict.get('password')
            newUser = UserProfile(username=name, password=pwd, level='1')
            newUser.save()
        except Exception as e:
            return build_failed_json_response(StatusCode.BAD_REQUEST,"请提供有效的用户名密码")
        payload = {
            'user_id': newUser.id,
            'username': name,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        }
        token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm='HS256')
        resp_body = {"status_code": StatusCode.OK.value, "message": 'SUCCESS', "data": {'token':token}}
        return HttpResponse(status=200, content=json.dumps(resp_body), content_type="application/json")
