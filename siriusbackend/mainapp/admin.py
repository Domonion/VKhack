from django.contrib import admin
from .models import *


@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    readonly_fields=('pk',)
    pass


@admin.register(Achievement)
class AchievementAdmin(admin.ModelAdmin):
    readonly_fields=('pk',)
    pass


@admin.register(UserAchievement)
class UserAchievementAdmin(admin.ModelAdmin):
    readonly_fields=('pk',)
    pass


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    readonly_fields=('pk',)
    pass


@admin.register(Subcategory)
class SubcategoryAdmin(admin.ModelAdmin):
    readonly_fields=('pk',)
    pass


@admin.register(UserInterests)
class UserInterestsAdmin(admin.ModelAdmin):
    readonly_fields=('pk',)
    pass


@admin.register(Organizer)
class OrganizerAdmin(admin.ModelAdmin):
    readonly_fields=('pk',)
    pass


@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    readonly_fields=('pk',)
    pass


@admin.register(UserEvent)
class UserEventAdmin(admin.ModelAdmin):
    readonly_fields=('pk',)
    pass


@admin.register(EventCategories)
class EventCategoriesAdmin(admin.ModelAdmin):
    readonly_fields=('pk',)
    pass


@admin.register(EventSubcategories)
class EventSubcategoriesAdmin(admin.ModelAdmin):
    readonly_fields=('pk',)
    pass
