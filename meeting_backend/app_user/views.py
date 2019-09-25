from django.shortcuts import render
from decorator import *
from django.contrib.auth.hashers import check_password, make_password
from django.http import HttpResponse
from django.shortcuts import render

from .models import *
import json


def test(param):
    print(param)
    return {
        "ok": "ok"
    }


@admin
@service
def allusers(param):
    interface_id = "1101"
    try:
        users = getAllUsers()
    except RFSException as e:
        return pack(interface_id, e.ret, e.msg)
    except Exception as e:
        return pack(interface_id, interface_id+'0', str(e))
    resp = {"users": [user.toDict() for user in users]}
    return pack(interface_id=interface_id, data=resp)


@admin
@service
def addusers(param):
    interface_id = "1111"
    users = param.get('users', None)
    print("users")
    try:
        users = json.loads(users)
        for index, u in enumerate(users):
            users[index]["username"] = u.get("姓名", None)
            users[index]["phonenumber"] = u.get("手机号", None)
            users[index]["gender"] = u.get("性别", None)
            users[index]["company"] = u.get("班级", None)
            users[index]["studentid"] = u.get("学号", None)
            users[index]["email"] = u.get("邮箱", None)
            users[index]["about"] = u.get("备注", None)
        addUsers(users)
        users = getAllUsers()
    except RFSException as e:
        return pack(interface_id, e.ret, e.msg)
    except Exception as e:
        return pack(interface_id, interface_id+'0', str(e))
    resp = {"users": [user.toDict() for user in users]}
    return pack(interface_id=interface_id, data=resp)


@admin
@service
def appenduser(param):
    interface_id = "1110"
    username = param.get('username', None) or param.get('name', None)
    phonenumber = param.get('phonenumber', None)
    gender = param.get('gender', None)
    company = param.get('company', None)
    studentid = param.get('studentid', None)
    email = param.get('email', None)
    about = param.get('about', None)
    try:
        appendUser(username, phonenumber, gender,
                   company, studentid, email, about)
        users = getAllUsers()
    except RFSException as e:
        return pack(interface_id, e.ret, e.msg)
    except Exception as e:
        return pack(interface_id, interface_id+'0', str(e))
    resp = {"users": [user.toDict() for user in users]}
    return pack(interface_id=interface_id, data=resp)


@admin
@service
def removeuser(param):
    interface_id = "1112"
    phonenumber = param.get('phonenumber', None)
    try:
        removeUser(phonenumber)
        users = getAllUsers()
    except RFSException as e:
        return pack(interface_id, e.ret, e.msg)
    except Exception as e:
        return pack(interface_id, interface_id+'0', str(e))
    resp = {"users": [user.toDict() for user in users]}
    return pack(interface_id=interface_id, data=resp)


@logout
@service
def log_in(param):
    # Auth: ZhengYiming
    # Date: 2019.4.12
    request = None
    interface_id = "1001"
    print("LOGIN...")
    username = param.get('username', None)
    password = param.get('password', None)
    print(param)
    try:
        user = getUserByPassword(username, password)
        token = constructToken(user.id, user.username, user.level)
    except RFSException as e:
        return pack(interface_id, e.ret, e.msg)
    except Exception as e:
        return pack(interface_id, interface_id+'0', str(e))
    # user.login(request)
    resp = {
        "user": user.toDict(),
        "token": token,
    }
    return pack(interface_id, data=resp)


@login
@service
def decodeToken(param):
    interface_id = "token"
    token = param.get("token", None)
    token_data = verifyToken(token)
    resp = {
        "user": token_data,
        "token": token
    }
    if token_data:
        return pack(interface_id, data=resp)
    else:
        return pack(interface_id, "token_verify_fail", "无效token, 请重新登录")


@logout
@service
def register(param):
    interface_id = "1000"
    username = param.get('username', None)
    password = param.get('password', None)
    gender = param.get('gender', None)
    phonenumber = param.get('phonenumber', None)
    email = param.get('email', None)

    try:
        user = createUser(username, password, gender, phonenumber, email)
    except RFSException as e:
        return pack(interface_id, e.ret, e.msg)
    except Exception as e:
        return pack(interface_id, interface_id+'0', str(e))
    resp = {"user": user.toDict()}
    return pack(interface_id=interface_id, data=resp)


@logout
@service
def log_out(param):
    interface_id = "1002"
    return pack(interface_id, "0", "成功", {})


@login
@service
def userinfo(param):
    interface_id = "1003"
    target_user_id = param.get('user_id', None)
    user_id = param["user"]['userid']
    level = param["user"]['level']
    try:
        user = getUserByID(target_user_id, user_id)
    except RFSException as e:
        return pack(interface_id, e.ret, e.msg)
    except Exception as e:
        return pack(interface_id, interface_id+'0', str(e))
    resp = {"user": user.toDict()}
    return pack(interface_id=interface_id, data=resp)


@login
@service
def set_userinfo(param):
    interface_id = "1004"
    user_id = param["user"]['userid']
    key = param.get('key', None)
    value = param.get('value', None)
    try:
        user = setUserInfo(user_id, key, value)
    except RFSException as e:
        return pack(interface_id, e.ret, e.msg)
    except Exception as e:
        return pack(interface_id, interface_id+'0', str(e))
    resp = {"user": user.toDict()}
    return pack(interface_id=interface_id, data=resp)
