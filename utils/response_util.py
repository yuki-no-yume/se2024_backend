import json
import string
from enum import Enum

from django.http import HttpResponse


class StatusCode(Enum):
    """
    400: 客户端请求的语法错误
    401: 用户未身份认证
    403: 服务器拒绝执行该请求
    404: 服务器找不到请求的资源
    409: 服务器处理请求时发生了冲突
    500: 服务器错误
    """
    OK = 200
    BAD_REQUEST = 400
    UNAUTHORIZED = 401
    FORBIDDEN = 403
    NOT_FOUND = 404
    CONFLICT = 409
    INTERNAL_SERVER_ERROR = 500


class ResponseUtil:
    @staticmethod
    def build_success_json_response(data: object = None, message: string = "SUCCESS"):
        response = {"status_code": StatusCode.OK.value, "message": message, "data": data}
        print(json.dumps(response))
        return HttpResponse(status=200, content=json.dumps(response), content_type="application/json")

    @staticmethod
    def build_failed_json_response(status_code: StatusCode, message: string = "FAILED"):
        response = {"status_code": status_code.value, "message": message}
        print(json.dumps(response))
        return HttpResponse(status=status_code.value, content=json.dumps(response), content_type="application/json")
