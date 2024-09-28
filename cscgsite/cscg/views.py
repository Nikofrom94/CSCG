from django.utils import timezone
from django.http import HttpResponseRedirect,JsonResponse
from django.shortcuts import render,get_object_or_404
from django.views.generic import ListView,DetailView
from django.views.generic.edit import FormView,CreateView, DeleteView, UpdateView
from django.views.generic.base import TemplateView
from cscg.models import CharacterType,Focus,Skill,Character,Descriptor,Flavor,Ability,Descriptor,AbilityCategory
from cscg.forms import AbilityForm
from django.core import serializers

class HomePageView(TemplateView):
    template_name = 'home.html'

####################################################
#  AbilityCategory
####################################################
class AbilityCategoryUpdateView(UpdateView):
    model = AbilityCategory
    template_name = "ability_category/ability_category_form.html"
    fields = ["name","name_en","description","cs_page"]
    context_object_name='ability_category'

class AbilityCategoryList(ListView):
    template_name = 'ability_category/ability_category_list.html'
    model=AbilityCategory
    context_object_name='ability_category_list'

class AbilityCategoryOGList(ListView):
    template_name = 'ability_category/ability_category_list_og.html'
    #model=AbilityCategory
    queryset = AbilityCategory.objects.order_by("name")
    context_object_name='ability_category_list'

class AbilityCategoryDetail(DetailView):
    template_name = 'ability_category/ability_category_detail.html'
    model=AbilityCategory
    context_object_name='ability_category'

####################################################
#  Ability
####################################################
class AbilityList(ListView):
    template_name = 'ability/ability_list.html'
    model=Ability
    context_object_name='ability_list'

class AbilityListOG(ListView):
    template_name = 'ability/ability_list_og.html'
    queryset = Ability.objects.order_by("name")
    context_object_name='ability_list'

class AbilityOGCSPGList(ListView):
    template_name = 'ability/ability_list_ogcspg.html'
    model=Ability
    context_object_name='ability_list'

class AbilityCSPageList(ListView):
    template_name = 'ability/ability_cs_page_list.html'
    queryset = Ability.objects.order_by("name_en")
    context_object_name='ability_list'

class AbilityIndexCompact(ListView):
    template_name = 'ability/ability_index_list_compact.html'
    queryset = Ability.objects.order_by("name")
    context_object_name='ability_list'
    

class AbilityJSONList(ListView):
    template_name = 'ability/ability_cs_page_list.html'
    queryset = Ability.objects.order_by("name_en")
    context_object_name='ability_list'

class AbilityDetail(DetailView):
    template_name = 'ability/ability_detail.html'
    model=Ability
    context_object_name='ability'

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

def update_ab_cspage(request):
    ab_id = request.POST['ab_id'] 
    ab = get_object_or_404(Ability,pk=ab_id)
    cs_page = request.POST["cs_page"]
    ab.cs_page = cs_page
    ab.save()
    response = JsonResponse({"ab_id": ab_id, "cs_page": cs_page, "result":"success"})
    return response

def getallab_json(request):
    response = JsonResponse(
        serializers.serialize(
            "json",
            Ability.objects.all(),

       ),
       safe=False
    )
    return response



####################################################
#  CharacterType
####################################################
class CharacterTypeList(ListView):
    template_name='charactertype/charactertype_list.html'
    model=CharacterType

class CharacterTypeDetail(DetailView):
    template_name = 'charactertype/charactertype_detail.html'
    model=CharacterType
    context_object_name='charactertype_list'

####################################################
#  Descriptor
####################################################
class DescriptorOGCSPGPageList(ListView):
    template_name = 'descriptor/descriptor_listogcspg_details.html'
    model = Descriptor
    #queryset = Descriptor.objects.order_by("name").all()
    context_object_name='descriptor_list'

class DescriptorOGCSPGList(ListView):
    template_name = 'descriptor/descriptor_listogcspg_links.html'
    model = Descriptor
    #queryset = Descriptor.objects.order_by("name").all()
    context_object_name='descriptor_list'

class DescriptorList(ListView):
    template_name='descriptor/descriptor_list.html'
    model=Descriptor
    context_object_name='descriptor_list'

class DescriptorDetail(DetailView):
    template_name = 'descriptor/descriptor_detail.html'
    model=Descriptor
    context_object_name='descriptor'

####################################################
#  Flavor
####################################################
class FlavorList(ListView):
    template_name='flavor/flavor_list.html'
    model=Flavor

class FlavorDetail(DetailView):
    template_name = 'flavor/flavor_detail.html'
    model=Flavor
    context_object_name='flavor'

####################################################
#  Focus
####################################################
class FocusOGCSPGList(ListView):
    template_name='focus/focus_list_ogcspg.html'
    model=Focus
    context_object_name='focus_list'

class FocusOGCSPGListWithDetails(ListView):
    template_name='focus/focus_list_ogcspg_details.html'
    model=Focus
    context_object_name='focus_list'

class FocusList(ListView):
    template_name='focus/focus_list.html'
    model=Focus
    context_object_name='focus_list'

class FocusDetail(DetailView):
    template_name = 'focus/focus_detail.html'
    model=Focus
    context_object_name='focus'

