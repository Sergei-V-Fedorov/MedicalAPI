"""
Описывает сериализаторы моделей приложения.

Содержит сериализаторы для модели для справочника
и элементов справочника.
"""
from rest_framework import serializers
from .models import Guide, Element


class GuideSerializer(serializers.ModelSerializer):
    """Сериализатор модели справочника."""

    class Meta:
        model = Guide
        fields = ['id', 'code', 'name']


class ElementSerializer(serializers.ModelSerializer):
    """Сериализатор модели элементов справочника."""

    class Meta:
        model = Element
        fields = ['code', 'value']
