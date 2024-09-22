from django.urls import path
from cscg.views import AbilityList,AbilityDetail,CharacterTypeDetail,CharacterTypeList,FlavorList,FlavorDetail,FocusList,FocusDetail,AbilityCSPageList
from cscg.views import AbilityUpdateView,AbilityCreateView,update_ab_cspage,getallab_json,AbilityOGCSPGList,FocusOGCSPGList,FocusOGCSPGListWithDetails

urlpatterns =[
    path('abilities/', AbilityList.as_view()),
    path('abilities_cs_page/', AbilityCSPageList.as_view()),
    path('abilities_cs_page/update', update_ab_cspage),
    path('abilities_ogcspg_/', AbilityOGCSPGList.as_view()),
    path('abilities_json/', getallab_json),
    path('abilities/<pk>/', AbilityDetail.as_view(), name="ability-detail"),
    path('types/',CharacterTypeList.as_view()),
    path('types/<pk>/',CharacterTypeDetail.as_view()),
    path('flavors/',FlavorList.as_view()),
    path('flavors/<pk>/',FlavorDetail.as_view()),
    path('focus/',FocusList.as_view()),
    path('focus/<pk>/',FocusDetail.as_view()),
    path('focus_ogcspg/', FocusOGCSPGList.as_view()),
    path('focus_ogcspg_details/', FocusOGCSPGListWithDetails.as_view()),
    path("ability/<int:pk>/", AbilityUpdateView.as_view(), name="ability-update"),
    path("ability-create/", AbilityCreateView.as_view(), name="ability-create"),
]