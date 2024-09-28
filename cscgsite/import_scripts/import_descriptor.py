from cscg.models import Descriptor,InitialLink,DescriptorCharacteristic
import json

def reset():
    print("flushing descriptor in DB")
    result = DescriptorCharacteristic.objects.all().delete()
    result = InitialLink.objects.all().delete()
    result = Descriptor.objects.all().delete()

class DescriptorENFR():
    def __init__(self, name_fr='',name_en='',cs_page=''):
        self.name_fr = name_fr
        self.name_en = name_en
        self.cs_page = cs_page
    
    def __str__(self):
        return self.name_fr +"/"+self.name_en+" ("+self.cs_page+")"

class PoolBous():
    def __init__(self):
        self.pool = ''
        self.bonus = ''

class DescriptorImport():
    def __init__(self):
        self.name = ''
        self.name_en = ''
        self.description = ''
        self.characteristics = []
        self.initial_links = []
        self.cs_page = ''
    
    def create(self):
        newdescriptor = Descriptor.objects.create(
            name = self.name,
            description = self.description,
            name_en = self.name_en,
            cs_page = self.cs_page
        )
        newdescriptor.initial_links.set(self.initial_links)
        newdescriptor.characteristics.set(self.characteristics)
        return newdescriptor

def import_descriptor(descriptor_en_fr,filename):
    reset()
    descriptor_names = {}
    with open(descriptor_en_fr,'r') as focus_file:
        for line in focus_file:
            line = line.strip()
            en_fr = line.split('/')
            desc_en_fr = DescriptorENFR( name_fr = en_fr[2], name_en = en_fr[0], cs_page = en_fr[1] )
            descriptor_names[en_fr[2].strip()] = desc_en_fr
    with open(filename,'r') as descriptor_file:
        descriptor = None
        description_start = False
        description_end = False
        lien_initial_start = False
        for line in descriptor_file:
            line = line.strip()
            if line.startswith("###"):
                if descriptor != None:
                    newdescriptor = descriptor.create()
                descriptor = DescriptorImport()
                descriptor.name = line[3:].strip()
                if descriptor.name in descriptor_names.keys():
                    descriptor.name_en = descriptor_names[descriptor.name].name_en
                    descriptor.cs_page = descriptor_names[descriptor.name].cs_page
                print(descriptor.name )
                description_start = True
                description_end == False
                lien_initial_start = False
                continue
            elif 'Vous bénéficiez des caractéristiques suivantes:' in line:
                description_end == True
                continue
            elif line.startswith('**') and '**Lien initial' not in line:
                description_end == True
                charac_name = line[2:line.find('**',2)].strip().strip(':')
                charac_desc = line[line.find('**',2)+2:].strip()
                descriptor.characteristics.append(DescriptorCharacteristic.objects.create(
                    name=charac_name,
                    description=charac_desc
                ))
                continue
            elif '**Lien initial' in line:
                description_end == True
                lien_initial_start = True
                continue
            elif lien_initial_start and len(line.strip()) != 0 and not line.startswith('---'):
                lien = line[3:]
                descriptor.initial_links.append(InitialLink.objects.create(description=lien))
                continue
            elif line.startswith('---'):
                description_end == True
                newdescriptor = descriptor.create()
                descriptor = DescriptorImport()
                description_start = True
                description_end == False
                lien_initial_start = False
                continue
            elif description_start and description_end==False and lien_initial_start == False:
                descriptor.description += line
        if descriptor != None:
            newdescriptor = descriptor.create()
