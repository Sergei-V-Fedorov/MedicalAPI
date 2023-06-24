from django.db import models


class Guide(models.Model):
    code = models.CharField(max_length=100, unique=True, verbose_name='код справочника')
    name = models.CharField(max_length=300, verbose_name='наименование справочника')
    description = models.TextField(verbose_name='описание справочника', blank=True)

    class Meta:
        ordering = ['pk']
        verbose_name = "справочник"
        verbose_name_plural = "справочники"

    # @property
    # def short_description(self):
    #     if len(self.description) < 50:
    #         return self.description
    #     return f"{self.description[:50]}..."

    def current_version(self):
        return Version.objects.select_related('guide_id').filter(guide_id=self.pk).\
            order_by('-since_date').first()

    def __str__(self):
        return f"Справочник({self.code}: {self.name[:15]}...)"


class Version(models.Model):
    guide_id = models.ForeignKey(Guide, on_delete=models.CASCADE, related_name='versions',
                                 verbose_name='справочник')
    version = models.CharField(max_length=50, verbose_name='версия справочника')
    since_date = models.DateField(blank=True, verbose_name='дата начала действия версия')

    class Meta:
        ordering = ['pk']
        unique_together = [
            # Для одного справочника - одна уникальная версия
            ["guide_id", "version"],
            # Для одного справочника - только одна версия начинается с даты since_date
            ["guide_id", "since_date"],
        ]
        verbose_name = "версия справочник"
        verbose_name_plural = "версии справочников"

    def __str__(self):
        return f"Версия({self.version})"


class Element(models.Model):
    version_id = models.ForeignKey(Version, on_delete=models.CASCADE, related_name='elements',
                                   verbose_name='версия')
    code = models.CharField(max_length=100, verbose_name='код элемента')
    value = models.CharField(max_length=300, verbose_name='значение элемента')

    class Meta:
        ordering = ['pk']
        # Для одной версии - один уникальный код элемента
        unique_together = ["version_id", "code"]
        verbose_name = "элемент справочника"
        verbose_name_plural = "элементы справочников"

    def __str__(self):
        return f"Элемент(код={self.code})"
