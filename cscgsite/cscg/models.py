import json
from django.db import models
from django.core.validators import MinValueValidator,MaxValueValidator
from django.utils import timezone
from django.utils.translation import gettext
from django.urls import reverse

STAT_CHOICES={
    "M":"Might",
    "S":"Speed",
    "I":"Intellect",
}

SKILLLEVEL_CHOICES={
    "I":"Inability",
    "P":"Practiced",
    "T":"Trained",
    "S":"Specialized",
}

class CSModelGenericManager(models.Manager):
    def create(self,**kwargs):
        now = timezone.now()
        return super().create(**kwargs, pub_date=now,created=now,updated=now)

class CSModelGeneric(models.Model):
    pub_date = models.DateTimeField("date published")
    created = models.DateTimeField("date created")
    updated = models.DateTimeField("date updated")

    class Meta:
        abstract = True

class AbilityCategory(models.Model):
    name = models.CharField(max_length=50,db_index=True)
    name_en = models.CharField(max_length=50,default='')
    description = models.TextField()
    cs_page = models.CharField(default='',max_length=50)

    def get_absolute_url(self):
        return reverse("ability_category-detail", kwargs={"pk": self.pk})
    
    def get_anchor(self):
        return self.name_en.lower().replace(' ','-')
            
    def get_cspage(self):
        if self.cs_page.startswith('('):
            return self.cs_page
        else:
            return '('+self.cs_page+')'
        
    def get_lowtierabsquery(self):
        return self.ability_set.filter(tier='L').order_by('name')

    def get_midtierabsquery(self):
        return self.ability_set.filter(tier='M').order_by('name')

    def get_hightierabsquery(self):
        return self.ability_set.filter(tier='H').order_by('name')
        
class Ability(CSModelGeneric):
    objects=CSModelGenericManager()
    name = models.CharField(max_length=50,db_index=True)
    name_en = models.CharField(max_length=50,default='',db_index=True)
    stat_cost = models.CharField(max_length=50,null=True)
    stat = models.CharField(max_length=50,null=True,blank=True)
    description = models.TextField()
    cs_page = models.CharField(default='',max_length=20)
    tier = models.CharField(max_length=1,null=True,blank=True)
    categories = models.ManyToManyField( AbilityCategory )

    def get_absolute_url(self):
        return reverse("ability-detail", kwargs={"pk": self.pk})
    
    def __str__(self):
        if self.stat != None:
            stat_info = ' ('+self.stat+')'
        else:
            stat_info = ''
        return self.name+stat_info+':'+self.description
    
    def get_anchor(self):
        return self.name_en.lower().replace(' ','-')
            
    def get_cspage(self):
        if self.cs_page.startswith('('):
            return self.cs_page
        else:
            return '('+self.cs_page+')'
        
    def get_json(self):
        ab_json = {
            "name":self.name,
            "name_en":self.name_en,
            "description":self.description,
            "anchor":self.get_anchor(),
            "cs_page":self.get_cspage()
        }
        return json.dumps(ab_json,indent=2)
        

class CharacterType(CSModelGeneric):
    objects=CSModelGenericManager()
    name = models.CharField(max_length=50)
    might_start = models.PositiveSmallIntegerField()
    speed_start = models.PositiveSmallIntegerField()
    intellect_start = models.PositiveSmallIntegerField()
    might_edge_start = models.PositiveSmallIntegerField(default=0)
    speed_edge_start = models.PositiveSmallIntegerField(default=0)
    intellect_edge_start = models.PositiveSmallIntegerField(default=0)
    cyphers_start = models.PositiveSmallIntegerField(default=2)
    abilities_tier1 = models.ManyToManyField(
        "Ability",
        related_name="charactertype_ab_1s",
        related_query_name="charactertype_ab_1")
    abilities_tier2 = models.ManyToManyField(
        "Ability",
        related_name="charactertype_ab_2s",
        related_query_name="charactertype_ab_2")
    abilities_tier3 = models.ManyToManyField(
        "Ability",
        related_name="charactertype_ab_3s",
        related_query_name="charactertype_ab_3")
    abilities_tier4 = models.ManyToManyField(
        "Ability",
        related_name="charactertype_ab_4s",
        related_query_name="charactertype_ab_4")
    abilities_tier5 = models.ManyToManyField(
        "Ability",
        related_name="charactertype_ab_5s",
        related_query_name="charactertype_ab_5")
    abilities_tier6 = models.ManyToManyField(
        "Ability",
        related_name="charactertype_ab_6s",
        related_query_name="charactertype_ab_6")

