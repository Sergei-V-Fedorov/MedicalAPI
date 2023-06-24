from django.urls import path
from .views import GuidesList, GuideElementDetail

urlpatterns = [
    path('refbooks/', GuidesList.as_view()),
    path('refbooks/<int:pk>/elements', GuideElementDetail.as_view()),
]
