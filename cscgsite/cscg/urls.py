from django.urls import path
from cscg.views import AbilityList,AbilityDetail,CharacterTypeDetail,CharacterTypeList,FlavorList,FlavorDetail,FocusList,FocusDetail,AbilityCSPageList
from cscg.views import AbilityUpdateView,AbilityCreateView,update_ab_cspage,getallab_json,AbilityOGCSPGList,FocusOGCSPGList,FocusOGCSPGListWithDetails
from cscg.views import DescriptorList,DescriptorDetail,DescriptorOGCSPGPageList,DescriptorOGCSPGList,AbilityIndexCompact
from cscg.views import AbilityCategoryUpdateView,AbilityCategoryList,AbilityCategoryDetail,AbilityCategoryOGList,AbilityListOG

urlpatterns =[
    #############################
    # AbilityCategory
    #############################
    path('ability_categories/', AbilityCategoryList.as_view()),
    path('ability_categories_og/', AbilityCategoryOGList.as_view()),
    path('ability_categories/<pk>/', AbilityCategoryDetail.as_view(), name="ability_category-detail"),
    path("ability_category/<int:pk>/", AbilityCategoryUpdateView.as_view(), name="ability_category-update"),
    #############################
    # Ability
    #############################
    path('abilities/', AbilityList.as_view()),
    path('abilities_og/', AbilityListOG.as_view()),
    path('abilities_cs_page/', AbilityCSPageList.as_view()),
    path('abilities_cs_page/update', update_ab_cspage),
    path('abilities_ogcspg_/', AbilityOGCSPGList.as_view()),
    path('abilities_indexcompact/', AbilityIndexCompact.as_view()),
    path('abilities_json/', getallab_json),
    path('abilities/<pk>/', AbilityDetail.as_view(), name="ability-detail"),
    path("ability/<int:pk>/", AbilityUpdateView.as_view(), name="ability-update"),
    path("ability-create/", AbilityCreateView.as_view(), name="ability-create"),
    #############################
    # CharacterType
    #############################    
    path('types/',CharacterTypeList.as_view()),
    path('types/<pk>/',CharacterTypeDetail.as_view()),
    #############################
    # Descriptor
    #############################
    path('descriptors/',DescriptorList.as_view()),
    path('descriptors/<pk>/',DescriptorDetail.as_view()),
    path('descriptors_ogcspg/', DescriptorOGCSPGPageList.as_view()),
    path('descriptors_ogcspg_links/', DescriptorOGCSPGList.as_view()),
    #############################
    # Flavor
    #############################
    path('flavors/',FlavorList.as_view()),
    path('flavors/<pk>/',FlavorDetail.as_view()),
    #############################
    # Focus
    #############################
    path('focus/',FocusList.as_view()),
    path('focus/<pk>/',FocusDetail.as_view()),
    path('focus_ogcspg/', FocusOGCSPGList.as_view()),
    path('focus_ogcspg_details/', FocusOGCSPGListWithDetails.as_view()),
]
