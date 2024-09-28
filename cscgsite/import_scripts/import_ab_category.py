from cscg.models import Ability,I18NCountryCode,I18NCharField50,I18NTextField,AbilityCategory

class Ab_import:
    def __init__(self,country_code):
        self.name = ""
        self.description = ''

    def create(self):
        if self.description.endswith('\n'):
            self.description = self.description.rstrip('\n')
        #print(self.tohash())
        print(self.name)
        return AbilityCategory.objects.create(
                    name=self.name,
                    description=self.description
                    )

def import_ab_category(filename):
    with open(filename,'r') as ability_file:
        ab_category = None
        start_description=False
        tier_name = ''
        current_tier = ''
        for line in ability_file:
            if line.startswith("##"):
                ab_category = AbilityCategory.objects.filter(name=line[3:].strip()).first()
                if ab_category == None:
                    ab_category = AbilityCategory.objects.create(name=line[3:].strip(),description='')
                else:
                    ab_category.description=''
                print(ab_category.name)
                start_description=True
                continue
            elif '{{' in line or '<--->' in line:
                    pass
            elif line.strip().startswith("**"):
                start_description = False
                ab_category.save()
                if 'Inférieur' in line:
                    current_tier = 'L'
                elif 'Intermédiaire' in line:
                    current_tier = 'M'
                elif 'Supérieur' in line:
                    current_tier = 'H'
            elif len(line.strip()) == 0:
                pass
            elif line.strip().startswith ('* '):
                ab_list = []
                ab_name = line.strip('* ').strip()
                if ' or ' in ab_name:
                    ab_item = Ability.objects.filter(name=ab_name).first()
                    if ab_item == None:
                        ab_name_list = ab_name.split(' or ')
                        for choice in ab_name_list:
                            ab_item = Ability.objects.filter(name=choice).first()
                            if ab_item != None:
                                ab_list.append(ab_item)
                    else:
                        ab_list.append(ab_item)
                else:
                    ab_item = Ability.objects.filter(name=ab_name).first()
                    if ab_item != None:
                        ab_list.append(ab_item)
                if len(ab_list)>0:
                    for ab_item in ab_list:
                        if ab_item.categories.filter(name=ab_category.name).first() == None:
                            ab_item.categories.add(ab_category)
                        if ab_item.tier != current_tier:
                            ab_item.tier = current_tier
                            ab_item.save()
                else:
                    print(ab_name,"not found")
            elif start_description:
                ab_category.description += line.strip()
            
