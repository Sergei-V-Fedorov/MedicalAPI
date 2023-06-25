from django.urls import path
from .views import GuidesList, GuideElementList, GuideElementCheckOut

app_name = 'medicalapi'

urlpatterns = [
    path('refbooks/', GuidesList.as_view(), name='refbooks'),
    path('refbooks/<int:pk>/elements', GuideElementList.as_view(), name='elements'),
    path('refbooks/<int:pk>/check_element', GuideElementCheckOut.as_view(), name='check'),
]
