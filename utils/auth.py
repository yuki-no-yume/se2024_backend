from django.conf import settings
from rest_framework.authentication import BaseAuthentication
from django.utils.deprecation import MiddlewareMixin
from rest_framework.exceptions import AuthenticationFailed
import jwt

from .response_util import *
from ylqk.models.users import UserProfile


class JwtQueryParamsAuthentication(MiddlewareMixin):

    def process_request(self, request):
        excluded_paths = [
            '/admin/',
            '/ylqk/login',
            '/ylqk/register',
        ]
        if any(request.path.startswith(path) for path in excluded_paths):
            return
        try:
            token = request.headers.get('Authorization')
            token = token.split(' ')[1]
            verified_payload = None
            verified_payload = jwt.decode(token, settings.SECRET_KEY, algorithms=['HS256'])
        except jwt.ExpiredSignatureError:
            raise AuthenticationFailed(StatusCode.BAD_REQUEST, "登录超时")
        except Exception as e:
            raise AuthenticationFailed(StatusCode.UNAUTHORIZED, "认证失败")
        id = verified_payload['user_id']
        user = UserProfile.objects.filter(id=id).first()
        if user and user.level == '1' and 'admin' in request.path:
            raise AuthenticationFailed(StatusCode.UNAUTHORIZED, "权限不足")
        return