from datetime import datetime
from django.test import TestCase, tag
from django.urls import reverse
from guides.models import Element, Version, Guide


@tag('refbooks')
class GuideListTest(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.url = '/refbooks/'
        cls.url_name = reverse('medicalapi:refbooks')
        cls.test_date = '2023-02-01'
        init_db()

    def test_url_available_by_name(self):
        """Тест на доступность страницы по name"""
        response = self.client.get(self.url_name)
        self.assertEqual(response.status_code, 200)

    def test_url_exists(self):
        """Тест на доступность страницы по url"""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)

    def test_refbooks_for_current_version(self):
        """Тест на получение списка справочников без указания версии."""
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        returned_guides = response.data['refbooks']
        guides_in_db = Guide.objects.all()
        # выдает одинаковое кол-во справочников
        self.assertEqual(len(returned_guides), len(guides_in_db))

        # проверка правильности выводы справочников
        for i in range(len(returned_guides)):
            with self.subTest(i=i + 1):
                self.assertEqual(returned_guides[i]['id'], guides_in_db[i].id)
                self.assertEqual(returned_guides[i]['code'], guides_in_db[i].code)

    def test_refbooks_with_date(self):
        """Тест на получение списка справочников с указанием даты."""
        url = f"{self.url}?date={self.test_date}"
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        returned_guides = response.data['refbooks']
        guides_in_db = Guide.objects.filter(versions__since_date__lte=self.test_date)
        # выдает одинаковое кол-во справочников
        self.assertEqual(len(returned_guides), len(guides_in_db))

        # проверка правильности выводы справочников
        for i in range(len(returned_guides)):
            with self.subTest(i=i + 1):
                self.assertEqual(returned_guides[i]['id'], guides_in_db[i].id)
                self.assertEqual(returned_guides[i]['code'], guides_in_db[i].code)


def init_db():
    guide_1 = Guide.objects.create(code='1', name='guide_1', description='description_1')
    guide_2 = Guide.objects.create(code='2', name='guide_2', description='description_2')

    version_1 = Version.objects.create(guide_id=guide_1,
                                       version='1.0',
                                       since_date=datetime.strptime('2023-01-20', '%Y-%m-%d'))
    version_2 = Version.objects.create(guide_id=guide_1,
                                       version='1.1',
                                       since_date=datetime.strptime('2023-06-01', '%Y-%m-%d'))
    Version.objects.create(guide_id=guide_2,
                           version='1.0',
                           since_date=datetime.strptime('2023-03-01', '%Y-%m-%d'))

    element_list_1 = [Element(version_id=version_1, code=f'{i}', value=value)
                      for i, value in enumerate(['value_1', 'value_2'])
                      ]

    Element.objects.bulk_create(element_list_1)

    element_list_2 = [Element(version_id=version_2, code=f'{i}', value=value)
                      for i, value in enumerate(['value_1', 'value_2', 'value_3'])
                      ]

    Element.objects.bulk_create(element_list_2)
