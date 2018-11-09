from django.db import models


class User(models.Model):
    vk_id = models.BigIntegerField(db_index=True, primary_key=True)
    banned = models.BooleanField(default=False)
    spent_time = models.FloatField(default=0.0)

    def to_json(self):
        return {"vk_id": self.vk_id,
                "banned": self.banned,
                "spent_time": self.spent_time}


class Achievement(models.Model):
    name = models.CharField(max_length=256)
    # picture

    def to_json(self):
        return {"name": self.name}


class UserAchievement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    achievement = models.ForeignKey(Achievement, on_delete=models.CASCADE)

    def to_json(self):
        return self.achievement.name


class Category(models.Model):
    name = models.CharField(max_length=256)

    def __str__(self):
        return self.name

    def to_json(self):
        return {"name": self.name}


class Subcategory(models.Model):
    name = models.CharField(max_length=256)
    parent = models.ForeignKey(Category, on_delete=models.CASCADE)

    def __str__(self):
        return self.name

    def to_json(self):
        return {"name": self.name}


class UserInterests(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Subcategory, on_delete=models.CASCADE, null=True)

    def to_json(self):
        if self.subcategory is None:
            return self.category.name

        return self.subcategory.name


class Organizer(models.Model):
    is_person = models.BooleanField()

    full_name = models.CharField(max_length=512)

    contact_data = models.TextField()
    contact_email = models.EmailField()

    description = models.TextField()

    is_verificated = models.BooleanField(default=False)

    # picture

    def to_json(self):
        return {
            "is_person": self.is_person,
            "name": self.full_name,
            "contact_data": self.contact_data,
            "contact_email": self.contact_email,
            "description": self.description,
            "is_verificated": self.is_verificated,
        }


class Event(models.Model):
    SCHOOL_TYPE = 1
    CIRCLE_TYPE = 2
    SINGLE_TIME_TYPE = 4
    OTHER_TYPE = 8
    ONLINE_COURSE_TYPE = 16
    TYPES = [
        (SCHOOL_TYPE, "Выездная школа"),
        (CIRCLE_TYPE, "Кружок"),
        (SINGLE_TIME_TYPE, "Единоразовое мероприятие"),
        (OTHER_TYPE, "Другое"),
        (ONLINE_COURSE_TYPE, "Онлайн-курсы"),
    ]

    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=256, null=False)
    type = models.PositiveSmallIntegerField(choices=TYPES)
    description = models.TextField()

    start_datetime = models.DateTimeField(null=True)
    finish_datetime = models.DateTimeField(null=True)
    week_day = models.PositiveSmallIntegerField()

    place_address = models.TextField()
    place_location_latitude = models.FloatField(null=True)
    place_location_longitude = models.FloatField(null=True)

    repeatable = models.BooleanField()

    contact_email = models.EmailField()
    contact_data = models.TextField()

    organizer = models.ForeignKey(Organizer, on_delete=models.CASCADE)

    def get_type_name(self):
        for x in self.TYPES:
            if self.type == x[0]:
                return x[1]
        raise RuntimeError("Type not found")

    def to_json(self):
        result = {
            "name": self.name,
            "type": self.get_type_name(),
            "description": self.description,
        }

        if self.start_datetime is not None:
            result["start_datetime"] = self.start_datetime
        if self.finish_datetime is not None:
            result["finish_datetime"] = self.finish_datetime
        if self.week_day != 0:
            result["week_day"] = self.week_day
        if self.place_address != "":
            result["place_address"] = self.place_address

        result.update({
            "repeatable": self.repeatable,
            "contact_email": self.contact_email,
            "contact_data": self.contact_data
        })

        result["organizer"] = self.organizer.to_json()

        return result


class UserEvent(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    event = models.ForeignKey(Event, on_delete=models.CASCADE)

    def to_json(self):
        return self.event.to_json()


class EventCategories(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)


class EventSubcategories(models.Model):
    event = models.ForeignKey(Event, on_delete=models.CASCADE)
    subcategory = models.ForeignKey(Category, on_delete=models.CASCADE)
