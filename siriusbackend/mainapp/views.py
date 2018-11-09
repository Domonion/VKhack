from django.shortcuts import render
from django.http.response import JsonResponse

from . import models


def get_all_categories(responce):
    result = dict()
    for item in list(models.Subcategory.objects.all()):
        if item.parent.name not in result:
            result[item.parent.name] = list()
        result[item.parent.name].append(item.name)
    return JsonResponse(result)
