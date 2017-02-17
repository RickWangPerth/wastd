# -*- coding: utf-8 -*-
# Generated by Django 1.10.5 on 2017-02-01 08:32
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0070_nesttagobservation'),
    ]

    operations = [
        migrations.AddField(
            model_name='nesttagobservation',
            name='comments',
            field=models.TextField(blank=True, help_text='Any other comments or notes.', null=True, verbose_name='Comments'),
        ),
    ]