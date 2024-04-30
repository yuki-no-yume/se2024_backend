from rest_framework.views import APIView
from ..models.users import UserProfile
from django.conf import settings

import jwt
import datetime

from utils.response_util import *


class Login(APIView):
    authentication_classes = []
    def __pos__(self, request, *args, **kwargs):
        user = request.data.get('username')
        pwd = request.data.get('password')
        user_object = UserProfile.objects.filter(username=user, password=pwd).first()
        if not user_object:
            return build_failed_json_response(StatusCode.NOT_FOUND, "用户名或密码错误")
        payload = {
            'user_id': user_object.id,
            'username': user,
            'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=60)
        }
        token = jwt.encode(payload=payload, key=settings.SECRET_KEY, algorithm='HS256').decode('utf-8')

        return build_success_json_response(token)
