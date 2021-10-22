# Generated by Django 3.1.13 on 2021-10-22 07:29

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('conservation', '0034_auto_20211022_1512'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communityconservationlisting',
            name='source_id',
            field=models.CharField(default=uuid.UUID('c0202e80-3309-11ec-87bb-6d83b420ce16'), help_text='The ID of the record in the original source, if available.', max_length=1000, verbose_name='Source ID'),
        ),
        migrations.AlterField(
            model_name='taxonconservationlisting',
            name='source_id',
            field=models.CharField(default=uuid.UUID('c0202e80-3309-11ec-87bb-6d83b420ce16'), help_text='The ID of the record in the original source, if available.', max_length=1000, verbose_name='Source ID'),
        ),
    ]
