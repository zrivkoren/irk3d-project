from django.contrib import admin
from django.contrib.auth.models import Group
from adminsortable2.admin import SortableAdminMixin
from .models import Tour, Tag, Scene, Feedback, Service, Client, FAQ


class SceneInline(admin.StackedInline):
    model = Scene
    extra = 3


@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug']


@admin.register(Tour)
class TourAdmin(admin.ModelAdmin):
    list_display = ['name', 'slug', 'get_admin_tags', 'created']
    inlines = [SceneInline]
    save_on_top = True


@admin.register(Feedback)
class FeedbackAdmin(admin.ModelAdmin):
    list_display = ['author_position_company', 'text']


@admin.register(Service)
class ServiceAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['order', 'name', 'text']


@admin.register(Client)
class ClientAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['name']


@admin.register(FAQ)
class FAQAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['number', 'question', 'answer']


admin.site.unregister(Group)
