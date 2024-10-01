from cscg.models import Cypher

class Cypher_import:
    def __init__(self):
        self.name = ""
        self.name_en = ""
        self.level = ""
        self.hint = ""
        self.effect = ""
        self.cs_page = "(Cypher System Rulebook, page 390)"
        self.table = ""
        self.obj = None
    
    def tohash(self):
        return {
            "name_en":self.name_en,
            'name':self.name,
            'level':self.level,
            'effect':self.effect,
            'hint':self.hint,
            'cs_page':self.cs_page,
            'table':self.table,
        }

    def create_Cypher(self):
        print(self.name)
        attributes = self.tohash()
        return Cypher.objects.create( **attributes )

def create_or_update(name,name_en):
    cypher = Cypher.objects.filter(name=name,name_en=name_en).first()
    if cypher == None:
        cypher = Cypher.objects.create(
            name=name,
            name_en=name_en,
            level = '',
            effect = '',
            hint = '',
            cs_page = '',
            table = ''
        )
        print(cypher.name_en, " -> create")
    else:
        print(cypher.name_en, " -> update")
    return cypher


def import_cypher(filename, update_fields=[]):
    if len(update_fields) == 0:
        update_fields = [
            'level',
            'effect',
            'hint',
            'cs_page',
            'table'
        ]
    with open(filename,'r') as cypher_file:
        start_hint = False
        end_hint = True
        start_table = False
        end_table = True
        new_cypher = None
        for line in cypher_file:
            if line.startswith('### '):
                if new_cypher != None and len(new_cypher.name) > 0:
                    new_cypher.save()
                start_hint = False
                end_hint = True
                start_table = False
                end_table = True
                names = line[4:].strip().split('/')
                name = ''
                name_en = ''
                if len(names) == 4:
                    name_en = names[0] + '/' + names[1]
                    name = names[2] + '/' + names[3]
                elif len(names) == 2:
                    name_en = names[0] 
                    name = names[1]
                else:
                    print("error in name",names)
                    exit(1)
                new_cypher = create_or_update(name,name_en)
            elif 'Niveau:' in line and 'level' in update_fields:
                new_cypher.level = line[len('**Niveau:**'):].strip()
            elif '*Effet:**' in line and 'effect' in update_fields:
                new_cypher.effect = line[len('**Effet:**'):].strip()
            elif '<table' in line and 'table' in update_fields:
                start_table = True
                new_cypher.table += line
                end_table = False
            elif '</table>' in line and 'table' in update_fields:
                new_cypher.table += line
                end_table = True
                start_table = False
                new_cypher.table = new_cypher.table.strip()
            elif start_table and not end_table and 'table' in update_fields:
                new_cypher.table += line
            elif '{{< hint info >}}' in line:
                start_hint = True
                end_hint = False
            elif '{{< /hint >}}' in line:
                new_cypher.hint = new_cypher.hint.strip()
                start_hint = False
                end_hint = True
            elif start_hint and not end_hint and 'hint' in update_fields:
                new_cypher.hint += line.strip()
        if new_cypher != None and len(new_cypher.name) > 0:
            new_cypher.save()

