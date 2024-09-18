from django.urls import path
from cscg.views import AbilityList,AbilityDetail,CharacterTypeDetail,CharacterTypeList,FlavorList,FlavorDetail,FocusList,FocusDetail
from cscg.views import AbilityUpdateView,AbilityCreateView

urlpatterns =[
    path('abilities/', AbilityList.as_view()),
    path('abilities/<pk>/', AbilityDetail.as_view(), name="ability-detail"),
    path('types/',CharacterTypeList.as_view()),
    path('types/<pk>/',CharacterTypeDetail.as_view()),
    path('flavors/',FlavorList.as_view()),
    path('flavors/<pk>/',FlavorDetail.as_view()),
    path('focus/',FocusList.as_view()),
    path('focus/<pk>/',FocusDetail.as_view()),
    path("ability/<int:pk>/", AbilityUpdateView.as_view(), name="ability-update"),
    path("ability-create/", AbilityCreateView.as_view(), name="ability-create"),
]