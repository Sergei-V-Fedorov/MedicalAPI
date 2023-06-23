from django.db import models


class Guide(models.Model):
    code = models.CharField(max_length=100, unique=True, verbose_name='код справочника')
    title = models.CharField(max_length=300, verbose_name='наименование справочника')
    description = models.TextField(verbose_name='описание справочника', blank=True)

    class Meta:
        ordering = ['pk']


class Version(models.Model):
    guide_id = models.ForeignKey(Guide, on_delete=models.CASCADE, related_name='versions',
                                 verbose_name='идентификатор справочника')
    version = models.CharField(max_length=50, verbose_name='версия справочника')
    since_date = models.DateField(blank=True)

    class Meta:
        ordering = ['pk']
        unique_together = [
            # Для одного справочника - одна уникальная версия
            ["guide_id", "version"],
            # Для одного справочника - только одна версия начинается с даты since_date
            ["guide_id", "since_date"],
        ]


class Element(models.Model):
    version_id = models.ForeignKey(Version, on_delete=models.CASCADE, related_name='elements')
    code = models.CharField(max_length=100, verbose_name='код элемента')
    value = models.CharField(max_length=300, verbose_name='значение элемента')

    class Meta:
        ordering = ['pk']
        # Для одной версии - один уникальный код элемента
        unique_together = ["version_id", "code"]


