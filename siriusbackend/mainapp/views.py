from django.shortcuts import render
from django.http.response import JsonResponse

from . import models


def get_all_categories(responce):
    return JsonResponse(models.get_all_subcategories())
