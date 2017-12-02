# -*- coding: utf-8 -*-
# Generated by Django 1.11.7 on 2017-12-02 14:33
from __future__ import unicode_literals

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0102_auto_20171202_1326'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='encounter',
            name='site_visit',
        ),
        migrations.AddField(
            model_name='encounter',
            name='site',
            field=models.ForeignKey(blank=True, help_text='The surveyed site, if known.', null=True, on_delete=django.db.models.deletion.CASCADE, to='observations.Area', verbose_name='Surveyed site'),
        ),
    ]
