# -*- coding: utf-8 -*-
# Generated by Django 1.10.3 on 2017-01-19 05:05
from __future__ import unicode_literals

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0056_auto_20170119_1248'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='tracktallyobservation',
            name='track_type',
        ),
        migrations.AddField(
            model_name='tracktallyobservation',
            name='nest_age',
            field=models.CharField(choices=[('old', '(O) old'), ('fresh', '(F) fresh'), ('unknown', '(U) unknown age')], default='unknown', help_text='The track or nest age.', max_length=300, verbose_name='Age'),
        ),
        migrations.AddField(
            model_name='tracktallyobservation',
            name='nest_type',
            field=models.CharField(choices=[('false-crawl', '(F) false crawl, non-nesting'), ('successful-crawl', '(S) successful crawl, nesting'), ('track-unsure', '(U) turtle track, success unsure'), ('track-not-assessed', '(T) turtle track, success not assessed'), ('nest', '(N) turtle nest, unhatched'), ('hatched-nest', '(H) turtle nest, hatched')], default='new-track-successful-crawl', help_text='The track or nest type.', max_length=300, verbose_name='Type'),
        ),
    ]