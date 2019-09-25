import re
import uuid
import time

from django.db import models
from django.contrib.auth.hashers import check_password, make_password

from decorator import *

tz = pytz.timezone('Asia/Shanghai')


class User(models.Model):
    username = models.CharField(
        blank=True, null=True, max_length=50, verbose_name='姓名')
    password = models.CharField(
        blank=True, null=True, max_length=100, verbose_name='密码')
    gender = models.CharField(
        blank=True, null=True, max_length=30, verbose_name='性别')
    phonenumber = models.CharField(
        max_length=30, unique=True, verbose_name='手机号')
    email = models.CharField(
        blank=True, null=True, max_length=50, verbose_name='邮箱')
    company = models.CharField(
        blank=True, null=True, max_length=200, verbose_name='班级')
    studentid = models.CharField(
        max_length=30, blank=True, null=True, verbose_name='学号')
    nation = models.CharField(
        max_length=30, blank=True, null=True, verbose_name='民族')
    hometown = models.CharField(
        max_length=30, blank=True, null=True, verbose_name='生源地')
    about = models.CharField(
        blank=True, null=True, max_length=200, verbose_name='备注')
    registerdate = models.DateTimeField(
        auto_now_add=True, blank=True, null=True, verbose_name='注册时间')
    level = models.CharField(
        default='user', max_length=20, verbose_name='用户等级')

    def toDict(self):
        return {
            "id": self.id,
            "username":  self.username if self.username else "",
            "gender": self.gender if self.gender else "",
            "phonenumber": self.phonenumber if self.phonenumber else "",
            "email": self.email if self.email else "",
            "level": self.level if self.level else "",
            "company": self.company if self.company else "",
            "studentid": self.studentid if self.studentid else "",
            "about": self.about if self.about else "",
            "registerdate": self.registerdate.astimezone(tz).strftime("%Y/%m/%d %H:%M:%S") if self.registerdate else "",
        }

    def __str__(self):
        text = "__User__\n"
        for key, value in self.toDict().items():
            text += "{}: {}\n".format(key, value)
        return text

    class Meta:
        db_table = 'user_info'


regular_list = {
    "username": "^[\u4e00-\u9fa5_a-zA-Z0-9_]{3,15}$",
    "password": "^[A-Za-z0-9]{6,16}$",
    "phonenumber": "^1[0-9]{10}$",
    "email": "[\w!#$%&'*+/=?^_`{|}~-]+(?:\.[\w!#$%&'*+/=?^_`{|}~-]+)*@(?:[\w](?:[\w-]*[\w])?\.)+[\w](?:[\w-]*[\w])?",
}


def getAllUsers():
    return User.objects.filter(level="user").order_by("id").all()


def addUsers(users):
    for u in users:
        appendUser(u["username"], u["phonenumber"], u["gender"],
                   u["company"], u["studentid"], u["email"], u["about"])


def appendUser(username, phonenumber, gender, company, studentid, email, about):
    user = getOrCreateUserByPhonenumber(phonenumber)
    user.username = username
    user.gender = gender
    user.company = company
    user.studentid = studentid
    user.email = email
    user.about = about
    user.save()


def removeUser(phonenumber):
    User.objects.filter(phonenumber=phonenumber).delete()


def getUserByID(user_id=None):

    if User.objects.filter(id=user_id).count():
        user = User.objects.get(id=user_id)
    else:
        raise RFSException("10032", "查无此人")
    return user


def getOrCreateUserByPhonenumber(phonenumber):
    if User.objects.filter(phonenumber=phonenumber).exists():
        user = User.objects.get(phonenumber=phonenumber)
    else:
        user = createUser(phonenumber=phonenumber)
    return user


def getUserByPassword(username=None, password=None):
    if username == None or password == None:
        raise ParamException()
    user = None
    if User.objects.filter(username=username).count():
        user = User.objects.get(username=username)
    elif User.objects.filter(phonenumber=username).count():
        user = User.objects.get(phonenumber=username)
    elif User.objects.filter(email=username).count():
        user = User.objects.get(email=username)
    else:
        raise RFSException("10011", "姓名不存在")
    if check_password(password, user.password):
        print("验证成功")
        return user
    else:
        raise RFSException("10012", "密码错误")
    # TODO
    raise RFSException("10013", "登录受限")


def makeUserId():
    uid = "u0" + hex(int(time.time()*1000000))[2:] + \
        "-" + str(uuid.uuid4())
    return uid[:29]


def createUser(username=None, password=None, gender=None, phonenumber=None, email=None):
    if not username:
        username = makeUserId()
    if User.objects.filter(phonenumber=phonenumber).exists():
        user = User.objects.get(phonenumber=phonenumber)
        raise RFSException("10004", "手机号重复")
    # else:
    #     if not re.match(regular_list["phonenumber"], phonenumber, flags=0):
    #         raise RFSException("10005", "手机号非法")
    user = User.objects.create(
        username=username,
        password=make_password(password),
        gender=gender,
        phonenumber=phonenumber,
        email=email,
    )
    return user


def setUserInfo(user_id, key, value):  # 弃用
    user = getUserByID(user_id)
    if key == None or value == None:
        raise ParamException()
    if key not in ["username", "password", "phonenumber", "email", "about"]:
        raise RFSException("10042", "未知属性")
    if key in ["username", "password", "phonenumber", "email"]:
        if not re.match(regular_list[key], value, flags=0):
            raise RFSException("10043", "参数"+key+"格式错误")
    if key == "username":
        user.username = value
    elif key == "password":
        user.password = make_password(value)
    elif key == "phonenumber":
        user.phonenumber = value
    elif key == "email":
        user.email = value
    elif key == "about":
        user.about = value
    user.save()
    # user.login(request)
    return user
