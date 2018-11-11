import json
import uuid

import vk
import dateutil.parser as datetimeparser

import datetime

from django.shortcuts import render
from django.http.response import JsonResponse
import django.core.exceptions as err
from django.views.decorators.csrf import csrf_exempt

from . import models

import sys
import os

sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from recomendations.lib.event import *


def _get_api(token="ce3641fdce3641fdce3641fd4ece6ff12dcce36ce3641fd95d3ba5bcc826e6a2fcb58b5"):
    session = vk.Session(access_token=token)
    api = vk.API(session, v="5.87")
    return api


def get_all_categories(responce):
    return JsonResponse(models.get_all_subcategories())


def get_user_info(request):
    """
        if error
    """
    # token = request.GET.get("token", None)
    # if token is None:
    #     return JsonResponse({"error": "token is None"})

    api = _get_api()
    # user_vk = api.users.get()
    # user_id = int(user_vk[0]["id"])
    user_id = int(request.GET.get("id"))

    try:
        user = models.User.objects.get(vk_id=user_id)
    except err.ObjectDoesNotExist:
        return JsonResponse({"error": "user does not exist"})

    user_json = user.to_json()

    api_response = api.users.get(user_ids=[user_id], fields=["photo_200"])

    user_json["first_name"] = api_response[0]["first_name"]
    user_json["last_name"] = api_response[0]["last_name"]
    user_json["picture"] = api_response[0]["photo_200"]

    user_json["interests"] = []
    for interest in user.userinterests_set.all():
        user_json["interests"].append(interest.to_json())

    user_json["achievements"] = []
    for achievement in user.userachievement_set.all():
        user_json["achievements"].append(achievement.to_json())

    user_json["rank"] = 0

    return JsonResponse(user_json)


def get_user_interests(request):
    # token = request.GET.get("token", None)
    # if token is None:
    #     return JsonResponse({"error": "token is None"})

    api = _get_api()
    # user_vk = api.users.get()
    # user_id = int(user_vk[0]["id"])
    user_id = int(request.GET.get("id"))

    try:
        user = models.User.objects.get(id=user_id)
    except err.ObjectDoesNotExist:
        return JsonResponse({"error": "user does not exist"})

    interests = user.userinterests_set.all()
    result = []
    for interest in interests:
        result.append(interest.to_json())
    return JsonResponse(result)


def get_user_events(request):
    # token = request.GET.get("token", None)
    # if token is None:
    #     return JsonResponse({"error": "token is None"})

    api = _get_api()
    # user_vk = api.users.get()
    # user_id = int(user_vk[0]["id"])
    user_id = int(request.GET.get("vk_id"))

    try:
        user = models.User.objects.get(vk_id=user_id)
    except err.ObjectDoesNotExist:
        return JsonResponse({"error": "user does not exist"})

    events = models.UserEvent.objects.filter(user=user).all()
    result = []
    for event in events:
        result.append(event.to_json())
    return JsonResponse(result, safe=False)


@csrf_exempt
def register_user(request):
    data = json.loads(request.body)
    user = models.User(vk_id=int(data["vk_id"]), subcategories_file=str(uuid.uuid4()))
    user.save()

    interests = data["interests"]
    for interest in interests:
        if "/" in interest:
            x = interest.split("/")
            category = models.Category.objects.get(name=x[0])
            subcategory = models.Subcategory.objects.get(name=x[1])
        else:
            category = models.Category.objects.get(name=interest)
            subcategory = None

        user_interest = models.UserInterests(user=user, category=category, subcategory=subcategory)
        user_interest.save()

    events = data.get("events")
    if events is not None:
        for event in events:
            user_event = models.UserEvent(user=user, event_id=event)
            user_event.save()

    return JsonResponse("ok", safe=False)


