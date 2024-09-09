from cscg.models import Focus,Ability
import json

ab_tiers = [
    'abilities_tier1',
    'abilities_tier2',
    'abilities_tier3',
    'abilities_tier4',
    'abilities_tier5',
    'abilities_tier6',
]

class Focus_import:
    def __init__(self):
        self.name = ""
        self.description = ""
        self.abilities_tier1 = []
        self.abilities_tier2 = []
        self.abilities_tier3 = []
        self.abilities_tier4 = []
        self.abilities_tier5 = []
        self.abilities_tier6 = []
    
    def __str__(self):
        return self.name + '->' + format(self.abilities_tier1)

    def tohash(self):
        return {
            'name':self.name,
            'description':self.description
        }

    def create_Focus(self):
        if self.description.endswith('\n'):
            self.description = self.description.rstrip('\n')
        focus_object = Focus.objects.create(name=self.name,description=self.description)
        focus_object.abilities_tier1.set(self.abilities_tier1)
        focus_object.abilities_tier2.set(self.abilities_tier2)
        focus_object.abilities_tier3.set(self.abilities_tier3)
        focus_object.abilities_tier4.set(self.abilities_tier4)
        focus_object.abilities_tier5.set(self.abilities_tier5)
        focus_object.abilities_tier6.set(self.abilities_tier6)

def get_Ability_pk(ability_list):
    ab_pk_list = []
    for ab in ability_list:
        ab_object = Ability.objects.filter(name=ab).first()
        if ab_object != None:
            ab_pk_list.append(ab_object.id)
    return ab_pk_list

def import_focus(filename):
    with open(filename,'r') as ability_file:
        current_focus = None
        for line in ability_file:
            if line.startswith("###"):
                if current_focus != None:
                    newfocus = current_focus.create_Focus()
                current_focus = Focus_import()
                current_focus.name = line.lstrip(' #').strip()
                print(current_focus.name)
                end_description = False
                continue
            if current_focus != None and end_description == False:
                if line.startswith('* '):
                    end_description = True
                else:
                    current_focus.description += line.replace('**','')
                    continue
            if current_focus!=None and line.startswith('* '):
                suite = line[10:].strip()
                ab_list = []
                if ' ou ' in suite:
                    ab_list = suite.split(' ou ')
                else:
                    ab_list.append(suite)
                if 'Rang 1' in line:
                    current_focus.abilities_tier1 += get_Ability_pk(ab_list)
                elif 'Rang 2' in line:
                    current_focus.abilities_tier2 += get_Ability_pk(ab_list)
                elif 'Rang 3' in line:
                    current_focus.abilities_tier3 += get_Ability_pk(ab_list)
                elif 'Rang 4' in line:
                    current_focus.abilities_tier4 += get_Ability_pk(ab_list)
                elif 'Rang 5' in line:
                    current_focus.abilities_tier5 += get_Ability_pk(ab_list)
                elif 'Rang 6' in line:
                    current_focus.abilities_tier6 += get_Ability_pk(ab_list)
        if current_focus != None:
            newfocus = current_focus.create_Focus()
