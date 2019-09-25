import datetime
import time
import uuid

from decorator import *
from django.db import models, connection, transaction

from app_user.models import *


tz = pytz.timezone('Asia/Shanghai')

# id
# 会议名称
# 会议logo
# 会议时间 开始，结束
# 报名时间
# 举办地点 one
# 主办单位 many
# 协办单位 many
# 会议内容

# 与会人员 - id


class Meeting(models.Model):
    id = models.CharField(max_length=60, primary_key=True)
    name = models.CharField(max_length=50, verbose_name='会议名称')
    meeting_startdate = models.DateTimeField(
        blank=True, null=True, verbose_name='会议开始时间')
    meeting_finishdate = models.DateTimeField(
        blank=True, null=True, verbose_name='会议结束时间')
    signup_startdate = models.DateTimeField(
        blank=True, null=True, verbose_name='报名开始时间')
    signup_finishdate = models.DateTimeField(
        blank=True, null=True, verbose_name='报名结束时间')
    venue = models.TextField(blank=True, null=True, verbose_name='举办地点')
    organizer = models.CharField(
        blank=True, null=True, max_length=255,  verbose_name='主办单位')
    co_organizer = models.CharField(
        blank=True, null=True, max_length=255,  verbose_name='协办单位')
    content = models.TextField(blank=True, null=True, verbose_name='会议内容')
    adddate = models.DateTimeField(auto_now_add=True,
                                   blank=True, null=True, verbose_name='添加时间')

    def toDict(self):
        return {
            "id": self.id,
            "name": self.name or "",
            "logo": "",
            "meeting_startdate": self.meeting_startdate.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S") if self.meeting_startdate else "",
            "meeting_finishdate": self.meeting_finishdate.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S") if self.meeting_finishdate else "",
            "signup_startdate": self.signup_startdate.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S") if self.signup_startdate else "",
            "signup_finishdate": self.signup_finishdate.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S") if self.signup_finishdate else "",
            "venue": self.venue or "",
            "organizer": self.organizer or "",
            "co_organizer": self.co_organizer or "",
            "content": self.content or "",
            "adddate": self.adddate.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S"),
            "participant": getMeetingParticipantQuantity(self.id)
        }

    def __str__(self):
        text = "__User__\n"
        for key, value in self.toDict().items():
            text += "{}: {}\n".format(key, value)
        return text

    class Meta:
        db_table = 'meeting_info'


class MeetingLogo(models.Model):
    meeting = models.OneToOneField(Meeting, null=True, blank=True,
                                   on_delete=models.CASCADE, related_name='logo_by_meeting')
    logo = models.TextField(blank=True, null=True, verbose_name='logo')

    class Meta:
        db_table = 'meeting_logo'


class Participant(models.Model):
    meeting = models.ForeignKey(Meeting, null=True, blank=True,
                                on_delete=models.SET_NULL, related_name='participants_by_meeting')
    name = models.CharField(
        max_length=30, blank=True, null=True,  verbose_name='姓名')
    phonenumber = models.CharField(
        max_length=30, verbose_name='手机号')
    signupdate = models.DateTimeField(
        blank=True, null=True, verbose_name='报名时间')
    arrivedate = models.DateTimeField(
        blank=True, null=True, verbose_name='签到时间')

    def toDict(self):
        return {
            "meeting_id": self.meeting_id,
            "signupdate": self.signupdate.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S") if self.signupdate else "",
            "arrivedate": self.arrivedate.astimezone(tz).strftime("%Y-%m-%d %H:%M:%S") if self.arrivedate else "",
            "name": self.name,
            "phonenumber": self.phonenumber,
        }

    def __str__(self):
        text = "__User__\n"
        for key, value in self.toDict().items():
            text += "{}: {}\n".format(key, value)
        return text

    class Meta:
        db_table = 'meeting_participants'
        # unique_together = ('meeting', 'phonenumber',)


def getMeetingParticipantQuantity(meeting_id):
    participants = Participant.objects.filter(
        meeting_id=meeting_id).exclude(signupdate=None)
    signup = participants.exclude(signupdate=None).count()
    arrived = participants.exclude(arrivedate=None).count()
    return {
        "signup": signup,
        "arrived": arrived,
        "unarrived": signup-arrived
    }


