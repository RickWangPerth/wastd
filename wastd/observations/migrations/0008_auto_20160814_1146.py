# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-14 03:46
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0007_auto_20160811_2207'),
    ]

    operations = [
        migrations.AddField(
            model_name='encounter',
            name='source',
            field=models.CharField(choices=[('direct', 'Direct entry'), ('paper', 'Paper data sheet'), ('wamtram', 'WAMTRAM 2 tagging DB'), ('ntp-exmouth', 'NTP Access DB Exmouth'), ('ntp-broome', 'NTP Access DB Broome')], default='direct', help_text='Where was this record captured initially?', max_length=300, verbose_name='Data Source'),
        ),
        migrations.AddField(
            model_name='encounter',
            name='source_id',
            field=models.CharField(blank=True, help_text='The ID of the record in the original source.', max_length=1000, null=True, verbose_name='Source ID'),
        ),
        migrations.AlterField(
            model_name='distinguishingfeatureobservation',
            name='algal_growth',
            field=models.CharField(choices=[('na', 'Not observed'), ('absent', 'Confirmed absent'), ('present', 'Confirmed present')], default='na', help_text='', max_length=300, verbose_name='Algal growth on carapace'),
        ),
        migrations.AlterField(
            model_name='distinguishingfeatureobservation',
            name='barnacles',
            field=models.CharField(choices=[('na', 'Not observed'), ('absent', 'Confirmed absent'), ('present', 'Confirmed present')], default='na', help_text='', max_length=300, verbose_name='Barnacles'),
        ),
        migrations.AlterField(
            model_name='distinguishingfeatureobservation',
            name='damage_injury',
            field=models.CharField(choices=[('na', 'Not observed'), ('absent', 'Confirmed absent'), ('present', 'Confirmed present')], default='na', help_text='', max_length=300, verbose_name='Obvious damage or injuries'),
        ),
        migrations.AlterField(
            model_name='distinguishingfeatureobservation',
            name='missing_limbs',
            field=models.CharField(choices=[('na', 'Not observed'), ('absent', 'Confirmed absent'), ('present', 'Confirmed present')], default='na', help_text='', max_length=300, verbose_name='Missing limbs'),
        ),
        migrations.AlterField(
            model_name='distinguishingfeatureobservation',
            name='propeller_damage',
            field=models.CharField(choices=[('na', 'Not observed'), ('absent', 'Confirmed absent'), ('present', 'Confirmed present')], default='na', help_text='', max_length=300, verbose_name='Propeller strike damage'),
        ),
        migrations.AlterField(
            model_name='distinguishingfeatureobservation',
            name='scanned_for_pit_tags',
            field=models.CharField(choices=[('na', 'Not observed'), ('absent', 'Confirmed absent'), ('present', 'Confirmed present')], default='na', help_text='', max_length=300, verbose_name='Scanned for PIT tags'),
        ),
        migrations.AlterField(
            model_name='distinguishingfeatureobservation',
            name='tagging_scars',
            field=models.CharField(choices=[('na', 'Not observed'), ('absent', 'Confirmed absent'), ('present', 'Confirmed present')], default='na', help_text='', max_length=300, verbose_name='Tagging scars'),
        ),
        migrations.AlterField(
            model_name='encounter',
            name='location_accuracy',
            field=models.CharField(choices=[('10', 'GPS reading at exact location (10 m)'), ('1000', 'Site centroid or place name (1 km)'), ('10000', 'Rough estimate (10 km)')], default='1000', help_text='The accuracy of the supplied location.', max_length=300, verbose_name='Location accuracy'),
        ),
        migrations.AlterField(
            model_name='observation',
            name='encounter',
            field=models.ForeignKey(default=1, help_text='The Encounter during which the observation was made', on_delete=django.db.models.deletion.CASCADE, to='observations.Encounter', verbose_name='Encounter'),
            preserve_default=False,
        ),
        migrations.AlterUniqueTogether(
            name='encounter',
            unique_together=set([('source', 'source_id')]),
        ),
    ]