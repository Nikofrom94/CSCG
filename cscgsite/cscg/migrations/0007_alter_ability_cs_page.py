# Generated by Django 5.1.1 on 2024-09-18 13:13

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cscg', '0006_alter_ability_stat_cost'),
    ]

    operations = [
        migrations.AlterField(
            model_name='ability',
            name='cs_page',
            field=models.CharField(default='', max_length=20),
        ),
    ]
