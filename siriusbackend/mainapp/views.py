import vk

from django.shortcuts import render
from django.http.response import JsonResponse
import django.core.exceptions as err

from . import models


def _get_api(token):
    session = vk.Session(access_token=token)
    api = vk.API(session, v="5.87")
    return api


def get_all_categories(responce):
    result = dict()
    for item in list(models.Subcategory.objects.all()):
        if item.parent.name not in result:
            result[item.parent.name] = list()
        result[item.parent.name].append(item.name)
    return JsonResponse(result)


def get_user_info(request):
    token = request.GET.get("token", None)
    if token is None:
        return JsonResponse({"error": "token is None"})

    api = _get_api(token)
    user_vk = api.users.get()
    user_id = int(user_vk[0]["id"])

    try:
        user = models.User.objects.get(id=user_id)
    except err.ObjectDoesNotExist:
        return JsonResponse({"error": "user does not exist"})

    user_json = user.to_json()

    user_json["first_name"] = api.users.get()[0]["first_name"]
    user_json["last_name"] = api.users.get()[0]["last_name"]

    return JsonResponse(user_json)


def get_user_interests(request):
    token = request.GET.get("token", None)
    if token is None:
        return JsonResponse({"error": "token is None"})

    api = _get_api(token)
    user_vk = api.users.get()
    user_id = int(user_vk[0]["id"])

    try:
        user = models.User.objects.get(id=user_id)
    except err.ObjectDoesNotExist:
        return JsonResponse({"error": "user does not exist"})

    interests = user.userinterests_set.all()
    result = []
    for interest in interests:
        result.append(interest.to_json())
    return JsonResponse(result)
