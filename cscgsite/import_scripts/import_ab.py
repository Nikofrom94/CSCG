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

def import_ab(filename,country_code):
    with open(filename,'r') as ability_file:
        current_ab = None
        for line in ability_file:
            if line.startswith("###"):
                if current_ab != None:
                    newab = current_ab.create_Ability()
                    current_ab = None
            elif line.startswith('**'):
                if current_ab != None:
                    newab = current_ab.create_Ability()
                current_ab = Ab_import(country_code)
                name = line[2:line.find("**",2)]
                suite = line[len(name)+4:].strip()
                if ('(' in suite) and (suite.find(':')>suite.find('(')):
                    stat = suite[suite.find('(')+1:suite.find(')')]
                    # stat_coststat_cost = stat[0:stat.find(' ')]
                    # stat = stat[len(stat_cost):]
                    # stat = stat.replace('points de','')
                    # stat = stat.replace('point de','')
                    # stat = stat.replace("point d'",'')
                    # stat = stat.replace("points d'",'')
                    stat = stat.strip()
                    current_ab.stat = stat
                    current_ab.stat_cost = ''
                current_ab.name = name
                description = suite[suite.find(':')+1:].strip()
                current_ab.description = description
            elif current_ab != None:
                current_ab.description += line
        if current_ab != None:
            newab = current_ab.create_Ability()
