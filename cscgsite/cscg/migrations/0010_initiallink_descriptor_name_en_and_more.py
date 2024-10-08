# Generated by Django 5.1.1 on 2024-09-22 14:10

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('cscg', '0009_focus_name_en_alter_ability_stat_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='InitialLink',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('description', models.CharField(max_length=150)),
            ],
        ),
        migrations.AddField(
            model_name='descriptor',
            name='name_en',
            field=models.CharField(default='', max_length=50),
        ),
        migrations.AlterField(
            model_name='characterskill',
            name='level',
            field=models.CharField(choices=[('I', 'Inability'), ('P', 'Practiced'), ('T', 'Trained'), ('S', 'Specialized')], default='P', max_length=1),
        ),
        migrations.AddField(
            model_name='descriptor',
            name='initial_links',
            field=models.ManyToManyField(to='cscg.initiallink'),
        ),
    ]
