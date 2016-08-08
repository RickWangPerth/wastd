# -*- coding: utf-8 -*-
# Generated by Django 1.9.8 on 2016-08-08 02:14
from __future__ import unicode_literals

from django.conf import settings
import django.contrib.gis.db.models.fields
from django.db import migrations, models
import django.db.models.deletion
import django_fsm


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('contenttypes', '0002_remove_content_type_name'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Encounter',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', django_fsm.FSMField(choices=[('new', 'New'), ('proofread', 'Proofread'), ('curated', 'Curated'), ('published', 'Published')], default='new', max_length=50, verbose_name='QA Status')),
                ('when', models.DateTimeField(help_text='The observation datetime, shown here as local time, stored as UTC.', verbose_name='Observed on')),
                ('where', django.contrib.gis.db.models.fields.PointField(help_text='The observation location as point in WGS84', srid=4326, verbose_name='Observed at')),
                ('as_html', models.TextField(blank=True, editable=False, help_text='The cached HTML representation for display purposes.', null=True, verbose_name='HTML representation')),
            ],
            options={
                'ordering': ['when', 'where'],
                'get_latest_by': 'when',
                'verbose_name': 'Encounter',
                'verbose_name_plural': 'Encounters',
            },
        ),
        migrations.CreateModel(
            name='Observation',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AnimalEncounter',
            fields=[
                ('encounter_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='observations.Encounter')),
                ('species', models.CharField(choices=[('Natator depressus', 'Flatback turtle (Natator depressus)'), ('Chelonia mydas', 'Green turtle (Chelonia mydas)'), ('Eretmochelys imbricata', 'Hawksbill turtle (Eretmochelys imbricata)'), ('Caretta caretta', 'Loggerhead turtle (Caretta caretta)'), ('Lepidochelys olivacea', 'Olive Ridley turtle (Lepidochelys olivacea)'), ('Dermochelys coriacea', 'Leatherback turtle (Dermochelys coriacea)'), ('unidentified', 'Unidentified species')], default='unidentified', help_text='The species of the animal.', max_length=300, verbose_name='Species')),
                ('sex', models.CharField(choices=[('male', 'male'), ('female', 'female'), ('unknown', 'sex not determined or not examined'), ('intersex', 'hermaphrodite or intersex')], default='unknown', help_text="The animal's sex.", max_length=300, verbose_name='Sex')),
                ('maturity', models.CharField(choices=[('hatchling', 'hatchling'), ('juvenile', 'juvenile'), ('adult', 'adult'), ('unknown', 'unknown maturity')], default='unknown', help_text="The animal's maturity.", max_length=300, verbose_name='Maturity')),
                ('health', models.CharField(choices=[('alive', 'Alive (healthy)'), ('alive-injured', 'Alive (injured)'), ('alive-then-died', 'Initally alive (but died)'), ('dead-edible', 'Dead (carcass edible)'), ('dead-organs-intact', 'Dead (decomposed but organs intact)'), ('dead-advanced', 'Dead (advanced decomposition)'), ('dead-mummified', 'Mummified (dead, skin holding bones)'), ('dead-disarticulated', 'Disarticulated (dead, no soft tissue remaining)'), ('other', 'Other')], default='alive', help_text='On a scale from the Fresh Prince of Bel Air to 80s Hair Metal: how dead and decomposed is the animal?', max_length=300, verbose_name='Health status')),
                ('behaviour', models.TextField(blank=True, help_text='Notes on condition or behaviour if alive.', null=True, verbose_name='Behaviour')),
            ],
            options={
                'ordering': ['when', 'where'],
                'get_latest_by': 'when',
                'verbose_name': 'Animal Encounter',
                'verbose_name_plural': 'Animal Encounters',
            },
            bases=('observations.encounter',),
        ),
        migrations.CreateModel(
            name='DisposalObservation',
            fields=[
                ('observation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='observations.Observation')),
                ('management_actions', models.TextField(blank=True, help_text='Managment actions taken. Keep updating as appropriate.', null=True, verbose_name='Management Actions')),
                ('comments', models.TextField(blank=True, help_text='Any other comments or notes.', null=True, verbose_name='Comments')),
            ],
            options={
                'abstract': False,
            },
            bases=('observations.observation',),
        ),
        migrations.CreateModel(
            name='DistinguishingFeatureObservation',
            fields=[
                ('observation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='observations.Observation')),
                ('damage_injury', models.CharField(choices=[('na', 'Not observed'), ('absent', 'Confirmed absent'), ('present', 'Confirmed present')], default='na', help_text='', max_length=300, verbose_name='Obvious damage or injuries')),
                ('missing_limbs', models.CharField(choices=[('na', 'Not observed'), ('absent', 'Confirmed absent'), ('present', 'Confirmed present')], default='na', help_text='', max_length=300, verbose_name='Missing limbs')),
                ('barnacles', models.CharField(choices=[('na', 'Not observed'), ('absent', 'Confirmed absent'), ('present', 'Confirmed present')], default='na', help_text='', max_length=300, verbose_name='Barnacles')),
                ('algal_growth', models.CharField(choices=[('na', 'Not observed'), ('absent', 'Confirmed absent'), ('present', 'Confirmed present')], default='na', help_text='', max_length=300, verbose_name='Algal growth on carapace')),
                ('tagging_scars', models.CharField(choices=[('na', 'Not observed'), ('absent', 'Confirmed absent'), ('present', 'Confirmed present')], default='na', help_text='', max_length=300, verbose_name='Tagging scars')),
                ('propeller_damage', models.CharField(choices=[('na', 'Not observed'), ('absent', 'Confirmed absent'), ('present', 'Confirmed present')], default='na', help_text='', max_length=300, verbose_name='Propeller strike damage')),
                ('entanglement', models.CharField(choices=[('na', 'Not observed'), ('absent', 'Confirmed absent'), ('present', 'Confirmed present')], default='na', help_text='Entanglement in anthropogenic debris', max_length=300, verbose_name='Entanglement')),
                ('see_photo', models.CharField(choices=[('na', 'Not applicable'), ('see photos', 'See attached photos for details')], default='na', help_text='More relevant detail in attached photos', max_length=300, verbose_name='See attached photos')),
                ('comments', models.TextField(blank=True, help_text='Further comments on distinguising features.', null=True, verbose_name='Comments')),
            ],
            options={
                'abstract': False,
            },
            bases=('observations.observation',),
        ),
        migrations.CreateModel(
            name='MediaAttachment',
            fields=[
                ('observation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='observations.Observation')),
                ('media_type', models.CharField(choices=[('data_sheet', 'Original data sheet'), ('photograph', 'Photograph'), ('other', 'Other')], default='other', help_text='What is the attached file about?', max_length=300, verbose_name='Attachment type')),
                ('title', models.CharField(blank=True, help_text='Give the attachment a representative name', max_length=300, null=True, verbose_name='Attachment name')),
                ('attachment', models.FileField(help_text='Upload the file', upload_to='attachments/%Y/%m/%d/', verbose_name='File attachment')),
            ],
            options={
                'abstract': False,
            },
            bases=('observations.observation',),
        ),
        migrations.CreateModel(
            name='TagObservation',
            fields=[
                ('observation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='observations.Observation')),
                ('tag_type', models.CharField(choices=[('flipper-tag', 'Flipper Tag'), ('pit-tag', 'PIT Tag'), ('satellite-tag', 'Satellite Tag'), ('physical-sample', 'Physical Sample'), ('biopsy-sample', 'Biopsy Sample'), ('genetic-fingerprint', 'Genetic Fingerprint'), ('whisker-id', 'Whisker ID'), ('other', 'Other')], default='flipper-tag', help_text='What kind of tag is it?', max_length=300, verbose_name='Tag type')),
                ('side', models.CharField(choices=[('L', 'left front flipper'), ('R', 'right front flipper'), ('C', 'carapace'), ('N', 'neck'), ('O', 'other, see comments')], default='L', help_text='Is the tag on the left or right front flipper?', max_length=300, verbose_name='Tag side')),
                ('position', models.CharField(choices=[('1', '1st scale from body/head'), ('2', '2nd scale from body/head'), ('3', '3rd scale from body/head'), ('O', 'other, see comments')], default='1', help_text='Counting from inside, to which flipper scale is the tag attached?', max_length=300, verbose_name='Tag position')),
                ('name', models.CharField(help_text='The ID of a tag must be unique within the tag type.', max_length=1000, verbose_name='Tag ID')),
                ('status', models.CharField(choices=[('ordered', 'ordered from manufacturer'), ('produced', 'produced by manufacturer'), ('delivered', 'delivered to HQ'), ('allocated', 'allocated to field team'), ('attached', 'attached new to an animal'), ('recaptured', 're-sighted as attached to animal'), ('detached', 'taken off an animal'), ('found', 'found detached'), ('returned', 'returned to HQ'), ('decommissioned', 'decommissioned from active tag pool'), ('destroyed', 'destroyed'), ('observed', 'observed in any other context, see comments')], default='recaptured', help_text='The status this tag was seen in, or brought into.', max_length=300, verbose_name='Tag status')),
                ('comments', models.TextField(blank=True, help_text='Any other comments or notes.', null=True, verbose_name='Comments')),
            ],
            options={
                'abstract': False,
            },
            bases=('observations.observation',),
        ),
        migrations.CreateModel(
            name='TurtleMorphometricObservation',
            fields=[
                ('observation_ptr', models.OneToOneField(auto_created=True, on_delete=django.db.models.deletion.CASCADE, parent_link=True, primary_key=True, serialize=False, to='observations.Observation')),
                ('curved_carapace_length_mm', models.PositiveIntegerField(blank=True, help_text='The Curved Carapace Length in millimetres.', null=True, verbose_name='Curved Carapace Length (mm)')),
                ('curved_carapace_length_accuracy', models.CharField(choices=[('unknown', 'Unknown'), ('estimated', 'Estimated'), ('measured', 'Measured')], default='unknown', help_text='The measurement type as indication of accuracy.', max_length=300, verbose_name='Curved Carapace Length Accuracy')),
                ('curved_carapace_notch_mm', models.PositiveIntegerField(blank=True, help_text='The Curved Carapace Notch in millimetres.', null=True, verbose_name='Curved Carapace Notch (mm)')),
                ('curved_carapace_notch_accuracy', models.CharField(choices=[('unknown', 'Unknown'), ('estimated', 'Estimated'), ('measured', 'Measured')], default='unknown', help_text='The measurement type as indication of accuracy.', max_length=300, verbose_name='Curved Carapace Notch Accuracy')),
                ('curved_carapace_width_mm', models.PositiveIntegerField(blank=True, help_text='Curved Carapace Width in millimetres.', null=True, verbose_name='Curved Carapace Width (mm)')),
                ('curved_carapace_width_accuracy', models.CharField(choices=[('unknown', 'Unknown'), ('estimated', 'Estimated'), ('measured', 'Measured')], default='unknown', help_text='The measurement type as indication of accuracy.', max_length=300, verbose_name='Curved Carapace Width Accuracy')),
                ('tail_length_mm', models.PositiveIntegerField(blank=True, help_text='The Tail Length, measured from carapace in millimetres.', null=True, verbose_name='Tail Length (mm)')),
                ('tail_length_accuracy', models.CharField(choices=[('unknown', 'Unknown'), ('estimated', 'Estimated'), ('measured', 'Measured')], default='unknown', help_text='The measurement type as indication of accuracy.', max_length=300, verbose_name='Tail Length Accuracy')),
                ('maximum_head_width_mm', models.PositiveIntegerField(blank=True, help_text='The Maximum Head Width in millimetres.', null=True, verbose_name='Maximum Head Width (mm)')),
                ('maximum_head_width_accuracy', models.CharField(choices=[('unknown', 'Unknown'), ('estimated', 'Estimated'), ('measured', 'Measured')], default='unknown', help_text='The measurement type as indication of accuracy.', max_length=300, verbose_name='Maximum Head Width Accuracy')),
            ],
            options={
                'abstract': False,
            },
            bases=('observations.observation',),
        ),
        migrations.AddField(
            model_name='observation',
            name='encounter',
            field=models.ForeignKey(blank=True, help_text='The Encounter during which the observation was made', null=True, on_delete=django.db.models.deletion.CASCADE, to='observations.Encounter', verbose_name='Encounter'),
        ),
        migrations.AddField(
            model_name='observation',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_observations.observation_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='encounter',
            name='polymorphic_ctype',
            field=models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.CASCADE, related_name='polymorphic_observations.encounter_set+', to='contenttypes.ContentType'),
        ),
        migrations.AddField(
            model_name='encounter',
            name='who',
            field=models.ForeignKey(help_text='The observer has to be a registered system user', on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL, verbose_name='Observed by'),
        ),
    ]
