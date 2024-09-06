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
