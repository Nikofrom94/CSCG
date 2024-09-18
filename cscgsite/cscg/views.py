from django.utils import timezone
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView,DetailView
from django.views.generic.edit import FormView,CreateView, DeleteView, UpdateView
from django.views.generic.base import TemplateView
from cscg.models import CharacterType,Focus,Skill,Character,Descriptor,Flavor,Ability
from cscg.forms import AbilityForm

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


class FocusList(ListView):
    template_name='focus/focus_list.html'
    model=Focus
    context_object_name='focus_list'

class FocusDetail(DetailView):
    template_name = 'focus/focus_detail.html'
    model=Focus
    context_object_name='focus'

class AbilityUpdateView(UpdateView):
    model = Ability
    template_name = "ability/ability_form.html"
    #form_class = AbilityForm
    fields = ["name","name_en","stat","description","cs_page"]

    def form_valid(self, form):
        now = timezone.now()
        form.instance.updated = now
        if form.instance.stat == None or len(form.instance.stat.strip()) == 0:
            form.instance.stat = ''
        return super().form_valid(form)
    
class AbilityCreateView(CreateView):
    model = Ability
    template_name = "ability/ability_form_new.html"
    fields = ["name","name_en","stat","description","cs_page"]

    def form_valid(self, form):
        now = timezone.now()
        if form.instance.stat == None or len(form.instance.stat.strip()) == 0:
            form.instance.stat = ""
        form.instance.pub_date = now
        form.instance.created = now
        form.instance.updated = now
        return super().form_valid(form)

