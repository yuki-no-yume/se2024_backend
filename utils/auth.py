from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from django.utils.deprecation import MiddlewareMixin
from rest_framework.exceptions import AuthenticationFailed
import jwt

from .response_util import *


class JwtQueryParamsAuthentication(MiddlewareMixin):

    def process_request(self, request):
        token = request.GET.get('token')
        verified_paylout = None
        try:
            verified_payload = jwt.decode(token, settings.SECRET_KEY, True)
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed(StatusCode.UNAUTHORIZED, "登录超时")
        except Exception as e:
            raise AuthenticationFailed(StatusCode.UNAUTHORIZED, "认证失败")
        return (verified_payload,token)

