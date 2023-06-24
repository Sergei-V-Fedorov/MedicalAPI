from rest_framework import serializers
from .models import Guide, Element


class GuideSerializer(serializers.ModelSerializer):
    class Meta:
        model = Guide
        fields = ['id', 'code', 'name']


class ElementSerializer(serializers.ModelSerializer):
    class Meta:
        model = Element
        fields = ['code', 'value']