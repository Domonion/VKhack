import os
import django

if __name__ == "__main__":
    print("Started preparing instance of Django for worker")
    os.environ["DJANGO_SETTINGS_MODULE"] = "siriusbackend.settings"
    django.setup()

    from mainapp import models

    while True:
        event_name = input("event_name")
        owner_id = 58321509
        event_type = models.Event.ONLINE_COURSE_TYPE
        description = input("description")
        href = input("href")

        event = models.Event(owner=models.User.objects.get(vk_id=owner_id),
                             name=event_name,33333333333333333333333333333333333333333333333333333333333333333333
                             type=event_type,
                             description=description,
                             organizer_id=3,
                             contact_data=href)
        event.save()

        keks = input("tags/subtags,...")
        for x in keks.split(","):
            y = x.split("/")
            tag = models.Category.objects.get(name=y[0])
            tag.save()

            if models.EventCategories.objects.filter(event=event, category=tag).count() == 0:
                models.EventCategories(event=event, category=tag).save()

            if len(y) > 1:
                subtag = models.Subcategory.objects.get(name=y[1], parent=tag)
                subtag.save()

                models.EventSubcategories(event=event, subcategory=subtag).save()

        print("ok")