"""
Содержит тесты для представления GuideElementList.

Проверка функционала представления GuideElementList.
"""
from django.shortcuts import get_object_or_404
from django.test import TestCase, tag
from django.urls import reverse
from guides.models import Element, Version, Guide
from .test_guidelist import init_db


@tag('elements')
class GuideElementListTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        init_db()
        # код справочника с несколькими версиями
        code = '1'
        cls.guide = get_object_or_404(Guide, code=code)
        cls.current_version = Version.objects.filter(guide_id=cls.guide).order_by('-since_date').first()
        cls.given_version = '1.0'
        cls.pk = cls.guide.pk
        cls.url = f'/refbooks/{cls.pk}/elements'
        cls.url_name = reverse('medicalapi:elements', args=[cls.pk])

    def test_url_available_by_name(self):
        """Тест на доступность страницы по name."""
        response = self.client.get(self.url_name)
        self.assertEqual(response.status_code, 200)

    def test_url_exists(self):
        """Тест на доступность страницы по url."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_element_for_current_guide_version(self):
        """Тест на получение элементов справочника текущей версии."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        returned_elements = response.data['elements']
        elements_in_db = Element.objects.filter(version_id=self.current_version)
        # выдает одинаковое кол-во элементов
        self.assertEqual(len(returned_elements), len(elements_in_db))

        # проверка правильности вывода элементов
        for i in range(len(returned_elements)):
            with self.subTest(i=i + 1):
                self.assertEqual(returned_elements[i]['code'], elements_in_db[i].code)
                self.assertEqual(returned_elements[i]['value'], elements_in_db[i].value)

    def test_element_for_giver_guide_version(self):
        """Тест на получение элементов справочника заданной версии."""
        url = f"{self.url}?version={self.given_version}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        returned_elements = response.data['elements']
        version = get_object_or_404(Version, guide_id=self.guide, version=self.given_version)
        elements_in_db = Element.objects.filter(version_id=version)
        # # выдает одинаковое кол-во элементов
        self.assertEqual(len(returned_elements), len(elements_in_db))

        # проверка правильности вывода элементов
        for i in range(len(returned_elements)):
            with self.subTest(i=i + 1):
                self.assertEqual(returned_elements[i]['code'], elements_in_db[i].code)
                self.assertEqual(returned_elements[i]['value'], elements_in_db[i].value)
