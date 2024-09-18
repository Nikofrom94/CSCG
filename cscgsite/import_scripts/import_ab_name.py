from cscg.models import Ability,I18NCountryCode,I18NCharField50,I18NTextField

class Ab_import:
    def __init__(self,country_code):
        self.country_code = country_code
        self.name = ""
        self.stat_cost = None
        self.stat = None
        self.description = ""
    
    def tohash(self):
        return {
            country_code:self.country_code,
            'name':self.name,
            'stat_cost':self.stat_cost,
            'stat':self.stat,
            'description':self.description
        }

    def create_Ability(self):
        if self.description.endswith('\n'):
            self.description = self.description.rstrip('\n')
        #print(self.tohash())
        print(self.name)
        return Ability.objects.create(
                    name=self.name,
                    stat_cost=self.stat_cost,
                    stat=self.stat,
                    description=self.description
                    )

def import_ab_name(filename):
    not_found = []
    with open(filename,'r') as ability_file:
        next_line_is_ab = False
        name_en = None
        name_fr = None
        for line in ability_file:
            if line.startswith("=="):
                next_line_is_ab = True
            elif next_line_is_ab:
                if line.find('/') > 0:
                    name_en = line[0:line.find('/')]
                    name_fr = line[len(name_en)+1:]
                else:
                    name_fr = line
                if ('(' in name_fr) and (name_fr.find(':')>name_fr.find('(')):
                    name_fr = name_fr[0:name_fr.find('(')].strip()
                else:
                    name_fr = name_fr[0:name_fr.find(':')].strip()
                next_line_is_ab = False
                if name_en == None:
                    name_en = name_fr
                ability_object = Ability.objects.filter(name=name_fr).first()
                if ability_object != None:
                    ability_object.name_en = name_en
                    ability_object.save()
                else:
                    not_found.append(name_fr)
                name_en = None
                name_fr = None

    for name_fr in not_found:
        print(name_fr)