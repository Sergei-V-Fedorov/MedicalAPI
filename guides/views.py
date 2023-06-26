"""
Содержит представления для отображения информации о медицинских справочниках.

Содержит представления для отображения списков справочников,
элементов заданного справочника,
валидации элементов справочника.
"""
from django.db.models import QuerySet
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Guide, Element, Version
from .serializers import GuideSerializer, ElementSerializer

from drf_spectacular.utils import extend_schema, OpenApiParameter, OpenApiExample, inline_serializer


@extend_schema(
        summary="Получение списка справочников",
        description="Выводит список **справочников** (+ актуальных на указанную дату)",
        responses={200: inline_serializer(
            name='get_refbooks',
            fields={"refbooks": GuideSerializer(many=True)}
        )},
        parameters=[
            OpenApiParameter(
                name='date',
                location=OpenApiParameter.QUERY,
                description='Дата начала действия версии справочника в формате ГГГГ-ММ-ДД.',
                required=False,
                type=str
            ),
        ]
)
class GuidesList(APIView):
    """Получение списка справочников."""

    def get_queryset(self) -> QuerySet:
        """Получает список справочников."""
        requested_date = self.request.query_params.get('date')
        if requested_date:
            queryset = Guide.objects.filter(versions__since_date__lte=requested_date)
        else:
            queryset = Guide.objects.all()
        return queryset

    def get(self, request, *args, **kwargs) -> Response:
        """Выводит список справочников."""
        queryset = self.get_queryset()
        serializer = GuideSerializer(queryset, many=True)
        json_response = {"refbooks": serializer.data}
        return Response(json_response)


@extend_schema(
        summary="Получение элементов заданного справочника",
        description="Выводит список **элементов** заданного справочника",
        responses={200: inline_serializer(
            name='get_elements',
            fields={"elements": ElementSerializer(many=True)}
        )},
        parameters=[
            OpenApiParameter(
                name='version',
                location=OpenApiParameter.QUERY,
                description='Версия справочника. Если не указана, то текущая версия.',
                required=False,
                type=str
            ),
        ]
)
class GuideElementList(APIView):
    """Получение элементов заданного справочника."""

    def get_queryset(self) -> QuerySet:
        """Получает список элементов справочника."""
        guide_id = self.kwargs.get('pk')
        version = self.request.query_params.get('version')
        guide = get_object_or_404(Guide, pk=guide_id)
        if version is None:
            version_id = guide.current_version().pk
        else:
            version_id = Version.objects.filter(guide_id=guide_id, version=version).first()

        queryset = Element.objects.filter(version_id=version_id).all()
        return queryset

    def get(self, request, *args, **kwargs) -> Response:
        """Выводит список элементов справочника."""
        queryset = self.get_queryset()
        serializer = ElementSerializer(queryset, many=True)
        json_response = {"elements": serializer.data}
        return Response(json_response)


@extend_schema(
        summary="Валидация элементов",
        description="Проверка, что элемент с данным **code** и **value** присутствует в указанной версии справочника",
        responses={200: 'Существует'},
        parameters=[
            OpenApiParameter(
                name='version',
                location=OpenApiParameter.QUERY,
                description='Версия справочника. Если не указана, то текущая версия',
                required=False,
                type=str
            ),
            OpenApiParameter(
                name='code',
                location=OpenApiParameter.QUERY,
                description='Код элемента справочника',
                required=True,
                type=str
            ),
            OpenApiParameter(
                name='value',
                location=OpenApiParameter.QUERY,
                description='Значение элемента справочника',
                required=True,
                type=str
            ),
        ],
        examples=[
            OpenApiExample(
                'Пример вывода 1',
                description='Вывод, если элемент существует',
                value="Существует"
            ),
            OpenApiExample(
                'Пример вывода 2',
                description='Вывод, если элемент не существует',
                value="Не существует"
            ),
        ],
)
class GuideElementCheckOut(APIView):
    """Проверка наличия элемента в справочнике."""

    def get_queryset(self) -> QuerySet:
        """Получает список элементов справочника."""
        guide_id = self.kwargs.get('pk')
        version = self.request.query_params.get('version')
        code = self.request.query_params.get('code')
        value = self.request.query_params.get('value')
        guide = get_object_or_404(Guide, pk=guide_id)
        if version is None:
            version_id = guide.current_version()
        else:
            version_id = Version.objects.filter(guide_id=guide_id, version=version).first()

        queryset = Element.objects.filter(version_id=version_id, code=code, value=value)
        return queryset

    def get(self, request, pk) -> Response:
        """Выводит результат проверки наличия элемента в справочнике."""
        queryset = self.get_queryset()
        if queryset.exists():
            return Response('Существует')
        return Response('Не существует')