class Flavor(CSModelGeneric):
    objects=CSModelGenericManager()
    name = models.CharField(max_length=50)
    description = models.TextField()
    abilities_tier1 = models.ManyToManyField(
        "Ability",
        related_name="flavor_ab_1s",
        related_query_name="flavor_ab_1")
    abilities_tier2 = models.ManyToManyField(
        "Ability",
        related_name="flavor_ab_2s",
        related_query_name="flavor_ab_2")
    abilities_tier3 = models.ManyToManyField(
        "Ability",
        related_name="flavor_ab_3s",
        related_query_name="flavor_ab_3")
    abilities_tier4 = models.ManyToManyField(
        "Ability",
        related_name="flavor_ab_4s",
        related_query_name="flavor_ab_4")
    abilities_tier5 = models.ManyToManyField(
        "Ability",
        related_name="flavor_ab_5s",
        related_query_name="flavor_ab_5")
    abilities_tier6 = models.ManyToManyField(
        "Ability",
        related_name="flavor_ab_6s",
        related_query_name="flavor_ab_6")

class FocusAbilities(models.Model):
    abilities = models.ManyToManyField(
        "Ability",
        related_name="focus_abs",
        related_query_name="focus_ab")
    abilities_to_choose = models.ManyToManyField(
        "Ability",
        related_name="focus_ab_choices",
        related_query_name="focus_ab_choice")

    def add_ab(self,ab,ab_choices):
        if ab != None:
            self.abilities.add(ab)
        elif ab_choices != None or len(ab_choices) != 0:
            for a in ab_choices:
                self.abilities_to_choose.add(a)

class FocusManager(CSModelGenericManager):
    def create(self,**kwargs):
        new_focus = super().create(**kwargs)
        new_focus.abilities_tier1 = FocusAbilities.objects.create()
        new_focus.abilities_tier2 = FocusAbilities.objects.create()
        new_focus.abilities_tier3 = FocusAbilities.objects.create()
        new_focus.abilities_tier4 = FocusAbilities.objects.create()
        new_focus.abilities_tier5 = FocusAbilities.objects.create()
        new_focus.abilities_tier6 = FocusAbilities.objects.create()
        new_focus.save()
        return new_focus

class Focus(CSModelGeneric):
    objects=FocusManager()
    name = models.CharField(max_length=50)
    name_en = models.CharField(max_length=50)
    description = models.TextField()
    abilities_tier1 = models.ForeignKey(
        "FocusAbilities",
        related_name="focus_ab_1s",
        related_query_name="focus_ab_1",
        null=True,
        on_delete=models.SET_NULL,
        )
    abilities_tier2 = models.ForeignKey(
        "FocusAbilities",
        related_name="focus_ab_2s",
        related_query_name="focus_ab_2",
        null=True,
        on_delete=models.SET_NULL,
        )
    abilities_tier3 = models.ForeignKey(
        "FocusAbilities",
        related_name="focus_ab_3s",
        related_query_name="focus_ab_3",
        null=True,
        on_delete=models.SET_NULL,
        )
    abilities_tier4 = models.ForeignKey(
        "FocusAbilities",
        related_name="focus_ab_4s",
        related_query_name="focus_ab_4",
        null=True,
        on_delete=models.SET_NULL,
        )
    abilities_tier5 = models.ForeignKey(
        "FocusAbilities",
        related_name="focus_ab_5s",
        related_query_name="focus_ab_5",
        null=True,
        on_delete=models.SET_NULL,
        )
    abilities_tier6 = models.ForeignKey(
        "FocusAbilities",
        related_name="focus_ab_6s",
        related_query_name="focus_ab_6",
        null=True,
        on_delete=models.SET_NULL,
        )
    
    def get_htmlid(self):
        return 'focus-'+self.name_en.replace(' ','-').lower().strip()
    
    def get_htmldescription(self):
        d = "<p>" + self.description+ "</p>"
        if "{{< hint info >}}" in d:
            d = d.replace("{{< hint info >}}",'<div class="og-sidebar pt-3 pb-1 ps-3 pe-3 mt-3 mb-3"><p> ')
            d = d.replace("{{< /hint >}}",'</p></div>')
        return d

