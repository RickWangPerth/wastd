# Generated by Django 3.2.19 on 2023-07-06 01:35

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0002_auto_20230703_1420'),
    ]

    operations = [
        migrations.AlterField(
            model_name='surveymediaattachment',
            name='survey',
            field=models.ForeignKey(blank=True, help_text='The Survey this attachment belongs to.', null=True, on_delete=django.db.models.deletion.SET_NULL, related_name='attachments', to='observations.survey', verbose_name='Survey'),
        ),
        migrations.AlterField(
            model_name='turtlehatchlingemergenceobservation',
            name='hatchling_emergence_time_accuracy',
            field=models.CharField(blank=True, choices=[('na', 'NA'), ('same-night', 'Sometime that night'), ('plusminus-2h', 'Plus/minus 2h of estimate'), ('plusminus-30m', 'Correct to the hour')], default='na', help_text='.', max_length=300, null=True, verbose_name='Hatchling emergence time estimate accuracy'),
        ),
        migrations.AlterField(
            model_name='turtlehatchlingemergenceobservation',
            name='light_sources_present',
            field=models.CharField(choices=[('na', 'NA'), ('absent', 'Absent'), ('present', 'Present'), ('yes', 'Yes'), ('no', 'No')], default='na', help_text='', max_length=300, verbose_name='Light sources present during emergence'),
        ),
        migrations.AlterField(
            model_name='turtlehatchlingemergenceobservation',
            name='outlier_tracks_present',
            field=models.CharField(choices=[('na', 'NA'), ('absent', 'Absent'), ('present', 'Present'), ('yes', 'Yes'), ('no', 'No')], default='na', help_text='', max_length=300, verbose_name='Outlier tracks present'),
        ),
        migrations.AlterField(
            model_name='turtlehatchlingemergenceoutlierobservation',
            name='outlier_group_size',
            field=models.PositiveIntegerField(blank=True, help_text='', null=True, verbose_name='Number of tracks in outlier group'),
        ),
        migrations.AlterField(
            model_name='turtlenestdisturbanceobservation',
            name='disturbance_cause',
            field=models.CharField(choices=[('turtle', 'Other turtle'), ('bandicoot', 'Bandicoot predation'), ('bird', 'Bird predation'), ('crab', 'Crab predation'), ('croc', 'Croc predation'), ('cyclone', 'Cyclone disturbance'), ('dingo', 'Dingo predation'), ('dog', 'Dog predation'), ('cat', 'Cat predation'), ('fox', 'Fox predation'), ('goanna', 'Goanna predation'), ('human', 'Human'), ('pig', 'Pig predation'), ('tide', 'Tidal disturbance'), ('vehicle', 'Vehicle damage'), ('unknown', 'Unknown'), ('other', 'Other identifiable (see comments)')], help_text='The cause of the disturbance.', max_length=300, verbose_name='Disturbance cause'),
        ),
        migrations.AlterField(
            model_name='turtlenestdisturbancetallyobservation',
            name='disturbance_cause',
            field=models.CharField(choices=[('turtle', 'Other turtle'), ('bandicoot', 'Bandicoot predation'), ('bird', 'Bird predation'), ('crab', 'Crab predation'), ('croc', 'Croc predation'), ('cyclone', 'Cyclone disturbance'), ('dingo', 'Dingo predation'), ('dog', 'Dog predation'), ('cat', 'Cat predation'), ('fox', 'Fox predation'), ('goanna', 'Goanna predation'), ('human', 'Human'), ('pig', 'Pig predation'), ('tide', 'Tidal disturbance'), ('vehicle', 'Vehicle damage'), ('unknown', 'Unknown'), ('other', 'Other identifiable (see comments)')], default='turtle', help_text='The cause of the disturbance.', max_length=300, verbose_name='Disturbance cause'),
        ),
    ]