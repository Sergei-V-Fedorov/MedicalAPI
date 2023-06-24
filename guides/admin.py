from django.contrib import admin
from .models import Guide, Version, Element


class VersionInline(admin.TabularInline):
    model = Version
    extra = 0


@admin.register(Guide)
class GuideAdmin(admin.ModelAdmin):
    list_display = ['id', 'code', 'name', 'version', 'version_date']
    list_display_links = ['id', 'code', 'name']
    inlines = [VersionInline]

    def short_description(self, obj: Guide) -> str:
        if len(obj.description) < 50:
            return obj.description
        return f"{obj.description[:50]}..."
    short_description.short_description = 'Описание справочника'

    def version(self, obj: Guide):
        return obj.current_version().version
    version.short_description = 'Текущая версия справочника'

    def version_date(self, obj: Guide):
        return obj.current_version().since_date
    version_date.short_description = 'Дата начала'


class ElementInline(admin.TabularInline):
    model = Element
    extra = 0


@admin.register(Version)
class VersionAdmin(admin.ModelAdmin):
    list_display = ['guide_code', 'guide_title', 'version', 'since_date']
    list_display_links = ['guide_code', 'guide_title', 'version']
    inlines = [ElementInline]

    def get_queryset(self, request):
        return Version.objects.select_related('guide_id')

    def guide_code(self, obj: Version):
        return obj.guide_id.code
    guide_code.short_description = 'Код справочника'

    def guide_title(self, obj: Version):
        return obj.guide_id.name
    guide_title.short_description = 'Наименование справочника'


@admin.register(Element)
class ElementAdmin(admin.ModelAdmin):
    list_display = ['code', 'value']
    list_display_links = ['code', 'value']
