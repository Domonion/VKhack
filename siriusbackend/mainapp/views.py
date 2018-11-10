import json
import uuid

import vk
import dateutil.parser as datetimeparser

from django.shortcuts import render
from django.http.response import JsonResponse
import django.core.exceptions as err
from django.views.decorators.csrf import csrf_exempt

from . import models


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

    events = user.userinterests_set.all()
    result = []
    for event in events:
        result.append(event.to_json())
    return JsonResponse(result)


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

    events = data["events"]
    for event in events:
        user_event = models.UserEvent(user=user, event_id=event)
        user_event.save()

    return JsonResponse("ok", safe=False)


@csrf_exempt
def add_event(request):
    data = json.loads(request.body)
    event = models.Event(owner=models.User.objects.get(id=int(data["id"])),
                         name=data["name"],
                         type=int(data["type"]),
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
    else:
        return JsonResponse({"error": "incorrect event type"})

    event.save()
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

#
# def get_events(request):
#     query_string = request.GET.get("q")
#     return []


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