from django.urls import path
from cscg.views import AbilityList,AbilityDetail

urlpatterns =[
    path('abilities/', AbilityList.as_view()),
    path('abilities/<pk>/', AbilityDetail.as_view()),
]