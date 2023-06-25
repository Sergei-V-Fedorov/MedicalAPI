from django.urls import path
from .views import GuidesList, GuideElementList, GuideElementCheckOut

urlpatterns = [
    path('refbooks/', GuidesList.as_view()),
    path('refbooks/<int:pk>/elements', GuideElementList.as_view()),
    path('refbooks/<int:pk>/check_element', GuideElementCheckOut.as_view()),
]
