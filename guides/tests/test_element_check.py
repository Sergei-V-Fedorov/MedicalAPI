from django.shortcuts import get_object_or_404
from django.test import TestCase, tag
from django.urls import reverse
from guides.models import Element, Version, Guide
from .test_guidelist import init_db


@tag('check')
class GuideElementCheckOutTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        init_db()
        # код справочника с несколькими версиями
        code = '1'
        cls.guide = get_object_or_404(Guide, code=code)
        cls.current_version = Version.objects.filter(guide_id=cls.guide).order_by('-since_date').first()
        cls.given_version = '1.0'
        cls.pk = cls.guide.pk
        cls.url = f'/refbooks/{cls.pk}/check_element'
        cls.url_name = reverse('medicalapi:check', args=[cls.pk])

    def test_url_available_by_name(self):
        """Тест на доступность страницы по name."""
        response = self.client.get(self.url_name)
        self.assertEqual(response.status_code, 200)

    def test_url_exists(self):
        """Тест на доступность страницы по url."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_element_exists_in_current_guide_version(self):
        """Тест на проверку существования элемента с заданным кодом и значением в текущей версии справочника."""
        elements = Element.objects.filter(version_id=self.current_version)
        code = elements[0].code
        value = elements[0].value
        url = f"{self.url}?code={code}&value={value}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        result = response.data['Element']
        self.assertEqual(result, 'Существует')

    def test_element_doesnt_exist_in_current_guide_version(self):
        """Тест на проверку отсутствия элемента с заданным кодом и значением в текущей версии справочника."""
        code = 'absent_code'
        value = 'absent_value'
        url = f"{self.url}?code={code}&value={value}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        result = response.data['Element']
        self.assertEqual(result, 'Не существует')

    def test_element_exists_in_given_guide_version(self):
        """Тест на проверку существования элемента с заданным кодом и значением в заданной версии справочника."""
        version = get_object_or_404(Version, guide_id=self.guide, version=self.given_version)
        elements = Element.objects.filter(version_id=version)
        code = elements[0].code
        value = elements[0].value
        url = f"{self.url}?code={code}&value={value}&version={self.given_version}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        result = response.data['Element']
        self.assertEqual(result, 'Существует')

    def test_element_doesnt_exist_in_given_guide_version(self):
        """Тест на проверку отсутствия элемента с заданным кодом и значением в заданной версии справочника."""
        code = 'absent_code'
        value = 'absent_value'
        url = f"{self.url}?code={code}&value={value}&version={self.given_version}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        result = response.data['Element']
        self.assertEqual(result, 'Не существует')
