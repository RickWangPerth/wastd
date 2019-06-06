# Generated by Django 2.1.7 on 2019-06-06 08:38

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('conservation', '0022_auto_20190508_1542'),
    ]

    operations = [
        migrations.AlterField(
            model_name='conservationcategory',
            name='level',
            field=models.CharField(choices=[('extinct', 'Extinct'), ('threatened', 'Threatened'), ('priority', 'Priority'), ('other', 'Other')], default='other', help_text='The general conservation status, threatened, prority, or other.', max_length=500, verbose_name='Conservation level'),
        ),
        migrations.AlterField(
            model_name='conservationcategory',
            name='short_code',
            field=models.CharField(choices=[('O', 'Other'), ('X', 'Extinct'), ('T', 'Threatened'), ('SP', 'Specially Protected'), ('1', 'Priority 1'), ('2', 'Priority 2'), ('3', 'Priority 3'), ('4', 'Priority 4'), ('5', 'Priority 5')], default='O', help_text='The general conservation status, threatened, prority, or other.', max_length=500, verbose_name='Conservation short code'),
        ),
        migrations.AlterField(
            model_name='conservationthreat',
            name='encountered_by',
            field=models.ForeignKey(blank=True, help_text='The person who experienced the original encounter. DBCA staff have to visit this site to create a new profile. Add User profiles for external people through the data curation portal.', null=True, on_delete=django.db.models.deletion.PROTECT, to=settings.AUTH_USER_MODEL, verbose_name='Encountered by'),
        ),
    ]
