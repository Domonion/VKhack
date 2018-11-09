from django.db import models

import siriusbackend.users.models as users


class Event(models.Model):
    SCHOOL_TYPE = 1
    CIRCLE_TYPE = 2
    SINGLE_TIME_TYPE = 4
    OTHER_TYPE = 8
    ONLINE_COURSE_TYPE = 16

    owner = models.ForeignKey(users.User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, null=False)
    type = models.PositiveSmallIntegerField(choices=[
        (SCHOOL_TYPE, "Выездная школа"),
        (CIRCLE_TYPE, "Кружок"),
        (SINGLE_TIME_TYPE, "Единоразовое мероприятие"),
        (OTHER_TYPE, "Другое"),
        (ONLINE_COURSE_TYPE, "Онлайн-курсы"),
    ])

    start_datetime = models.DateTimeField(null=True)
    finish_datetime = models.DateTimeField(null=True)
    week_day = models.PositiveSmallIntegerField()

    place_address = models.TextField()
    place_location_latitude = models.FloatField(null=True)
    place_location_longitude = models.FloatField(null=True)

    repeatable = models.BooleanField()

    contact_email = models.EmailField()
    contact_data = models.TextField()

