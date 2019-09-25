from django.urls import path, include
from . import views


urlpatterns = [
    path("test", views.test),
    path("recent", views.recentmeeting),
    path("create", views.createmeeting),
    path("update", views.createmeeting),
    path("remove", views.removemeeting),
    path("info", views.meetinginfo),
    path("all", views.allmeeting),
    path("participant", views.participantinfo),
    path("participant/add", views.addparticipants),
    path("participant/arrived", views.setarrived),
    path("participant/unarrived", views.setunarrived),
    path("participant/signin", views.participantarrive),
    path("participant/append", views.appendparticipant),
    path("participant/remove", views.removeparticipant),


]