class InitialLink(models.Model):
    description = models.CharField(max_length=150)

class DescriptorCharacteristic(models.Model):
    name = models.CharField(max_length=50)
    description = models.TextField()

class DescriptorManager(CSModelGenericManager):
    pass

class Descriptor(CSModelGeneric):
    objects = DescriptorManager()
    name = models.CharField(max_length=50)
    name_en = models.CharField(max_length=50,default='')
    description = models.TextField()
    characteristics= models.ManyToManyField("DescriptorCharacteristic") 
    initial_links = models.ManyToManyField("InitialLink")
    cs_page = models.CharField(default='',max_length=20)

    def get_anchor(self):
        return self.name_en.lower().replace(' ','-')
    
    def get_cs_page(self):
        if self.cs_page.startswith('('):
            return self.cs_page
        else:
            return '('+self.page+')'
    
    def get_description(self):
        pos_hint = self.description.find("{{< hint info >}}")
        if pos_hint > 0:
            return self.description[0:pos_hint].strip()
        else:
            return self.description

    def has_hint(self):
        pos_hint = self.description.find("{{< hint info >}}")
        return pos_hint > 0

    def get_hint(self):
        hint_prefix = "{{< hint info >}}"
        hint_suffix = "{{< /hint >}}"
        pos_hint = self.description.find(hint_prefix)
        if pos_hint > 0:
            return self.description[
                pos_hint+len(hint_prefix):self.description.find(hint_suffix)
                ].strip()
        else:
            return ""

    def get_ogformat(self):
        ogformat = """
                    &lt;div class="col-lg-6"&gt;<br>
                    &lt;h5 class="og-h-small og-border" id="descriptor-{anchor}"&gt;{name}&lt;a class="og-h-anchor" href="#descriptor-{anchor}" title="Permalink" aria-hidden="true"&gt;&lt;/a&gt;&lt;/h5&gt;<br>
                    &lt;p&gt;{description}&lt;/p&gt;<br>
                    &lt;p class="og-ind"&gt;Vous ajoutez les caractéristiques suivantes:&lt;/p&gt;<br>
                    &lt;ul class="list-unstyled og-ind"&gt;<br>\n""".format(
            anchor=self.get_anchor(),
            name=self.name,
            description=self.description,
            )
        for characteristic in self.characteristics.all():
            ogformat += """
                    &lt;li&gt;&lt;p&gt;&lt;strong&gt;{name}:&lt;/strong&gt; {description}&lt;/p&gt;&lt;/li&gt;<br>
                    """.format(name=characteristic.name,description=characteristic.description)
        ogformat += """&lt;li&gt;&lt;p&gt;&lt;strong&gt;Lien initial à la Première Aventure:&lt;/strong&gt;&lt;/p&gt;&lt;/li&gt;<br>
                    &lt;/ul&gt;<br>
                    &lt;ol&gt;<br>"""
        for link in self.initial_links.all():
            ogformat += "&lt;li&gt;{description}&lt;/li&gt;<br>\n".format(description=link.description)
        ogformat += """
                    &lt;/ol&gt;<br>
                    &lt;/div&gt;<br>\n"""
        return ogformat