@csrf_exempt
def add_event(request):
    data = json.loads(request.body)

    kek = data["type"]

    foo = -1
    for i, lol in enumerate(models.Event.TYPES):
        if lol[1] == kek:
            foo = 2 ** i
            break

    if foo == -1:
        return JsonResponse({"error": "вы проиграли"})

    event = models.Event(owner=models.User.objects.get(id=int(data["id"])),
                         name=data["name"],
                         type=foo,
                         description=data["description"])

    if event.type == models.Event.SCHOOL_TYPE:
        event.start_datetime = datetimeparser.parse(data["start_datetime"])
        event.finish_datetime = datetimeparser.parse(data["finish_datetime"])
        event.contact_email = data["contact_email"]
        event.contact_data = data.get("contact_data")
        event.place_address = data["place_address"]
        event.organizer = models.Organizer.objects.get(full_name=data["organizer"])

    elif event.type == models.Event.CIRCLE_TYPE:
        event.week_day = int(data["week_day"])
        event.start_datetime = datetimeparser.parse(data["start_datetime"])
        event.finish_datetime = datetimeparser.parse(data["finish_datetime"])
        if data.get("contact_email") is not None:
            event.contact_email = data.get("contact_email")
        if data.get("contact_data") is not None:
            event.contact_data = data.get("contact_data")
        event.repeatable = True
        if data.get("place_address") is not None:
            event.place_address = data.get("place_address")
        if data.get("organizer") is not None:
            event.organizer = models.Organizer.objects.get(full_name=data.get("organizer"))

    elif event.type == models.Event.SINGLE_TIME_TYPE:
        event.place_address = data["place_address"]
        event.start_datetime = datetimeparser.parse(data["start_datetime"])
        event.finish_datetime = datetimeparser.parse(data["finish_datetime"])
        if data.get("organizer") is not None:
            event.organizer = models.Organizer.objects.get(full_name=data.get("organizer"))
        if data.get("contact_email") is not None:
            event.contact_email = data.get("contact_email")
        if data.get("contact_data") is not None:
            event.contact_data = data.get("contact_data")

    elif event.type == models.Event.OTHER_TYPE:
        event.start_datetime = datetimeparser.parse(data.get("start_datetime"))
        event.finish_datetime = datetimeparser.parse(data.get("finish_datetime"))
        event.week_day = data.get("week_day")
        event.place_address = data.get("place_address")
        event.repeatable = data.get("repeatable")
        event.contact_email = data.get("contact_email")
        event.contact_data = data.get("contact_data")
        event.organizer = models.Organizer.objects.get(full_name=data.get("organizer"))
    elif event.type == models.Event.OTHER_TYPE:
        return JsonResponse({"error": "users not allowed to add online-courses"})
    else:
        return JsonResponse({"error": "incorrect event type"})

    event.save()
    event_handler.add_event_add_query(event)

    return JsonResponse({"id": event.id})


def get_organizer_info(request):
    full_name = request.GET.get("full_name")
    if full_name is None:
        return JsonResponse({"error": "No such organizer"})
    organizer = models.Organizer.objects.get(full_name=full_name)
    result = organizer.to_json()
    result["events"] = list([x.to_json(False) for x in models.Event.objects.filter(organizer=organizer).all()])
    return JsonResponse(result)


def get_event_info(request):
    event_id = request.GET.get("id")
    if event_id is None:
        return JsonResponse({"error": "id must be specified"})

    event = models.Event.objects.get(id=int(event_id))
    return JsonResponse(event.to_json())


def get_events(request):
    by_location = request.GET.get("by_location", False)
    user_id = request.GET.get("user_id")
    if user_id is None:
        return JsonResponse({"error": "kek"})

    events = event_handler.get_all_sorted_events(user_id)
    return JsonResponse([event.to_json() for event in events], safe=False)


@csrf_exempt
def add_review(request):
    data = json.loads(request.body)

    user_vk_id = data.get("user_id")
    event_id = data.get("event_id")
    mark = data.get("mark")
    text = data.get("text", "")

    if user_vk_id is None or event_id is None or mark is None:
        return JsonResponse({"error": "user_vk_id, event_id and mark must be specified"})

    review = models.Review(user=models.User.objects.get(vk_id=user_vk_id),
                           event_id=event_id,
                           mark=int(mark),
                           text=text)
    review.save()
    return JsonResponse({"id": review.id})


def get_event_by_id(request):
    vk_id = request.GET.get("user_id")
    event_id = request.GET.get("event_id")

    if vk_id is None or event_id is None:
        return JsonResponse({"error": "vk_id and event_id must be specified"})

    try:
        user_event = models.UserEvent.objects.get(user_id=vk_id, event_id=event_id)
    except err.ObjectDoesNotExist:
        return JsonResponse(models.Event.objects.get(id=event_id).to_json())

    return JsonResponse(user_event.to_json())


def subscribe(request):
    vk_id = request.GET.get("user_id")
    event_id = request.GET.get("event_id")

    if vk_id is None or event_id is None:
        return JsonResponse({"error": "vk_id and event_id must be specified"})

    try:
        user_event = models.UserEvent.objects.get(user=models.User.objects.get(vk_id=vk_id), event_id=event_id)
    except err.ObjectDoesNotExist:
        kek = models.UserEvent(user=models.User.objects.get(vk_id=vk_id), event_id=event_id)
        kek.save()
        event_handler.subscribe(user=models.User.objects.get(vk_id=vk_id),
                                event=models.Event.objects.get(id=event_id))
        return JsonResponse(kek.to_json())

    event_handler.unsubscribe(user=models.User.objects.get(vk_id=vk_id),
                              event=models.Event.objects.get(id=event_id))
    user_event.delete()
    return JsonResponse(models.Event.objects.get(id=event_id).to_json())


def rating(request):
    return JsonResponse(models.User.objects.get(vk_id=58321509).to_json())
