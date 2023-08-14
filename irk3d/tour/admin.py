from django.contrib import admin
from django.contrib.auth.models import Group
from .models import Tour, Tag, Scene, Feedback

admin.site.unregister(Group)


class SceneInline(admin.StackedInline):
    model = Scene
    extra = 3


@admin.register(Scene)
class SceneAdmin(admin.ModelAdmin):
    list_display = ['name', 'tour']
    list_filter = ['tour']


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
