from rest_framework import serializers
from .models import Tour


class TourListSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tour
        fields = ['name', 'slug', "created", "preview_image", "text", "vt_url", "tags"]
