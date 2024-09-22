from cscg.models import Descriptor,InitialLink
import json

class DescriptorENFR():
    def __init__(self, name_fr='',name_en='',cs_page=''):
        self.name_fr = name_fr
        self.name_en = name_en
        self.cs_page = cs_page

def import_descriptor(descriptor_en_fr,filename):
    descriptor_names = {}
    with open(descriptor_en_fr,'r') as focus_file:
        for line in focus_file:
            en_fr = line.split('/')
            desc_en_fr = DescriptorENFR( name_fr = en_fr[2], name_en = en_fr[0], cs_page = en_fr[1] )
            descriptor_names[en_fr[1].strip()] = desc_en_fr
    with open(filename,'r') as ability_file:
        current_focus = None
        newfocus = None
        tier = 0
        for line in ability_file:
            if line.startswith("###"):
                current_focus = Focus_import()
                newfocus = None
                current_focus.name = line.lstrip(' #').strip()
                if current_focus.name in descriptor_names.keys():
                    current_focus.name_en = descriptor_names[current_focus.name]
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