def makeMeetingId():
    mid = "m0" + hex(int(time.time()*1000000))[2:] + \
        "-" + str(uuid.uuid4())
    return mid


def createMeeting(name=None, logo=None, meeting_startdate=None, meeting_finishdate=None, signup_startdate=None, signup_finishdate=None, venue=None, organizer=None, co_organizer=None, content=None, meeting_id=None):
    if not name:
        raise RFSException("20001", "无效会议名称")

    logo = logo if logo else None
    venue = venue if venue else None
    organizer = organizer if organizer else None
    co_organizer = co_organizer if co_organizer else None
    content = content if content else None
    meeting_startdate = meeting_startdate if meeting_startdate else None
    meeting_finishdate = meeting_finishdate if meeting_finishdate else None
    signup_startdate = signup_startdate if signup_startdate else None
    signup_finishdate = signup_finishdate if signup_finishdate else None

    # if meeting_id:
    #     meeting = getMeetingByID(meeting.id)
    #     meeting
    #     pass
    meetingDict = {
        "name": name,
        "meeting_startdate": meeting_startdate,  # YYYY-MM-DD HH:MM
        "meeting_finishdate": meeting_finishdate,
        "signup_startdate": signup_startdate,
        "signup_finishdate": signup_finishdate,
        "venue": venue,
        "organizer": organizer,
        "co_organizer": co_organizer,
        "content": content,
    }
    if not meeting_id:
        meetingDict["id"] = makeMeetingId()
        meeting = Meeting.objects.create(**meetingDict)
    else:
        Meeting.objects.filter(id=meeting_id).update(**meetingDict)
        meeting = getMeetingByID(meeting_id)
    # print(type(meeting), meeting)
    updateLogo(meeting.id, logo)
    # meeting = Meeting.objects.update_or_create(
    #     defaults={"id": meeting_id},
    #     id=makeMeetingId(),
    #     name=name,
    #     meeting_startdate=meeting_startdate,  # YYYY-MM-DD HH:MM
    #     meeting_finishdate=meeting_finishdate,
    #     signup_startdate=signup_startdate,
    #     signup_finishdate=signup_finishdate,
    #     venue=venue,
    #     organizer=organizer,
    #     co_organizer=co_organizer,
    #     content=content,
    # )

    return getMeetingByID(meeting.id)


def removeMeeting(meeting_id=None):
    if not Meeting.objects.filter(id=meeting_id).exists():
        return RFSException("20002", "无效会议ID")
    Meeting.objects.filter(id=meeting_id).delete()


def getRecentMeeting():
    if Meeting.objects.exclude(meeting_startdate=None).exclude(meeting_finishdate=None).exists():
        return Meeting.objects.exclude(meeting_startdate=None).exclude(meeting_finishdate=None).order_by("-adddate").all()[0]
    else:
        raise RFSException("20003", "无近期会议")


def updateLogo(meeting_id, logo=None):
    if not meeting_id or not logo:
        return
    MeetingLogo.objects.update_or_create(
        meeting_id=meeting_id,
        logo=logo
    )
    # if MeetingLogo.objects.filter(meeting_id=meeting_id).exists():
    #     MeetingLogo.objects.filter(meeting_id=meeting_id).update(logo=logo)
    # else:
    #     MeetingLogo.objects.create(
    #         meeting_id=meeting_id,
    #         logo=logo
    #     )


def getLogo(meeting_id):
    if MeetingLogo.objects.filter(meeting_id=meeting_id).exists():
        return MeetingLogo.objects.filter(meeting_id=meeting_id).get().logo
    return ""


def getMeetingByID(meeting_id):
    if not meeting_id:
        raise RFSException("20002", "无效会议ID")
    if Meeting.objects.filter(id=meeting_id).exists():
        meeting = Meeting.objects.get(id=meeting_id)
    else:
        raise RFSException("20002", "无效会议ID")
    return meeting


