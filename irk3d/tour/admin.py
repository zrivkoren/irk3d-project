from django.contrib import admin
from django.contrib.auth.models import Group
from adminsortable2.admin import SortableAdminMixin
from .models import Tour, Tag, Scene, Feedback, Service, Client, FAQ, Irk3dSettings


class SceneInline(admin.StackedInline):
    model = Scene
    extra = 3


@admin.register(Tag)
class TagAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['name', 'order', 'slug', 'is_in_portfolio']


@admin.register(Tour)
class TourAdmin(SortableAdminMixin, admin.ModelAdmin):
    list_display = ['name', 'order', 'slug', 'get_admin_tags', 'created']
    inlines = [SceneInline]
    save_on_top = True
    list_filter = ['tags']


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


@admin.register(Irk3dSettings)
class Irk3dSettingsAdmin(admin.ModelAdmin):
    list_display = ['price_low', 'price_medium', 'price_high', 'vt_count', 'panorama_count']


admin.site.unregister(Group)
