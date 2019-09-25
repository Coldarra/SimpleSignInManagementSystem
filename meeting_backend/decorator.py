import datetime
import json
import time

import pytz
from cryptography.fernet import Fernet
from django.http import HttpResponse
from django.conf import settings


cipher_key = b'BxgJ3nXVtc8ErKdoD7gx7R0TkK1x4U8GYMSwcbHH7WE='
cipher = Fernet(cipher_key)


class RFSException(Exception):
    def __init__(self, ret="-1", msg="Exception!"):
        self.ret = ret
        self.msg = msg
        if settings.DEBUG:
            print(self)

    def __str__(self):
        return "\033[3;31;40m__RFSException__\nret: {}\nmsg: {}\033[0m\n".format(self.ret, self.msg)


class ParamException(RFSException):
    def __init__(self, ret="110", msg="参数非法"):
        self.ret = ret
        self.msg = msg


class NoJurisdictionException(RFSException):
    def __init__(self, ret="11", msg="权限不足"):
        self.ret = ret
        self.msg = msg


def service(func):
    def wrapper(request, *args, **kw):
        if settings.DEBUG:
            print('call %s():' % func.__name__)
        param = {
            "user": getUserInfo(request),
            "token": getToken(request)
        }
        for k, v in request.GET.items():
            param[k] = v
        for k, v in request.POST.items():
            param[k] = v
        # print(param)

        if settings.DEBUG:
            print("\033[3;31;33m__PARAM__\n{}\033[0m\n".format(param))
        return func(param, * args, **kw)
    return wrapper


def pack(interface_id="null", ret="0", msg="成功", data={}):
    '''interface_id, ret, msg, data'''

    if settings.DEBUG:
        print("\033[1;36m——PACK——\ninterface_id: {}\nret: {}\nmsg: {}\ndata: {}\n\033[0m".format(
            interface_id, ret, msg, data))
    resp = {
        "ret": str(ret),
        "msg": "({}){}".format(interface_id, msg),
        "data": data,
    }
    try:
        response = HttpResponse(content=json.dumps(
            resp), status=200, content_type="application/json")
        response['Access-Control-Allow-Origin'] = '*'
        response['Access-Control-Allow-Headers'] = '*'
        return response
    except Exception as e:
        if settings.DEBUG:
            print(
                "\033[1;32m数据打包出错\nException: {}\ndata: {}\033[0m".format(e, data))
        return pack(interface_id, -1, "数据打包出错")


def post(func):
    def wrapper(request, *args, **kw):
        if settings.DEBUG:
            print('call %s():' % func.__name__)
        if request.method != "POST":
            return pack("method", "100", "接口调用方式错误")
        return func(request, *args, **kw)
    return wrapper


def get(func):
    def wrapper(request, *args, **kw):
        print('call %s():' % func.__name__)
        print(request)
        if request.method != "GET":
            return pack("method", "100", "接口调用方式错误")
        return func(request, *args, **kw)
    return wrapper


def login(func):
    def wrapper(request, *args, **kw):
        token = getToken(request)
        token = verifyToken(token)
        if not token:
            return pack("login", "10", "未登录")
        return func(request, *args, **kw)
    return wrapper


def logout(func):
    def wrapper(request, *args, **kw):
        print('call %s():' % func.__name__)
        print("logout")
        return func(request, *args, **kw)
    return wrapper


# @login
def admin(func):
    def wrapper(request, *args, **kw):
        if settings.DEBUG:
            print('call %s():' % func.__name__)
        userInfo = getUserInfo(request)
        # print(userInfo)
        if not userInfo.get('level', None):
            return pack("login", "10", "未登录")
        if userInfo.get('level', None) != 'admin':
            return pack("admin", "11", "权限不足")
        return func(request, *args, **kw)
    return wrapper


def constructToken(userid=None, username=None, level=None):
    token_data = {
        "userid": userid,
        "username": username,
        "level": level,
        "time": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
    }
    token = 'Bearer ' + str(cipher.encrypt(
        bytes(json.dumps(token_data).encode('utf-8'))), encoding='utf-8')
    # print(token, "\n", verifyToken(token))
    return token


def getToken(request):
    return request.META.get("HTTP_AUTHORIZATION", None)


def getUserInfo(request):
    token = getToken(request)
    token_data = verifyToken(token)
    if token_data:
        return token_data
    else:
        return {
            "userid": None,
            "username": None,
            "level": None,
            "time": None,
        }


def verifyToken(token):
    # print(token)
    try:
        if token[:6] == "Bearer":
            token = token[7:]
        decrypt_data = cipher.decrypt(bytes(token, encoding="utf-8"))
        data = json.loads(decrypt_data)
        data["token"] = token
        # print("data:", data)
        return data
    except Exception as e:
        # print("Exception:", e)
        return None