def getAllMeeting():
    return Meeting.objects.all()


# def setMeetingInfo(meeting_id, key, value):
#     meeting = getMeetingById(meeting_id)
#     if key == "name":
#         meeting.name = value
#     elif key == "logo":
#         meeting.logo = value
#     elif key == "meeting_startdate":
#         meeting.meeting_startdate = value
#     elif key == "meeting_finishdate":
#         meeting.meeting_finishdate = value
#     elif key == "signup_startdate":
#         meeting.signup_startdate = value
#     elif key == "signup_finishdate":
#         meeting.signup_finishdate = value
#     elif key == "venue":
#         meeting.venue = value
#     elif key == "organizer":
#         meeting.organizer = value
#     elif key == "co_organizer":
#         meeting.co_organizer = value
#     elif key == "content":
#         meeting.content = value
#     meeting.save()

#     return meeting


ParticipantsDuplicateRemovalSqlString = """
    delete from meeting_participants p 
    where (p.meeting_id,p.phonenumber) in (select meeting_id,phonenumber from meeting_participants group by meeting_id,phonenumber having count(*) > 1) 
    and id not in (select min(id) from meeting_participants group by meeting_id,phonenumber having count(*)>1) 
"""


def addParticipants(meeting_id, participants):
    participants_list = []
    for p in participants:
        name = p["name"]
        phonenumber = p["phonenumber"]
        if not name or not phonenumber:
            continue
        participants_list.append(Participant(meeting_id=meeting_id,
                                             name=str(name),
                                             signupdate=datetime.datetime.now(),
                                             phonenumber=str(phonenumber)
                                             ))
    meeting = getMeetingByID(meeting_id)

    Participant.objects.bulk_create(participants_list)
    cursor = connection.cursor()
    cursor.execute(ParticipantsDuplicateRemovalSqlString)

    # getOrCreateUserByPhonenumber(str(name), str(phonenumber))
    # addMeetingParticipant(meeting_id, str(name), str(phonenumber))


def appendParticipant(meeting_id, name, phonenumber):
    if not name:
        raise RFSException("20031", "无效姓名")
    if not phonenumber:
        raise RFSException("20032", "无效手机号")

    meeting = getMeetingByID(meeting_id)
    if Participant.objects.filter(meeting_id=meeting_id, phonenumber=phonenumber).exists():
        raise RFSException("20033", "手机号重复")
    else:
        participant = Participant.objects.create(
            meeting_id=meeting_id,
            name=name,
            phonenumber=phonenumber,
            signupdate=datetime.datetime.now(),
        )
        return participant


def getMeetingParticipants(meeting_id):
    if not meeting_id:
        raise RFSException("20002", "无效会议ID")
    participants = Participant.objects.filter(
        meeting_id=meeting_id).exclude(signupdate=None)
    # signup = participants.all()
    arrived = participants.exclude(
        arrivedate=None).order_by("arrivedate").all()
    unarrived = participants.filter(arrivedate=None).all()

    return {
        # "signup": [p.toDict() for p in signup],
        "arrived": [p.toDict() for p in arrived],
        "unarrived": [p.toDict() for p in unarrived]
    }


def setParticipantArrived(meeting_id, phonenumber):
    if not phonenumber:
        raise RFSException("30002", "无效手机号")
    if not Participant.objects.filter(meeting_id=meeting_id, phonenumber=phonenumber).exists():
        raise RFSException("30003", "没有查到报名信息，请检查手机号或重试")
    participant = Participant.objects.get(
        meeting_id=meeting_id, phonenumber=phonenumber)
    if participant.arrivedate:
        return participant
        # raise RFSException("30004", "请勿重复签到")
    participant.arrivedate = datetime.datetime.now()
    participant.save()
    return participant


def setParticipantUnarrived(meeting_id,  phonenumber):
    Participant.objects.filter(
        meeting_id=meeting_id, phonenumber=phonenumber).update(arrivedate=None)


def removeMeetingParticipant(meeting_id,  phonenumber):
    Participant.objects.filter(
        meeting_id=meeting_id, phonenumber=phonenumber).delete()
