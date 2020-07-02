# Generated by Django 2.2.13 on 2020-07-02 06:55

from django.db import migrations, models
import uuid


class Migration(migrations.Migration):

    dependencies = [
        ('conservation', '0031_auto_20200521_1437'),
    ]

    operations = [
        migrations.AlterField(
            model_name='communityconservationlisting',
            name='source_id',
            field=models.CharField(default=uuid.UUID('f64f4fc9-bc30-11ea-8c93-97af6dbfb137'), help_text='The ID of the record in the original source, if available.', max_length=1000, verbose_name='Source ID'),
        ),
        migrations.AlterField(
            model_name='taxonconservationlisting',
            name='source_id',
            field=models.CharField(default=uuid.UUID('f64f4fc9-bc30-11ea-8c93-97af6dbfb137'), help_text='The ID of the record in the original source, if available.', max_length=1000, verbose_name='Source ID'),
        ),
    ]
