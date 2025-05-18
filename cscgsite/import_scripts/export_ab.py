from cscg.models import Ability
import csv

def export_ab():
    with open('ability.csv','w',encoding='utf-8',newline='') as csvfile:
        writer = csv.DictWriter(csvfile,fieldnames=['name','name_en','stat', 'description'])
        writer.writeheader()
        for ab in Ability.objects.all():
            writer.writerow(
                {
                    'name':ab.name,
                    'name_en':ab.name_en,
                    'stat':ab.stat,
                    'description':ab.description
                }
            )