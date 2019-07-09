# Generated by Django 2.2.3 on 2019-07-09 05:42

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0010_auto_20190709_1318'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='animalencounter',
            options={'get_latest_by': 'when', 'verbose_name': 'Animal Encounter', 'verbose_name_plural': 'Animal Encounters'},
        ),
        migrations.AlterModelOptions(
            name='linetransectencounter',
            options={'get_latest_by': 'when', 'verbose_name': 'Line Transect Encounter', 'verbose_name_plural': 'Line Transect Encounters'},
        ),
        migrations.AlterModelOptions(
            name='loggerencounter',
            options={'get_latest_by': 'when', 'verbose_name': 'Logger Encounter', 'verbose_name_plural': 'Logger Encounters'},
        ),
        migrations.AlterModelOptions(
            name='turtlenestencounter',
            options={'get_latest_by': 'when', 'verbose_name': 'Turtle Nest Encounter', 'verbose_name_plural': 'Turtle Nest Encounters'},
        ),
        migrations.AlterIndexTogether(
            name='encounter',
            index_together={('when', 'where')},
        ),
    ]
