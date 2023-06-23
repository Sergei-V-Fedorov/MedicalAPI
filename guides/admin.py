from django.contrib import admin
from .models import Guide, Version, Element


@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = '__all__'


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = '__all__'


@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    list_display = '__all__'
