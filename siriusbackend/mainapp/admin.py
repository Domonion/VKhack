from django.contrib import admin
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    pass


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    pass


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    pass


@admin.register(UserInterests)
class UserInterestsAdmin(admin.ModelAdmin):
    pass


@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    pass


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    pass


@admin.register(UserEvent)
class UserEventAdmin(admin.ModelAdmin):
    pass


@admin.register(EventCategories)
class EventCategoriesAdmin(admin.ModelAdmin):
    pass


@admin.register(EventSubcategories)
class EventSubcategoriesAdmin(admin.ModelAdmin):
    pass
