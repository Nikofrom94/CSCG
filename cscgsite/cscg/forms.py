from django import forms
from cscg.models import Ability

class AbilityForm(forms.Form):
    class meta:
        model=Ability
        fields=["name","name_en","stat","description","cs_page"]
    # name = forms.CharField(label="Nom", max_length=50, required=True)
    # name_en = forms.CharField(label="Nom en anglais",max_length=50)
    # stat = forms.CharField(label="Coût en stat",max_length=50,empty_value='')
    # description = forms.CharField(label="description",widget=forms.Textarea)
    # cs_page = forms.IntegerField(label="CS rulebook page ref")