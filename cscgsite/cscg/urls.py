from django.urls import path
from cscg.views import AbilityList,AbilityDetail,CharacterTypeDetail,CharacterTypeList,FlavorList,FlavorDetail

urlpatterns =[
    path('abilities/', AbilityList.as_view()),
    path('abilities/<pk>/', AbilityDetail.as_view()),
    path('types/',CharacterTypeList.as_view()),
    path('types/<pk>/',CharacterTypeDetail.as_view()),
    path('flavors/',FlavorList.as_view()),
    path('flavors/<pk>/',FlavorDetail.as_view()),
]