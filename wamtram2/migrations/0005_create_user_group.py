# Generated by Django 4.2.11 on 2024-07-08 10:17

from django.db import migrations
from django.contrib.auth.models import Group, Permission
from django.contrib.contenttypes.models import ContentType

def create_tagging_data_entry_group(apps, schema_editor):
    # Create Tagging Data Entry group
    tagging_data_entry_group, created = Group.objects.get_or_create(name='Tagging Data Entry')

    # Get content types for models
    TrtEntryBatches = apps.get_model('wamtram2', 'TrtEntryBatches')
    TrtDataEntry = apps.get_model('wamtram2', 'TrtDataEntry')
    TrtTurtles = apps.get_model('wamtram2', 'TrtTurtles')
    TrtTags = apps.get_model('wamtram2', 'TrtTags')
    TrtPitTags = apps.get_model('wamtram2', 'TrtPitTags')

    # Define permissions to add
    permissions_to_add = []
    
    # Function to create or get permission
    def get_or_create_permission(model, codename, name):
        content_type = ContentType.objects.get_for_model(model)
        permission, created = Permission.objects.get_or_create(
            content_type=content_type,
            codename=codename,
            defaults={'name': name}
        )
        return permission

    # Create or get permissions for TrtEntryBatches
    permissions_to_add.extend([
        get_or_create_permission(TrtEntryBatches, 'add_trtentrybatches', 'Can add TRT entry batches'),
        get_or_create_permission(TrtEntryBatches, 'change_trtentrybatches', 'Can change TRT entry batches'),
        get_or_create_permission(TrtEntryBatches, 'view_trtentrybatches', 'Can view TRT entry batches'),
        get_or_create_permission(TrtEntryBatches, 'delete_trtentrybatches', 'Can delete TRT entry batches'),
    ])

    # Create or get permissions for TrtDataEntry
    permissions_to_add.extend([
        get_or_create_permission(TrtDataEntry, 'add_trtdataentry', 'Can add TRT data entry'),
        get_or_create_permission(TrtDataEntry, 'change_trtdataentry', 'Can change TRT data entry'),
        get_or_create_permission(TrtDataEntry, 'view_trtdataentry', 'Can view TRT data entry'),
        get_or_create_permission(TrtDataEntry, 'delete_trtdataentry', 'Can delete TRT data entry'),
    ])

    # Create or get permissions for TrtTurtles
    permissions_to_add.extend([
        get_or_create_permission(TrtTurtles, 'view_trtturtles', 'Can view TRT turtles'),
        get_or_create_permission(TrtTurtles, 'add_trtturtles', 'Can add TRT turtles'),
    ])

    # Create or get permissions for TrtTags
    permissions_to_add.extend([
        get_or_create_permission(TrtTags, 'view_trttags', 'Can view TRT tags'),
        get_or_create_permission(TrtTags, 'add_trttags', 'Can add TRT tags'),
    ])

    # Create or get permissions for TrtPitTags
    permissions_to_add.extend([
        get_or_create_permission(TrtPitTags, 'view_trtpittags', 'Can view TRT pit tags'),
        get_or_create_permission(TrtPitTags, 'add_trtpittags', 'Can add TRT pit tags'),
    ])

    # Add permissions to the group
    tagging_data_entry_group.permissions.add(*permissions_to_add)

def remove_tagging_data_entry_group(apps, schema_editor):
    # Remove Tagging Data Entry group
    Group.objects.filter(name='Tagging Data Entry').delete()

class Migration(migrations.Migration):

    dependencies = [
        ('wamtram2', '0004_alter_trtdataentry_options_alter_trtpersons_options_and_more'),
    ]

    operations = [
        migrations.RunPython(create_tagging_data_entry_group, remove_tagging_data_entry_group),
    ]