class Skill(CSModelGeneric):
    name = models.CharField(max_length=50)
    
class Character(CSModelGeneric):
    name = models.CharField(max_length=50)
    tier = models.PositiveSmallIntegerField(default=1,validators=[MinValueValidator(1),MaxValueValidator(6)])
    character_type = models.ForeignKey("CharacterType", on_delete=models.SET_NULL,null=True)
    desciptors = models.ManyToManyField("Descriptor")
    focus = models.ForeignKey("Focus",on_delete=models.SET_NULL,null=True)
    flavor = models.ForeignKey("Flavor",on_delete=models.SET_NULL,null=True)
    might = models.PositiveSmallIntegerField(default=0)
    speed = models.PositiveSmallIntegerField(default=0)
    intellect = models.PositiveSmallIntegerField(default=0)
    might_edge = models.PositiveSmallIntegerField(default=0)
    speed_edge = models.PositiveSmallIntegerField(default=0)
    intellect_edge = models.PositiveSmallIntegerField(default=0)
    cyphers = models.PositiveSmallIntegerField(default=2)
    abilities = models.ManyToManyField("Ability")
    skills = models.ManyToManyField("CharacterSkill")

class CharacterSkill(models.Model):
    skill = models.ForeignKey("Skill",on_delete=models.SET_NULL,null=True)
    level = models.CharField(max_length=1,choices=SKILLLEVEL_CHOICES,default="P")

class I18NCodeManager(models.Manager):
    def get_or_create(self,code):
        cc = self.filter(name=code).first()
        if cc == None:
            attributes = {'name':code}
            cc = self.create(**attributes)
        return cc

class I18NCode(models.Model):
    objects=I18NCodeManager()
    name = models.CharField(max_length=50,primary_key=True)

class I18NCountryCodeManager(models.Manager):
    def get_or_create(self,country_code):
        cc = self.filter(name=country_code).first()
        if cc == None:
            attributes = {'name':country_code}
            cc = self.create(**attributes)
        return cc

class I18NCountryCode(models.Model):
    objects=I18NCountryCodeManager()
    name = models.CharField(max_length=50,primary_key=True)


class CSModelI18NFieldManager(models.Manager):
    def get_or_create(self,country_code,i18n_code):
        cc = I18NCountryCode.objects.get_or_create(country_code)
        code = I18NCode.objects.get_or_create(i18n_code)
        current_i18nfield = self.filter(countrycode_id=cc.name,code_id=code.name).first()
        if current_i18nfield == None:
            current_i18nfield = self.create(countrycode_id=cc.name,code_id=code.name)
        return current_i18nfield

class CSModelI18NField(models.Model):
    objects = CSModelI18NFieldManager()
    countrycode = models.ForeignKey("I18NCountryCode", on_delete=models.CASCADE)
    code = models.ForeignKey("I18NCode", on_delete=models.CASCADE)
    class Meta:
        abstract = True

class I18NCharFieldManager(CSModelI18NFieldManager):
    def get_or_create(self,country_code,i18n_code,content):
        current_i18nfield = super().get_or_create(country_code,i18n_code)
        if current_i18nfield.content != content:
            current_i18nfield.content = content
            current_i18nfield.save(update_fields=['content'])
        return current_i18nfield

class I18NCharField200(CSModelI18NField):
    objects = I18NCharFieldManager()
    content = models.CharField(max_length=200)

class I18NCharField50(CSModelI18NField):
    objects = I18NCharFieldManager()
    content = models.CharField(max_length=50)

class I18NCharField20(CSModelI18NField):
    objects = I18NCharFieldManager()
    content = models.CharField(max_length=20)

class I18NTextField(CSModelI18NField):
    objects = I18NCharFieldManager()
    content = models.TextField()

