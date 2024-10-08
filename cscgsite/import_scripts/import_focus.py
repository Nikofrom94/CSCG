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
        self.name_en = ""
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
        focus_object = Focus.objects.create(
            name = self.name,
            name_en = self.name_en,
            description = self.description
            )
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
        else:
            print("WARNING : ",ab,", not found")
    return ab_pk_list

def import_focus(focus_en_fr,filename):
    focus_names = {}
    with open(focus_en_fr,'r') as focus_file:
        for line in focus_file:
            en_fr = line.split('/')
            focus_names[en_fr[1].strip()] = en_fr[0]
    with open(filename,'r') as ability_file:
        current_focus = None
        newfocus = None
        tier = 0
        for line in ability_file:
            if line.startswith("###"):
                current_focus = Focus_import()
                newfocus = None
                current_focus.name = line.lstrip(' #').strip()
                if current_focus.name in focus_names.keys():
                    current_focus.name_en = focus_names[current_focus.name]
                else:
                    print("WARNING: focus without en name",current_focus.name)
                print(current_focus.name)
                end_description = False
                continue
            if current_focus != None and end_description == False:
                if line.startswith('* '):
                    end_description = True
                    if current_focus.description.endswith('\n'):
                        current_focus.description = current_focus.description.rstrip('\n')
                else:
                    current_focus.description += line.replace('**','')
                    continue
            if 'Rang 1' in line:
                tier = 1
            elif 'Rang 2' in line:
                tier = 2
            elif 'Rang 3' in line:
                tier = 3
            elif 'Rang 4' in line:
                tier = 4
            elif 'Rang 5' in line:
                tier = 5
            elif 'Rang 6' in line:
                tier = 6
            if current_focus!=None and line.startswith('* '):
                if newfocus == None:
                    newfocus = Focus.objects.create(
                        name = current_focus.name,
                        name_en = current_focus.name_en,
                        description = current_focus.description
                        )
                    tier = 1
                suite = line[10:].strip()
                ab = None
                ab_choice = []
                if ' ou ' in suite:
                    ab = Ability.objects.filter(name=suite).first()
                    if ab == None:
                        ab_list = suite.split(' ou ')
                        for ab_name in ab_list:
                            a = Ability.objects.filter(name=ab_name).first()
                            if a != None:
                                ab_choice.append(a)
                            else:
                                print('WARNING Ability not found:',ab_name)
                else:
                    ab = Ability.objects.filter(name=suite).first()
                    if ab == None:
                        print('WARNING Ability not found:',suite)
                if tier == 1:
                    newfocus.abilities_tier1.add_ab(ab,ab_choice)
                elif tier == 2:
                    newfocus.abilities_tier2.add_ab(ab,ab_choice)
                elif tier == 3:
                    newfocus.abilities_tier3.add_ab(ab,ab_choice)
                elif tier == 4:
                    newfocus.abilities_tier4.add_ab(ab,ab_choice)
                elif tier == 5:
                    newfocus.abilities_tier5.add_ab(ab,ab_choice)
                elif tier == 6:
                    newfocus.abilities_tier6.add_ab(ab,ab_choice)
