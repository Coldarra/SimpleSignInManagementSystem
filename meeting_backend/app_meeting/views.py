import json

from decorator import *
from django.shortcuts import render

from .models import *


@service
def test(param):
    return pack(interface_id=0, data={"ok": "ok"})


@admin
@service
def recentmeeting(param):
    interface_id = "2000"
    try:
        meeting = getRecentMeeting()
    except RFSException as e:
        return pack(interface_id, e.ret, e.msg)
    except Exception as e:
        return pack(interface_id, interface_id+'0', str(e))
    resp = {"meeting": meeting.toDict()}
    return pack(interface_id=interface_id, data=resp)


@admin
@service
def createmeeting(param):
    interface_id = "2001"

    name = param.get('name', None) or param.get('username', None)
    logo = param.get('logo', None)
    meeting_startdate = param.get('meeting_startdate', None)
    meeting_finishdate = param.get('meeting_finishdate', None)
    signup_startdate = param.get('signup_startdate', None)
    signup_finishdate = param.get('signup_finishdate', None)
    venue = param.get('venue', None)
    organizer = param.get('organizer', None)
    co_organizer = param.get('co_organizer', None)
    content = param.get('content', None)
    meeting_id = param.get('meeting_id', None)

    # meeting = createMeeting(name, logo, meeting_startdate, meeting_finishdate,
    #                         signup_startdate, signup_finishdate, venue, organizer, co_organizer, content, meeting_id)

    try:
        meeting = createMeeting(name, logo, meeting_startdate, meeting_finishdate,
                                signup_startdate, signup_finishdate, venue, organizer, co_organizer, content, meeting_id)
    except RFSException as e:
        return pack(interface_id, e.ret, e.msg)
    except Exception as e:
        return pack(interface_id, interface_id+'0', str(e))
    resp = {"meeting": meeting.toDict()}

    return pack(interface_id=interface_id, data=resp)


@admin
@service
def removemeeting(param):
    interface_id = "2002"
    meeting_id = param.get("meeting_id", None)
    try:
        removeMeeting(meeting_id)
    except RFSException as e:
        return pack(interface_id, e.ret, e.msg)
    except Exception as e:
        return pack(interface_id, interface_id+'0', str(e))

    resp = {"meeting_id": meeting_id}
    return pack(interface_id=interface_id, data=resp)


@service
def meetinginfo(param):
    interface_id = "2005"

    meeting_id = param.get("meeting_id", None)
    user_id = param["user"]['userid']
    level = param["user"]['level']

    try:
        meeting = getMeetingByID(meeting_id)
    except RFSException as e:
        return pack(interface_id, e.ret, e.msg)
    except Exception as e:
        return pack(interface_id, interface_id+'0', str(e))

    resp = {"meeting": meeting.toDict()}
    return pack(interface_id=interface_id, data=resp)


@admin
@service
def allmeeting(param):
    interface_id = "2006"

    meeting_id = param.get("meeting_id", None)

    try:
        meetings = getAllMeeting()
    except RFSException as e:
        return pack(interface_id, e.ret, e.msg)
    except Exception as e:
        return pack(interface_id, interface_id+'0', str(e))

    resp = {"meetings": [m.toDict() for m in meetings]}
    return pack(interface_id=interface_id, data=resp)


@admin
@service
def participantinfo(param):
    interface_id = "3005"

    meeting_id = param.get("meeting_id", None)

    try:
        participants = getMeetingParticipants(meeting_id)
    except RFSException as e:
        return pack(interface_id, e.ret, e.msg)
    except Exception as e:
        return pack(interface_id, interface_id+'0', str(e))

    resp = {"participants": participants}
    return pack(interface_id=interface_id, data=resp)


@admin
@service
def setarrived(param):
    interface_id = "3101"
    meeting_id = param.get("meeting_id", None)
    phonenumber = param.get("phonenumber", None)
    try:
        setParticipantArrived(meeting_id, phonenumber)
        participants = getMeetingParticipants(meeting_id)
    except RFSException as e:
        return pack(interface_id, e.ret, e.msg)
    except Exception as e:
        return pack(interface_id, interface_id+'0', str(e))
    resp = {"participants": participants}
    return pack(interface_id=interface_id, data=resp)


@admin
@service
def setunarrived(param):
    interface_id = "3102"
    meeting_id = param.get("meeting_id", None)
    phonenumber = param.get("phonenumber", None)
    try:
        setParticipantUnarrived(meeting_id, phonenumber)
        participants = getMeetingParticipants(meeting_id)
    except RFSException as e:
        return pack(interface_id, e.ret, e.msg)
    except Exception as e:
        return pack(interface_id, interface_id+'0', str(e))
    resp = {"participants": participants}
    return pack(interface_id=interface_id, data=resp)


@admin
@service
def removeparticipant(param):
    interface_id = "3103"
    meeting_id = param.get("meeting_id", None)
    phonenumber = param.get("phonenumber", None)
    try:
        removeMeetingParticipant(meeting_id, phonenumber)
        participants = getMeetingParticipants(meeting_id)
    except RFSException as e:
        return pack(interface_id, e.ret, e.msg)
    except Exception as e:
        return pack(interface_id, interface_id+'0', str(e))
    resp = {"participants": participants}
    return pack(interface_id=interface_id, data=resp)


@admin
@service
def addparticipants(param):  # 添加多个
    interface_id = "3121"
    meeting_id = param.get("meeting_id", None)
    participants = param.get("participants", None)
    try:
        participants = json.loads(participants)
        for index, p in enumerate(participants):
            participants[index]["name"] = p.get('姓名', None)
            participants[index]["phonenumber"] = p.get("手机号", None)
        addParticipants(meeting_id, participants)
        participants = getMeetingParticipants(meeting_id)
    except RFSException as e:
        return pack(interface_id, e.ret, e.msg)
    except Exception as e:
        return pack(interface_id, interface_id+'0', str(e))
    resp = {"participants": participants}
    return pack(interface_id=interface_id, data=resp)


@admin
@service
def appendparticipant(param):  # 添加单个
    interface_id = "3122"
    meeting_id = param.get("meeting_id", None)
    name = param.get("name", None)
    phonenumber = param.get("phonenumber", None)
    try:
        appendParticipant(meeting_id, name, phonenumber)
        participants = getMeetingParticipants(meeting_id)
    except RFSException as e:
        return pack(interface_id, e.ret, e.msg)
    except Exception as e:
        return pack(interface_id, interface_id+'0', str(e))
    resp = {"participants": participants}
    return pack(interface_id=interface_id, data=resp)


@service
def participantarrive(param):
    interface_id = "3201"
    meeting_id = param.get("meeting_id", None)
    phonenumber = param.get("phonenumber", None)

    try:
        meeting = getMeetingByID(meeting_id)
        participant = setParticipantArrived(meeting_id, phonenumber)
    except RFSException as e:
        return pack(interface_id, e.ret, e.msg)
    except Exception as e:
        return pack(interface_id, interface_id+'0', str(e))
    resp = {
        "participant": participant.toDict(),
        # "meeting": meeting.toDict()
    }
    return pack(interface_id=interface_id, data=resp)
