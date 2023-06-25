from django.db.models import Q
from rest_framework import generics, mixins
from rest_framework.generics import get_object_or_404
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Guide, Element, Version
from .serializers import GuideSerializer, ElementSerializer


class GuidesList(APIView):
    def get_queryset(self):
        requested_date = self.request.query_params.get('date')
        if requested_date:
            queryset = Guide.objects.filter(versions__since_date__lte=requested_date)
        else:
            queryset = Guide.objects.all()
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = GuideSerializer(queryset, many=True)
        json_response = {"refbooks": serializer.data}
        return Response(json_response)


class GuideElementList(APIView):
    def get_queryset(self):
        guide_id = self.kwargs.get('pk')
        version = self.request.query_params.get('version')
        guide = get_object_or_404(Guide, pk=guide_id)
        if version is None:
            version_id = guide.current_version().pk
        else:
            version_id = Version.objects.filter(guide_id=guide_id, version=version).first()

        queryset = Element.objects.filter(version_id=version_id).all()
        return queryset

    def get(self, request, *args, **kwargs):
        queryset = self.get_queryset()
        serializer = ElementSerializer(queryset, many=True)
        json_response = {"elements": serializer.data}
        return Response(json_response)


class GuideElementCheckOut(APIView):
    def get_queryset(self):
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

    def get(self, request, pk):
        queryset = self.get_queryset()
        if queryset.exists():
            return Response({'Element': 'Существует'})
        return Response({'Element': 'Не существует'})
