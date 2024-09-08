from django.shortcuts import render
from django.views.generic import ListView,DetailView
from django.views.generic.edit import FormView
from django.views.generic.base import TemplateView
from cscg.models import CharacterType,Focus,Skill,Character,Descriptor,Flavor,Ability

class HomePageView(TemplateView):
    template_name = 'home.html'

class AbilityList(ListView):
    template_name = 'ability/ability_list.html'
    model=Ability
    context_object_name='ability_list'

class AbilityDetail(DetailView):
    template_name = 'ability/ability_detail.html'
    model=Ability
    context_object_name='ability'

class CharacterTypeList(ListView):
    template_name='charactertype/charactertype_list.html'
    model=CharacterType

class CharacterTypeDetail(DetailView):
    template_name = 'charactertype/charactertype_detail.html'
    model=CharacterType
    context_object_name='charactertype_list'

class FlavorList(ListView):
    template_name='flavor/flavor_list.html'
    model=Flavor

class FlavorDetail(DetailView):
    template_name = 'flavor/flavor_detail.html'
    model=Flavor
    context_object_name='flavor'

