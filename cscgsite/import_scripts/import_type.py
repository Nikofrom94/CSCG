from cscg.models import CharacterType,Ability
import json

ab_tiers = [
    'abilities_tier1',
    'abilities_tier2',
    'abilities_tier3',
    'abilities_tier4',
    'abilities_tier5',
    'abilities_tier6',
]

def import_type(filename):
    with open(filename,'r') as typefile:
        typelist = json.load( typefile )
    for charactertype in typelist:
        print(charactertype['name'])
        type_object = CharacterType.objects.filter(name=charactertype['name']).first()
        if type_object == None:
            attributes = {}
            for key in charactertype.keys():
                if key not in ab_tiers:
                    attributes[key] = charactertype[key]
            type_object = CharacterType.objects.create(**attributes)
            for ab_tier in ab_tiers:
                ab_object_list = []
                for ab in charactertype[ab_tier]:
                    ab_object = Ability.objects.filter(name=ab['name']).first()
                    if ab_object != None:
                        if ab_tier == 'abilities_tier1':
                            type_object.abilities_tier1.add(ab_object)
                        elif ab_tier == 'abilities_tier2':
                            type_object.abilities_tier2.add(ab_object)
                        elif ab_tier == 'abilities_tier3':
                            type_object.abilities_tier3.add(ab_object)
                        elif ab_tier == 'abilities_tier4':
                            type_object.abilities_tier4.add(ab_object)
                        elif ab_tier == 'abilities_tier5':
                            type_object.abilities_tier5.add(ab_object)
                        elif ab_tier == 'abilities_tier6':
                            type_object.abilities_tier6.add(ab_object)

            
                

            

