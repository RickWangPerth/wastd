# Generated by Django 3.2.13 on 2022-05-26 01:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0050_auto_20220526_0948'),
    ]

    operations = [
        migrations.AlterField(
            model_name='campaignmediaattachment',
            name='media_type',
            field=models.CharField(choices=[('datasheet', 'Data sheet'), ('journal', 'Field journal'), ('communication', 'Communication record'), ('photograph', 'Photograph'), ('other', 'Other')], default='datasheet', help_text='What is the attached file about?', max_length=300, verbose_name='Attachment type'),
        ),
        migrations.AlterField(
            model_name='turtlehatchlingemergenceobservation',
            name='light_sources_present',
            field=models.CharField(choices=[('na', 'NA'), ('absent', 'Confirmed absent'), ('present', 'Confirmed present')], default='na', help_text='', max_length=300, verbose_name='Light sources present during emergence'),
        ),
        migrations.AlterField(
            model_name='turtlehatchlingemergenceobservation',
            name='outlier_tracks_present',
            field=models.CharField(choices=[('na', 'NA'), ('absent', 'Confirmed absent'), ('present', 'Confirmed present')], default='na', help_text='', max_length=300, verbose_name='Outlier tracks present'),
        ),
        migrations.AlterField(
            model_name='turtlehatchlingemergenceoutlierobservation',
            name='outlier_group_size',
            field=models.PositiveIntegerField(blank=True, help_text='', null=True, verbose_name='Number of tracks in outlier group'),
        ),
    ]
