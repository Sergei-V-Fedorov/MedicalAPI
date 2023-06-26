"""
Описывает элементы админ-панели.

Содержит модели для отображения экземпляров справочника,
версий справочника и элементов справочника.
"""
from django.contrib import admin
from django.db.models import QuerySet
from .models import Guide, Version, Element

from datetime import date


class VersionInline(admin.TabularInline):
    """Класс для отображения связанных со справочником версий."""

    model = Version
    extra = 0


@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    """Класс для отображения в панели администратора экземпляров справочника."""

    list_display = ['id', 'code', 'name', 'version', 'version_date']
    list_display_links = ['id', 'code', 'name']
    inlines = [VersionInline]

    def version(self, obj: Guide) -> str:
        """Возвращает номер текущей версии справочника."""
        return obj.current_version().version
    version.short_description = 'Текущая версия справочника'

    def version_date(self, obj: Guide) -> date:
        """Возвращает начало действия текущей версии справочника."""
        return obj.current_version().since_date
    version_date.short_description = 'Дата начала'


class ElementInline(admin.TabularInline):
    """Класс для отображения связанных с версией справочника элементов."""

    model = Element
    extra = 0


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    """Класс для отображения в панели администратора экземпляров версий справочника."""

    list_display = ['guide_code', 'guide_title', 'version', 'since_date']
    list_display_links = ['guide_code', 'guide_title', 'version']
    inlines = [ElementInline]

    def get_queryset(self, request) -> QuerySet:
        """Возвращает версии справочника."""
        return Version.objects.select_related('guide_id')

    def guide_code(self, obj: Version) -> str:
        """Возвращает код справочника."""
        return obj.guide_id.code
    guide_code.short_description = 'Код справочника'

    def guide_title(self, obj: Version) -> str:
        """Возвращает заголовок справочника."""
        return obj.guide_id.name
    guide_title.short_description = 'Наименование справочника'


@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    """Класс для отображения в панели администратора экземпляров элементов справочника."""

    list_display = ['code', 'value']
    list_display_links = ['code', 'value']
