import datetime

from django.conf import settings
from django.http import HttpRequest
from rest_framework.authentication import BaseAuthentication
from django.utils.deprecation import MiddlewareMixin
from rest_framework.exceptions import AuthenticationFailed
import jwt

from .response_util import *
from ylqk.models.users import UserProfile


class JwtQueryParamsAuthentication(MiddlewareMixin):
    def process_request(self, request):
        excluded_paths = [
            '/admin',
            '/ylqk/login',
            '/ylqk/register',
            '/ylqk/retrieve',
            '/ylqk/test',
            # '/ylqk',
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
        if user and user.level == '1' and 'admin' in request.path: # 保证每个仅管理员可用的页面包含admin
            raise AuthenticationFailed(StatusCode.UNAUTHORIZED, "权限不足")
        #2，3
        return

def TokenRefresh(request:HttpRequest):
    token = request.headers.get('Authorization')
    refresh_token = token.split(' ')[1]

    try:
        payload = jwt.decode(refresh_token, settings.SECRET_KEY, algorithms=['HS256'])
    except jwt.ExpiredSignatureError:
        raise AuthenticationFailed(StatusCode.BAD_REQUEST, "请重新登录")
    except Exception as e:
        raise AuthenticationFailed(StatusCode.UNAUTHORIZED, "refresh_token无效")
    access_payload = payload.copy()
    refresh_payload = payload.copy()
    access_payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(minutes=150)
    access_token = jwt.encode(payload=access_payload, key=settings.SECRET_KEY, algorithm='HS256')
    refresh_payload['exp'] = datetime.datetime.utcnow() + datetime.timedelta(hours=12)
    refresh_token = jwt.encode(payload=refresh_payload, key=settings.SECRET_KEY, algorithm='HS256')
    message = '请更新客户端token'
    data = {
        "access_token":access_token,
        "refresh_token":refresh_token,
    }
    resp_body = {"status_code": StatusCode.OK.value, "message": message, "data": data}
    return HttpResponse(status=200, content=json.dumps(resp_body), content_type="application/json")



