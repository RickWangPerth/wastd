# This is an auto-generated Django model module.
# You'll have to do the following manually to clean this up:
#   * Rearrange models' order
#   * Make sure each model has one field with primary_key=True
#   * Make sure each ForeignKey and OneToOneField has `on_delete` set to the desired behavior
#   * Remove `managed = False` lines if you wish to allow Django to create, modify, and delete the table
# Feel free to rename the models, but don't rename db_table values or field names.
from datetime import datetime
from django.conf import settings
from django.contrib.gis.geos import Point
from django.db import models
from django.urls import reverse


class TrtActivities(models.Model):
    activity_code = models.CharField(db_column='ACTIVITY_CODE', primary_key=True, max_length=1)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=50)  # Field name made lowercase.
    nesting = models.CharField(db_column='NESTING', max_length=50)  # Field name made lowercase.
    new_code = models.CharField(db_column='New_Code', max_length=255, blank=True, null=True)  # Field name made lowercase.
    display_observation = models.BooleanField(db_column='Display_Observation')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_ACTIVITIES'


class TrtBeachPositions(models.Model):
    beach_position_code = models.CharField(db_column='BEACH_POSITION_CODE', primary_key=True, max_length=2)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=50)  # Field name made lowercase.
    new_code = models.CharField(db_column='New_Code', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_BEACH_POSITIONS'


class TrtBodyParts(models.Model):
    body_part = models.CharField(db_column='BODY_PART', primary_key=True, max_length=1)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=50)  # Field name made lowercase.
    flipper = models.BooleanField(db_column='FLIPPER')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_BODY_PARTS'


class TrtCauseOfDeath(models.Model):
    cause_of_death = models.CharField(db_column='CAUSE_OF_DEATH', primary_key=True, max_length=2)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_CAUSE_OF_DEATH'


class TrtConditionCodes(models.Model):
    condition_code = models.CharField(db_column='CONDITION_CODE', primary_key=True, max_length=1)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_CONDITION_CODES'


class TrtDamage(models.Model):
    observation = models.OneToOneField('TrtObservations', models.DO_NOTHING, db_column='OBSERVATION_ID', primary_key=True)  # Field name made lowercase.
    body_part = models.ForeignKey(TrtBodyParts, models.DO_NOTHING, db_column='BODY_PART')  # Field name made lowercase.
    damage_code = models.ForeignKey('TrtDamageCodes', models.DO_NOTHING, db_column='DAMAGE_CODE')  # Field name made lowercase.
    damage_cause_code = models.ForeignKey('TrtDamageCauseCodes', models.DO_NOTHING, db_column='DAMAGE_CAUSE_CODE', blank=True, null=True)  # Field name made lowercase.
    comments = models.CharField(db_column='COMMENTS', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_DAMAGE'
        unique_together = (('observation', 'body_part', 'body_part'),)


class TrtDamageCause(models.Model):
    observation_id = models.IntegerField(db_column='OBSERVATION_ID')  # Field name made lowercase.
    body_part = models.CharField(db_column='BODY_PART', max_length=1)  # Field name made lowercase.
    damage_code = models.CharField(db_column='DAMAGE_CODE', max_length=1)  # Field name made lowercase.
    damage_cause_code = models.CharField(db_column='DAMAGE_CAUSE_CODE', max_length=2, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_DAMAGE_CAUSE'


class TrtDamageCauseCodes(models.Model):
    damage_cause_code = models.CharField(db_column='DAMAGE_CAUSE_CODE', primary_key=True, max_length=2)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_DAMAGE_CAUSE_CODES'


class TrtDamageCodes(models.Model):
    damage_code = models.CharField(db_column='DAMAGE_CODE', primary_key=True, max_length=1)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=50)  # Field name made lowercase.
    flipper = models.BooleanField(db_column='FLIPPER')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_DAMAGE_CODES'


class TrtDataChanged(models.Model):
    trt_data_changed_id = models.AutoField(db_column='TRT_DATA_CHANGED_ID', primary_key=True)  # Field name made lowercase.
    datachanged_date = models.DateTimeField(db_column='DATACHANGED_DATE', blank=True, null=True)  # Field name made lowercase.
    datachangedby = models.CharField(db_column='DATACHANGEDBY', max_length=255, blank=True, null=True)  # Field name made lowercase.
    comment = models.CharField(db_column='COMMENT', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_DATA_CHANGED'


class TrtDataEntry(models.Model):
    data_entry_id = models.AutoField(db_column='DATA_ENTRY_ID', primary_key=True)  # Field name made lowercase.
    entry_batch = models.ForeignKey('TrtEntryBatches', models.DO_NOTHING, db_column='ENTRY_BATCH_ID')  # Field name made lowercase.
    user_entry_id = models.IntegerField(db_column='USER_ENTRY_ID')  # Field name made lowercase.
    turtle_id = models.IntegerField(db_column='TURTLE_ID', blank=True, null=True)  # Field name made lowercase.
    observation_id = models.IntegerField(db_column='OBSERVATION_ID', blank=True, null=True)  # Field name made lowercase.
    do_not_process = models.BooleanField(db_column='DO_NOT_PROCESS')  # Field name made lowercase.
    recapture_left_tag_id = models.CharField(db_column='RECAPTURE_LEFT_TAG_ID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    recapture_left_tag_id_2 = models.CharField(db_column='RECAPTURE_LEFT_TAG_ID_2', max_length=10, blank=True, null=True)  # Field name made lowercase.
    recapture_right_tag_id = models.CharField(db_column='RECAPTURE_RIGHT_TAG_ID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    recapture_right_tag_id_2 = models.CharField(db_column='RECAPTURE_RIGHT_TAG_ID_2', max_length=10, blank=True, null=True)  # Field name made lowercase.
    recapture_pit_tag_id = models.CharField(db_column='RECAPTURE_PIT_TAG_ID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    other_left_tag = models.CharField(db_column='OTHER_LEFT_TAG', max_length=2, blank=True, null=True)  # Field name made lowercase.
    other_right_tag = models.CharField(db_column='OTHER_RIGHT_TAG', max_length=2, blank=True, null=True)  # Field name made lowercase.
    new_left_tag_id = models.CharField(db_column='NEW_LEFT_TAG_ID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    new_left_tag_id_2 = models.CharField(db_column='NEW_LEFT_TAG_ID_2', max_length=10, blank=True, null=True)  # Field name made lowercase.
    new_right_tag_id = models.CharField(db_column='NEW_RIGHT_TAG_ID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    new_right_tag_id_2 = models.CharField(db_column='NEW_RIGHT_TAG_ID_2', max_length=10, blank=True, null=True)  # Field name made lowercase.
    new_pit_tag_id = models.CharField(db_column='NEW_PIT_TAG_ID', max_length=50, blank=True, null=True)  # Field name made lowercase.
    alive = models.CharField(db_column='ALIVE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    place_code = models.CharField(db_column='PLACE_CODE', max_length=4, blank=True, null=True)  # Field name made lowercase.
    observation_date = models.DateTimeField(db_column='OBSERVATION_DATE', blank=True, null=True)  # Field name made lowercase.
    observation_time = models.DateTimeField(db_column='OBSERVATION_TIME', blank=True, null=True)  # Field name made lowercase.
    nesting = models.CharField(db_column='NESTING', max_length=1, blank=True, null=True)  # Field name made lowercase.
    species_code = models.CharField(db_column='SPECIES_CODE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    identification_confidence = models.CharField(db_column='IDENTIFICATION_CONFIDENCE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    sex = models.CharField(db_column='SEX', max_length=1, blank=True, null=True)  # Field name made lowercase.
    curved_carapace_length = models.IntegerField(db_column='CURVED_CARAPACE_LENGTH', blank=True, null=True)  # Field name made lowercase.
    curved_carapace_width = models.IntegerField(db_column='CURVED_CARAPACE_WIDTH', blank=True, null=True)  # Field name made lowercase.
    activity_code = models.CharField(db_column='ACTIVITY_CODE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    beach_position_code = models.CharField(db_column='BEACH_POSITION_CODE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    damage_carapace = models.CharField(db_column='DAMAGE_CARAPACE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    damage_lff = models.CharField(db_column='DAMAGE_LFF', max_length=1, blank=True, null=True)  # Field name made lowercase.
    damage_rff = models.CharField(db_column='DAMAGE_RFF', max_length=1, blank=True, null=True)  # Field name made lowercase.
    damage_lhf = models.CharField(db_column='DAMAGE_LHF', max_length=1, blank=True, null=True)  # Field name made lowercase.
    damage_rhf = models.CharField(db_column='DAMAGE_RHF', max_length=1, blank=True, null=True)  # Field name made lowercase.
    body_part_1 = models.CharField(db_column='BODY_PART_1', max_length=1, blank=True, null=True)  # Field name made lowercase.
    damage_code_1 = models.CharField(db_column='DAMAGE_CODE_1', max_length=1, blank=True, null=True)  # Field name made lowercase.
    body_part_2 = models.CharField(db_column='BODY_PART_2', max_length=1, blank=True, null=True)  # Field name made lowercase.
    damage_code_2 = models.CharField(db_column='DAMAGE_CODE_2', max_length=1, blank=True, null=True)  # Field name made lowercase.
    egg_count = models.IntegerField(db_column='EGG_COUNT', blank=True, null=True)  # Field name made lowercase.
    egg_count_method = models.CharField(db_column='EGG_COUNT_METHOD', max_length=3, blank=True, null=True)  # Field name made lowercase.
    clutch_completed = models.CharField(db_column='CLUTCH_COMPLETED', max_length=1, blank=True, null=True)  # Field name made lowercase.
    measured_by = models.CharField(db_column='MEASURED_BY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    recorded_by = models.CharField(db_column='RECORDED_BY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tagged_by = models.CharField(db_column='TAGGED_BY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    entered_by = models.CharField(db_column='ENTERED_BY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    measured_recorded_by = models.CharField(db_column='MEASURED_RECORDED_BY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    measurement_type_1 = models.CharField(db_column='MEASUREMENT_TYPE_1', max_length=10, blank=True, null=True)  # Field name made lowercase.
    measurement_value_1 = models.FloatField(db_column='MEASUREMENT_VALUE_1', blank=True, null=True)  # Field name made lowercase.
    measurement_type_2 = models.CharField(db_column='MEASUREMENT_TYPE_2', max_length=10, blank=True, null=True)  # Field name made lowercase.
    measurement_value_2 = models.FloatField(db_column='MEASUREMENT_VALUE_2', blank=True, null=True)  # Field name made lowercase.
    datum_code = models.CharField(db_column='DATUM_CODE', max_length=5, blank=True, null=True)  # Field name made lowercase.
    zone = models.IntegerField(db_column='ZONE', blank=True, null=True)  # Field name made lowercase.
    easting = models.FloatField(db_column='EASTING', blank=True, null=True)  # Field name made lowercase.
    northing = models.FloatField(db_column='NORTHING', blank=True, null=True)  # Field name made lowercase.
    latitude = models.FloatField(db_column='LATITUDE', blank=True, null=True)  # Field name made lowercase.
    longitude = models.FloatField(db_column='LONGITUDE', blank=True, null=True)  # Field name made lowercase.
    latitude_degrees = models.IntegerField(db_column='LATITUDE_DEGREES', blank=True, null=True)  # Field name made lowercase.
    latitude_minutes = models.FloatField(db_column='LATITUDE_MINUTES', blank=True, null=True)  # Field name made lowercase.
    latitude_seconds = models.FloatField(db_column='LATITUDE_SECONDS', blank=True, null=True)  # Field name made lowercase.
    longitude_degrees = models.IntegerField(db_column='LONGITUDE_DEGREES', blank=True, null=True)  # Field name made lowercase.
    longitude_minutes = models.FloatField(db_column='LONGITUDE_MINUTES', blank=True, null=True)  # Field name made lowercase.
    longitude_seconds = models.FloatField(db_column='LONGITUDE_SECONDS', blank=True, null=True)  # Field name made lowercase.
    identification_type = models.CharField(db_column='IDENTIFICATION_TYPE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    identifier = models.CharField(db_column='IDENTIFIER', max_length=20, blank=True, null=True)  # Field name made lowercase.
    comment_fromrecordedtagstable = models.CharField(db_column='COMMENT_FROMRECORDEDTAGSTABLE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    scars_left = models.BooleanField(db_column='SCARS_LEFT')  # Field name made lowercase.
    scars_right = models.BooleanField(db_column='SCARS_RIGHT')  # Field name made lowercase.
    other_tags = models.CharField(db_column='OTHER_TAGS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    other_tags_identification_type = models.CharField(db_column='OTHER_TAGS_IDENTIFICATION_TYPE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    scars_left_scale_1 = models.BooleanField(db_column='SCARS_LEFT_SCALE_1')  # Field name made lowercase.
    scars_left_scale_2 = models.BooleanField(db_column='SCARS_LEFT_SCALE_2')  # Field name made lowercase.
    scars_left_scale_3 = models.BooleanField(db_column='SCARS_LEFT_SCALE_3')  # Field name made lowercase.
    scars_right_scale_1 = models.BooleanField(db_column='SCARS_RIGHT_SCALE_1')  # Field name made lowercase.
    scars_right_scale_2 = models.BooleanField(db_column='SCARS_RIGHT_SCALE_2')  # Field name made lowercase.
    scars_right_scale_3 = models.BooleanField(db_column='SCARS_RIGHT_SCALE_3')  # Field name made lowercase.
    cc_length_not_measured = models.BooleanField(db_column='CC_LENGTH_NOT_MEASURED')  # Field name made lowercase.
    cc_notch_length_not_measured = models.BooleanField(db_column='CC_NOTCH_LENGTH_NOT_MEASURED')  # Field name made lowercase.
    cc_width_not_measured = models.BooleanField(db_column='CC_WIDTH_NOT_MEASURED')  # Field name made lowercase.
    tagscarnotchecked = models.BooleanField(db_column='TAGSCARNOTCHECKED')  # Field name made lowercase.
    didnotcheckforinjury = models.BooleanField(db_column='DIDNOTCHECKFORINJURY')  # Field name made lowercase.
    comments = models.TextField(db_column='COMMENTS', blank=True, null=True)  # Field name made lowercase.
    error_number = models.IntegerField(db_column='ERROR_NUMBER', blank=True, null=True)  # Field name made lowercase.
    error_message = models.CharField(db_column='ERROR_MESSAGE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    recapture_left_tag_id_3 = models.CharField(db_column='RECAPTURE_LEFT_TAG_ID_3', max_length=10, blank=True, null=True)  # Field name made lowercase.
    recapture_right_tag_id_3 = models.CharField(db_column='RECAPTURE_RIGHT_TAG_ID_3', max_length=10, blank=True, null=True)  # Field name made lowercase.
    body_part_3 = models.CharField(db_column='BODY_PART_3', max_length=1, blank=True, null=True)  # Field name made lowercase.
    damage_code_3 = models.CharField(db_column='DAMAGE_CODE_3', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tissue_type_1 = models.CharField(db_column='TISSUE_TYPE_1', max_length=5, blank=True, null=True)  # Field name made lowercase.
    sample_label_1 = models.CharField(db_column='SAMPLE_LABEL_1', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tissue_type_2 = models.CharField(db_column='TISSUE_TYPE_2', max_length=5, blank=True, null=True)  # Field name made lowercase.
    sample_label_2 = models.CharField(db_column='SAMPLE_LABEL_2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    turtle_comments = models.CharField(db_column='TURTLE_COMMENTS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    recapture_pit_tag_id_2 = models.CharField(db_column='RECAPTURE_PIT_TAG_ID_2', max_length=50, blank=True, null=True)  # Field name made lowercase.
    new_pit_tag_id_2 = models.CharField(db_column='NEW_PIT_TAG_ID_2', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_DATA_ENTRY'
        unique_together = (('entry_batch', 'user_entry_id'),)


class TrtDataEntryExceptions(models.Model):
    entry_batch_id = models.IntegerField(db_column='ENTRY_BATCH_ID', primary_key=True)  # Field name made lowercase.
    data_entry_id = models.IntegerField(db_column='DATA_ENTRY_ID')  # Field name made lowercase.
    turtle_id = models.IntegerField(db_column='TURTLE_ID', blank=True, null=True)  # Field name made lowercase.
    observation_id = models.IntegerField(db_column='OBSERVATION_ID', blank=True, null=True)  # Field name made lowercase.
    recapture_left_tag_id = models.CharField(db_column='RECAPTURE_LEFT_TAG_ID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    recapture_right_tag_id = models.CharField(db_column='RECAPTURE_RIGHT_TAG_ID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    recapture_left_tag_id_2 = models.CharField(db_column='RECAPTURE_LEFT_TAG_ID_2', max_length=10, blank=True, null=True)  # Field name made lowercase.
    recapture_right_tag_id_2 = models.CharField(db_column='RECAPTURE_RIGHT_TAG_ID_2', max_length=10, blank=True, null=True)  # Field name made lowercase.
    other_left_tag = models.CharField(db_column='OTHER_LEFT_TAG', max_length=2, blank=True, null=True)  # Field name made lowercase.
    other_right_tag = models.CharField(db_column='OTHER_RIGHT_TAG', max_length=2, blank=True, null=True)  # Field name made lowercase.
    new_left_tag_id = models.CharField(db_column='NEW_LEFT_TAG_ID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    new_right_tag_id = models.CharField(db_column='NEW_RIGHT_TAG_ID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    alive = models.CharField(db_column='ALIVE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    place_code = models.CharField(db_column='PLACE_CODE', max_length=4, blank=True, null=True)  # Field name made lowercase.
    observation_date = models.DateTimeField(db_column='OBSERVATION_DATE', blank=True, null=True)  # Field name made lowercase.
    observation_time = models.DateTimeField(db_column='OBSERVATION_TIME', blank=True, null=True)  # Field name made lowercase.
    nesting = models.CharField(db_column='NESTING', max_length=1, blank=True, null=True)  # Field name made lowercase.
    species_code = models.CharField(db_column='SPECIES_CODE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    identification_confidence = models.CharField(db_column='IDENTIFICATION_CONFIDENCE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    sex = models.CharField(db_column='SEX', max_length=1, blank=True, null=True)  # Field name made lowercase.
    curved_carapace_length = models.IntegerField(db_column='CURVED_CARAPACE_LENGTH', blank=True, null=True)  # Field name made lowercase.
    curved_carapace_width = models.IntegerField(db_column='CURVED_CARAPACE_WIDTH', blank=True, null=True)  # Field name made lowercase.
    activity_code = models.CharField(db_column='ACTIVITY_CODE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    beach_position_code = models.CharField(db_column='BEACH_POSITION_CODE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    damage_carapace = models.CharField(db_column='DAMAGE_CARAPACE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    damage_lff = models.CharField(db_column='DAMAGE_LFF', max_length=1, blank=True, null=True)  # Field name made lowercase.
    damage_rff = models.CharField(db_column='DAMAGE_RFF', max_length=1, blank=True, null=True)  # Field name made lowercase.
    damage_lhf = models.CharField(db_column='DAMAGE_LHF', max_length=1, blank=True, null=True)  # Field name made lowercase.
    damage_rhf = models.CharField(db_column='DAMAGE_RHF', max_length=1, blank=True, null=True)  # Field name made lowercase.
    clutch_completed = models.CharField(db_column='CLUTCH_COMPLETED', max_length=1, blank=True, null=True)  # Field name made lowercase.
    egg_count = models.IntegerField(db_column='EGG_COUNT', blank=True, null=True)  # Field name made lowercase.
    egg_count_method = models.CharField(db_column='EGG_COUNT_METHOD', max_length=3, blank=True, null=True)  # Field name made lowercase.
    measured_by = models.CharField(db_column='MEASURED_BY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    recorded_by = models.CharField(db_column='RECORDED_BY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    tagged_by = models.CharField(db_column='TAGGED_BY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    measurement_type_1 = models.CharField(db_column='MEASUREMENT_TYPE_1', max_length=10, blank=True, null=True)  # Field name made lowercase.
    measurement_value_1 = models.FloatField(db_column='MEASUREMENT_VALUE_1', blank=True, null=True)  # Field name made lowercase.
    measurement_type_2 = models.CharField(db_column='MEASUREMENT_TYPE_2', max_length=10, blank=True, null=True)  # Field name made lowercase.
    measurement_value_2 = models.FloatField(db_column='MEASUREMENT_VALUE_2', blank=True, null=True)  # Field name made lowercase.
    datum_code = models.CharField(db_column='DATUM_CODE', max_length=5, blank=True, null=True)  # Field name made lowercase.
    latitude = models.FloatField(db_column='LATITUDE', blank=True, null=True)  # Field name made lowercase.
    longitude = models.FloatField(db_column='LONGITUDE', blank=True, null=True)  # Field name made lowercase.
    latitude_degrees = models.IntegerField(db_column='LATITUDE_DEGREES', blank=True, null=True)  # Field name made lowercase.
    latitude_minutes = models.FloatField(db_column='LATITUDE_MINUTES', blank=True, null=True)  # Field name made lowercase.
    latitude_seconds = models.FloatField(db_column='LATITUDE_SECONDS', blank=True, null=True)  # Field name made lowercase.
    longitude_degrees = models.IntegerField(db_column='LONGITUDE_DEGREES', blank=True, null=True)  # Field name made lowercase.
    longitude_minutes = models.FloatField(db_column='LONGITUDE_MINUTES', blank=True, null=True)  # Field name made lowercase.
    longitude_seconds = models.FloatField(db_column='LONGITUDE_SECONDS', blank=True, null=True)  # Field name made lowercase.
    zone = models.IntegerField(db_column='ZONE', blank=True, null=True)  # Field name made lowercase.
    easting = models.FloatField(db_column='EASTING', blank=True, null=True)  # Field name made lowercase.
    northing = models.FloatField(db_column='NORTHING', blank=True, null=True)  # Field name made lowercase.
    identification_type = models.CharField(db_column='IDENTIFICATION_TYPE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    identifier = models.CharField(db_column='IDENTIFIER', max_length=20, blank=True, null=True)  # Field name made lowercase.
    comments = models.CharField(db_column='COMMENTS', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_DATA_ENTRY_EXCEPTIONS'
        unique_together = (('entry_batch_id', 'data_entry_id'),)


class TrtDataEntryPersons(models.Model):
    data_entry_person_id = models.AutoField(db_column='DATA_ENTRY_PERSON_ID', primary_key=True)  # Field name made lowercase.
    entry_batch = models.ForeignKey('TrtEntryBatches', models.DO_NOTHING, db_column='ENTRY_BATCH_ID')  # Field name made lowercase.
    person_name = models.CharField(db_column='PERSON_NAME', max_length=100)  # Field name made lowercase.
    person_id = models.IntegerField(db_column='PERSON_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_DATA_ENTRY_PERSONS'
        unique_together = (('entry_batch', 'person_name'),)


class TrtDatumCodes(models.Model):
    datum_code = models.CharField(db_column='DATUM_CODE', primary_key=True, max_length=5)  # Field name made lowercase.
    datum_description = models.CharField(db_column='DATUM_DESCRIPTION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    semi_major_axis = models.FloatField(db_column='SEMI_MAJOR_AXIS', blank=True, null=True)  # Field name made lowercase.
    inverse_flattening = models.FloatField(db_column='INVERSE_FLATTENING', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_DATUM_CODES'


class TrtDefault(models.Model):
    id = models.CharField(db_column='ID', primary_key=True, max_length=10)  # Field name made lowercase.
    dataentry_exportpath = models.CharField(db_column='DataEntry_ExportPath', max_length=200)  # Field name made lowercase.
    dataentry_sourcedatabase = models.CharField(db_column='DataEntry_SourceDatabase', max_length=200, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_DEFAULT'


class TrtDocuments(models.Model):
    document_id = models.AutoField(db_column='DOCUMENT_ID', primary_key=True)  # Field name made lowercase.
    document_type = models.CharField(db_column='DOCUMENT_TYPE', max_length=10)  # Field name made lowercase.
    filename = models.CharField(db_column='FILENAME', max_length=255, blank=True, null=True)  # Field name made lowercase.
    turtle_id = models.IntegerField(db_column='TURTLE_ID', blank=True, null=True)  # Field name made lowercase.
    person_id = models.IntegerField(db_column='PERSON_ID', blank=True, null=True)  # Field name made lowercase.
    species_code = models.CharField(db_column='SPECIES_CODE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    title = models.CharField(db_column='TITLE', max_length=255, blank=True, null=True)  # Field name made lowercase.
    comments = models.CharField(db_column='COMMENTS', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_DOCUMENTS'


class TrtDocumentTypes(models.Model):
    document_type = models.CharField(db_column='DOCUMENT_TYPE', primary_key=True, max_length=10)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_DOCUMENT_TYPES'


class TrtEggCountMethods(models.Model):
    egg_count_method = models.CharField(db_column='EGG_COUNT_METHOD', primary_key=True, max_length=3)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_EGG_COUNT_METHODS'


class TrtEntryBatches(models.Model):
    entry_batch_id = models.AutoField(db_column='ENTRY_BATCH_ID', primary_key=True)  # Field name made lowercase.
    entry_date = models.DateTimeField(db_column='ENTRY_DATE', blank=True, null=True)  # Field name made lowercase.
    entered_person_id = models.IntegerField(db_column='ENTERED_PERSON_ID', blank=True, null=True)  # Field name made lowercase.
    filename = models.CharField(db_column='FILENAME', max_length=255, blank=True, null=True)  # Field name made lowercase.
    comments = models.CharField(db_column='COMMENTS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    pr_date_convention = models.BooleanField(db_column='PR_DATE_CONVENTION')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_ENTRY_BATCHES'


class TrtIdentification(models.Model):
    turtle = models.OneToOneField('TrtTurtles', models.DO_NOTHING, db_column='TURTLE_ID', primary_key=True)  # Field name made lowercase.
    identification_type = models.ForeignKey('TrtIdentificationTypes', models.DO_NOTHING, db_column='IDENTIFICATION_TYPE')  # Field name made lowercase.
    identifier = models.CharField(db_column='IDENTIFIER', max_length=20)  # Field name made lowercase.
    comments = models.CharField(db_column='COMMENTS', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_IDENTIFICATION'
        unique_together = (('turtle', 'identification_type', 'identifier'),)


class TrtIdentificationTypes(models.Model):
    identification_type = models.CharField(db_column='IDENTIFICATION_TYPE', primary_key=True, max_length=10)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_IDENTIFICATION_TYPES'


class TrtLocations(models.Model):
    location_code = models.CharField(db_column='LOCATION_CODE', primary_key=True, max_length=2)  # Field name made lowercase.
    location_name = models.CharField(db_column='LOCATION_NAME', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_LOCATIONS'


class TrtMeasurements(models.Model):
    observation = models.OneToOneField('TrtObservations', models.DO_NOTHING, db_column='OBSERVATION_ID', primary_key=True)  # Field name made lowercase.
    measurement_type = models.ForeignKey('TrtMeasurementTypes', models.DO_NOTHING, db_column='MEASUREMENT_TYPE')  # Field name made lowercase.
    measurement_value = models.FloatField(db_column='MEASUREMENT_VALUE')  # Field name made lowercase.
    comments = models.CharField(db_column='COMMENTS', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_MEASUREMENTS'
        unique_together = (('observation', 'measurement_type'),)


class TrtMeasurementTypes(models.Model):
    measurement_type = models.CharField(db_column='MEASUREMENT_TYPE', primary_key=True, max_length=10)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=100)  # Field name made lowercase.
    measurement_units = models.CharField(db_column='MEASUREMENT_UNITS', max_length=10, blank=True, null=True)  # Field name made lowercase.
    minimum_value = models.FloatField(db_column='MINIMUM_VALUE', blank=True, null=True)  # Field name made lowercase.
    maximum_value = models.FloatField(db_column='MAXIMUM_VALUE', blank=True, null=True)  # Field name made lowercase.
    comments = models.CharField(db_column='COMMENTS', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_MEASUREMENT_TYPES'


class TrtNesting(models.Model):
    place_code = models.CharField(db_column='PLACE_CODE', primary_key=True, max_length=4)  # Field name made lowercase.
    species_code = models.CharField(db_column='SPECIES_CODE', max_length=2)  # Field name made lowercase.
    comments = models.CharField(db_column='COMMENTS', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_NESTING'
        unique_together = (('place_code', 'species_code'),)


class TrtNestingSeason(models.Model):
    nesting_seasonid = models.AutoField(db_column='NESTING_SEASONID', primary_key=True)  # Field name made lowercase.
    nesting_season = models.CharField(db_column='NESTING_SEASON', max_length=20)  # Field name made lowercase.
    startdate = models.DateTimeField(db_column='STARTDATE')  # Field name made lowercase.
    enddate = models.DateTimeField(db_column='ENDDATE')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_NESTING_SEASON'


class TrtObservations(models.Model):
    observation_id = models.AutoField(db_column='OBSERVATION_ID', primary_key=True)  # Field name made lowercase.
    turtle = models.ForeignKey('TrtTurtles', models.DO_NOTHING, db_column='TURTLE_ID', related_name='observations')  # Field name made lowercase.
    observation_date = models.DateTimeField(db_column='OBSERVATION_DATE')  # Field name made lowercase.
    observation_time = models.DateTimeField(db_column='OBSERVATION_TIME', blank=True, null=True)  # Field name made lowercase.
    observation_date_old = models.DateTimeField(db_column='OBSERVATION_DATE_OLD', blank=True, null=True)  # Field name made lowercase.
    alive = models.CharField(db_column='ALIVE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    measurer_person = models.ForeignKey('TrtPersons', models.DO_NOTHING, db_column='MEASURER_PERSON_ID', blank=True, null=True, related_name='measurer_person')  # Field name made lowercase.
    measurer_reporter_person = models.ForeignKey('TrtPersons', models.DO_NOTHING, db_column='MEASURER_REPORTER_PERSON_ID', blank=True, null=True, related_name='measurer_reporter_person')  # Field name made lowercase.
    tagger_person = models.ForeignKey('TrtPersons', models.DO_NOTHING, db_column='TAGGER_PERSON_ID', blank=True, null=True, related_name='tagger_person')  # Field name made lowercase.
    reporter_person = models.ForeignKey('TrtPersons', models.DO_NOTHING, db_column='REPORTER_PERSON_ID', blank=True, null=True, related_name='reporter_person')  # Field name made lowercase.
    place_code = models.ForeignKey('TrtPlaces', models.DO_NOTHING, db_column='PLACE_CODE', blank=True, null=True)  # Field name made lowercase.
    place_description = models.CharField(db_column='PLACE_DESCRIPTION', max_length=300, blank=True, null=True)  # Field name made lowercase.
    datum_code = models.ForeignKey(TrtDatumCodes, models.DO_NOTHING, db_column='DATUM_CODE', blank=True, null=True)  # Field name made lowercase.
    latitude = models.FloatField(db_column='LATITUDE', blank=True, null=True)  # Field name made lowercase.
    longitude = models.FloatField(db_column='LONGITUDE', blank=True, null=True)  # Field name made lowercase.
    latitude_degrees = models.IntegerField(db_column='LATITUDE_DEGREES', blank=True, null=True)  # Field name made lowercase.
    latitude_minutes = models.FloatField(db_column='LATITUDE_MINUTES', blank=True, null=True)  # Field name made lowercase.
    latitude_seconds = models.FloatField(db_column='LATITUDE_SECONDS', blank=True, null=True)  # Field name made lowercase.
    longitude_degrees = models.IntegerField(db_column='LONGITUDE_DEGREES', blank=True, null=True)  # Field name made lowercase.
    longitude_minutes = models.FloatField(db_column='LONGITUDE_MINUTES', blank=True, null=True)  # Field name made lowercase.
    longitude_seconds = models.FloatField(db_column='LONGITUDE_SECONDS', blank=True, null=True)  # Field name made lowercase.
    zone = models.IntegerField(db_column='ZONE', blank=True, null=True)  # Field name made lowercase.
    easting = models.FloatField(db_column='EASTING', blank=True, null=True)  # Field name made lowercase.
    northing = models.FloatField(db_column='NORTHING', blank=True, null=True)  # Field name made lowercase.
    activity_code = models.ForeignKey('TrtActivities', models.DO_NOTHING, db_column='ACTIVITY_CODE', blank=True, null=True)  # Field name made lowercase.
    beach_position_code = models.ForeignKey(TrtBeachPositions, models.DO_NOTHING, db_column='BEACH_POSITION_CODE', blank=True, null=True)  # Field name made lowercase.
    condition_code = models.ForeignKey(TrtConditionCodes, models.DO_NOTHING, db_column='CONDITION_CODE', blank=True, null=True)  # Field name made lowercase.
    nesting = models.CharField(db_column='NESTING', max_length=1, blank=True, null=True)  # Field name made lowercase.
    clutch_completed = models.CharField(db_column='CLUTCH_COMPLETED', max_length=1, blank=True, null=True)  # Field name made lowercase.
    number_of_eggs = models.SmallIntegerField(db_column='NUMBER_OF_EGGS', blank=True, null=True)  # Field name made lowercase.
    egg_count_method = models.ForeignKey(TrtEggCountMethods, models.DO_NOTHING, db_column='EGG_COUNT_METHOD', blank=True, null=True)  # Field name made lowercase.
    measurements = models.CharField(db_column='MEASUREMENTS', max_length=1)  # Field name made lowercase.
    action_taken = models.CharField(db_column='ACTION_TAKEN', max_length=255, blank=True, null=True)  # Field name made lowercase.
    comments = models.TextField(db_column='COMMENTS', blank=True, null=True)  # Field name made lowercase.
    entered_by = models.CharField(db_column='ENTERED_BY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    date_entered = models.DateTimeField(db_column='DATE_ENTERED', blank=True, null=True)  # Field name made lowercase.
    original_observation_id = models.IntegerField(db_column='ORIGINAL_OBSERVATION_ID', blank=True, null=True)  # Field name made lowercase.
    entry_batch = models.ForeignKey(TrtEntryBatches, models.DO_NOTHING, db_column='ENTRY_BATCH_ID', blank=True, null=True)  # Field name made lowercase.
    comment_fromrecordedtagstable = models.TextField(db_column='COMMENT_FROMRECORDEDTAGSTABLE', blank=True, null=True)  # Field name made lowercase.
    scars_left = models.BooleanField(db_column='SCARS_LEFT')  # Field name made lowercase.
    scars_right = models.BooleanField(db_column='SCARS_RIGHT')  # Field name made lowercase.
    other_tags = models.CharField(db_column='OTHER_TAGS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    other_tags_identification_type = models.ForeignKey(TrtIdentificationTypes, models.DO_NOTHING, db_column='OTHER_TAGS_IDENTIFICATION_TYPE', blank=True, null=True)  # Field name made lowercase.
    transferid = models.IntegerField(db_column='TransferID', blank=True, null=True)  # Field name made lowercase.
    mund = models.BooleanField(db_column='Mund')  # Field name made lowercase.
    entered_by_person = models.ForeignKey('TrtPersons', models.DO_NOTHING, db_column='ENTERED_BY_PERSON_ID', blank=True, null=True)  # Field name made lowercase.
    scars_left_scale_1 = models.BooleanField(db_column='SCARS_LEFT_SCALE_1')  # Field name made lowercase.
    scars_left_scale_2 = models.BooleanField(db_column='SCARS_LEFT_SCALE_2')  # Field name made lowercase.
    scars_left_scale_3 = models.BooleanField(db_column='SCARS_LEFT_SCALE_3')  # Field name made lowercase.
    scars_right_scale_1 = models.BooleanField(db_column='SCARS_RIGHT_SCALE_1')  # Field name made lowercase.
    scars_right_scale_2 = models.BooleanField(db_column='SCARS_RIGHT_SCALE_2')  # Field name made lowercase.
    scars_right_scale_3 = models.BooleanField(db_column='SCARS_RIGHT_SCALE_3')  # Field name made lowercase.
    cc_length_not_measured = models.BooleanField(db_column='CC_LENGTH_Not_Measured')  # Field name made lowercase.
    cc_notch_length_not_measured = models.BooleanField(db_column='CC_NOTCH_LENGTH_Not_Measured')  # Field name made lowercase.
    cc_width_not_measured = models.BooleanField(db_column='CC_WIDTH_Not_Measured')  # Field name made lowercase.
    tagscarnotchecked = models.BooleanField(db_column='TagScarNotChecked')  # Field name made lowercase.
    didnotcheckforinjury = models.BooleanField(db_column='DidNotCheckForInjury')  # Field name made lowercase.
    date_convention = models.CharField(db_column='DATE_CONVENTION', max_length=1)  # Field name made lowercase.
    observation_status = models.CharField(db_column='OBSERVATION_STATUS', max_length=50, blank=True, null=True)  # Field name made lowercase.
    corrected_date = models.DateTimeField(db_column='CORRECTED_DATE', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_OBSERVATIONS'
        unique_together = (('observation_id', 'turtle'),)
        #ordering = ('-observation_date', '-observation_time')  # NOTE: ordering doesn't work.

    def __str__(self):
        if self.observation_status:
            return f'{self.observation_id} ({self.get_observation_datetime_awst().isoformat()}) {(self.observation_status)}'
        else:
            return f'{self.observation_id} ({self.get_observation_datetime_awst().isoformat()})'

    def get_observation_datetime_awst(self):
        """Returns a combined observation datetime, in AWST.
        """
        if self.observation_time:
            return datetime(self.observation_date.year, self.observation_date.month, self.observation_date.day, self.observation_time.hour, self.observation_time.minute, tzinfo=settings.AWST)
        else:
            return datetime(self.observation_date.year, self.observation_date.month, self.observation_date.day, 0, 0, tzinfo=settings.AWST)

    def get_observation_datetime_utc(self):
        """Returns a combined observation datetime, in UTC.
        """
        if self.observation_time:
            obs = datetime(self.observation_date.year, self.observation_date.month, self.observation_date.day, self.observation_time.hour, self.observation_time.minute, tzinfo=settings.AWST)
        else:
            obs = datetime(self.observation_date.year, self.observation_date.month, self.observation_date.day, 0, 0, tzinfo=settings.AWST)
        return obs.astimezone(settings.UTC)

    def get_point(self):
        """Returns a geometry point as WGS84.
        """
        if not self.longitude or not self.latitude:
            return None
        if self.datum_code:
            if self.datum_code.datum_code == "AGD66":
                datum = 4202
            elif self.datum_code.datum_code == "AGD66":
                datum = 4203
            elif self.datum_code.datum_code == "GDA94":
                datum = 4283
            elif self.datum_code.datum_code == "WGS84":
                datum = 4326
        else:
            datum = 4326
        geom = Point(x=self.longitude, y=self.latitude, srid=datum)
        geom.transform(4326)
        return geom


class TrtPersons(models.Model):
    person_id = models.AutoField(db_column='PERSON_ID', primary_key=True)  # Field name made lowercase.
    first_name = models.CharField(db_column='FIRST_NAME', max_length=50)  # Field name made lowercase.
    middle_name = models.CharField(db_column='MIDDLE_NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    surname = models.CharField(db_column='SURNAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    specialty = models.CharField(db_column='SPECIALTY', max_length=255, blank=True, null=True)  # Field name made lowercase.
    address_line_1 = models.CharField(db_column='ADDRESS_LINE_1', max_length=255, blank=True, null=True)  # Field name made lowercase.
    address_line_2 = models.CharField(db_column='ADDRESS_LINE_2', max_length=255, blank=True, null=True)  # Field name made lowercase.
    town = models.CharField(db_column='TOWN', max_length=50, blank=True, null=True)  # Field name made lowercase.
    state = models.CharField(db_column='STATE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    post_code = models.CharField(db_column='POST_CODE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    country = models.CharField(db_column='COUNTRY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    telephone = models.CharField(db_column='TELEPHONE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    fax = models.CharField(db_column='FAX', max_length=20, blank=True, null=True)  # Field name made lowercase.
    mobile = models.CharField(db_column='MOBILE', max_length=20, blank=True, null=True)  # Field name made lowercase.
    email = models.CharField(db_column='EMAIL', max_length=150, blank=True, null=True)  # Field name made lowercase.
    comments = models.CharField(db_column='COMMENTS', max_length=400, blank=True, null=True)  # Field name made lowercase.
    transfer = models.CharField(db_column='Transfer', max_length=50, blank=True, null=True)  # Field name made lowercase.
    recorder = models.BooleanField(db_column='Recorder')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_PERSONS'


class TrtPitTags(models.Model):
    pit_tag_id = models.CharField(db_column='PIT_TAG_ID', primary_key=True, max_length=50)  # Field name made lowercase.
    issue_location = models.CharField(db_column='ISSUE_LOCATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    custodian_person_id = models.IntegerField(db_column='CUSTODIAN_PERSON_ID', blank=True, null=True)  # Field name made lowercase.
    turtle = models.ForeignKey('TrtTurtles', models.DO_NOTHING, db_column='TURTLE_ID', related_name='pit_tags', blank=True, null=True)  # Field name made lowercase.
    pit_tag_status = models.CharField(db_column='PIT_TAG_STATUS', max_length=10, blank=True, null=True)  # Field name made lowercase.
    return_date = models.DateTimeField(db_column='RETURN_DATE', blank=True, null=True)  # Field name made lowercase.
    return_condition = models.CharField(db_column='RETURN_CONDITION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    comments = models.CharField(db_column='COMMENTS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    field_person_id = models.IntegerField(db_column='FIELD_PERSON_ID', blank=True, null=True)  # Field name made lowercase.
    tag_order_id = models.IntegerField(db_column='TAG_ORDER_ID', blank=True, null=True)  # Field name made lowercase.
    batch_number = models.CharField(db_column='BATCH_NUMBER', max_length=50, blank=True, null=True)  # Field name made lowercase.
    box_number = models.CharField(db_column='BOX_NUMBER', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_PIT_TAGS'
        unique_together = (('pit_tag_id', 'turtle'),)


class TrtPitTagStates(models.Model):
    pit_tag_state = models.CharField(db_column='PIT_TAG_STATE', primary_key=True, max_length=10)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=50)  # Field name made lowercase.
    pit_tag_status = models.ForeignKey('TrtPitTagStatus', models.DO_NOTHING, db_column='PIT_TAG_STATUS')  # Field name made lowercase.
    existing_tag_list = models.BooleanField(db_column='EXISTING_TAG_LIST')  # Field name made lowercase.
    new_tag_list = models.BooleanField(db_column='NEW_TAG_LIST')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_PIT_TAG_STATES'


class TrtPitTagStatus(models.Model):
    pit_tag_status = models.CharField(db_column='PIT_TAG_STATUS', primary_key=True, max_length=10)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_PIT_TAG_STATUS'


class TrtPlaces(models.Model):
    place_code = models.CharField(db_column='PLACE_CODE', primary_key=True, max_length=4)  # Field name made lowercase.
    place_name = models.CharField(db_column='PLACE_NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    location_code = models.ForeignKey('TrtLocations', models.DO_NOTHING, db_column='LOCATION_CODE', related_name='places')
    rookery = models.CharField(db_column='ROOKERY', max_length=1, blank=True, null=True)  # Field name made lowercase.
    beach_approach = models.CharField(db_column='BEACH_APPROACH', max_length=50, blank=True, null=True)  # Field name made lowercase.
    aspect = models.CharField(db_column='ASPECT', max_length=3, blank=True, null=True)  # Field name made lowercase.
    datum_code = models.CharField(db_column='DATUM_CODE', max_length=5, blank=True, null=True)  # Field name made lowercase.
    latitude = models.FloatField(db_column='LATITUDE', blank=True, null=True)  # Field name made lowercase.
    longitude = models.FloatField(db_column='LONGITUDE', blank=True, null=True)  # Field name made lowercase.
    comments = models.CharField(db_column='COMMENTS', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_PLACES'

    def __str__(self):
        if self.place_name:
            return f"{self.location_code.location_name} - {self.place_name}"
        else:
            return f"{self.location_code.location_name} - {self.place_code}"


class TrtRecordedIdentification(models.Model):
    recorded_identification_id = models.AutoField(db_column='RECORDED_IDENTIFICATION_ID', primary_key=True)  # Field name made lowercase.
    observation_id = models.IntegerField(db_column='OBSERVATION_ID')  # Field name made lowercase.
    turtle = models.ForeignKey(TrtIdentification, models.DO_NOTHING, db_column='TURTLE_ID')  # Field name made lowercase.
    comments = models.CharField(db_column='COMMENTS', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_RECORDED_IDENTIFICATION'


class TrtRecordedPitTags(models.Model):
    recorded_pit_tag_id = models.AutoField(db_column='RECORDED_PIT_TAG_ID', primary_key=True)  # Field name made lowercase.
    observation_id = models.IntegerField(db_column='OBSERVATION_ID')  # Field name made lowercase.
    pit_tag_id = models.CharField(db_column='PIT_TAG_ID', max_length=50)  # Field name made lowercase.
    pit_tag_state = models.ForeignKey(TrtPitTagStates, models.DO_NOTHING, db_column='PIT_TAG_STATE')  # Field name made lowercase.
    pit_tag_position = models.CharField(db_column='PIT_TAG_POSITION', max_length=10, blank=True, null=True)  # Field name made lowercase.
    comments = models.CharField(db_column='COMMENTS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    turtle_id = models.IntegerField(db_column='TURTLE_ID')  # Field name made lowercase.
    checked = models.BooleanField(db_column='Checked')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_RECORDED_PIT_TAGS'


class TrtRecordedTags(models.Model):
    recorded_tag_id = models.AutoField(db_column='RECORDED_TAG_ID', primary_key=True)  # Field name made lowercase.
    observation_id = models.IntegerField(db_column='OBSERVATION_ID')  # Field name made lowercase.
    tag_id = models.CharField(db_column='TAG_ID', max_length=10)  # Field name made lowercase.
    other_tag_id = models.CharField(db_column='OTHER_TAG_ID', max_length=10, blank=True, null=True)  # Field name made lowercase.
    side = models.CharField(db_column='SIDE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tag_state = models.CharField(db_column='TAG_STATE', max_length=10, blank=True, null=True)  # Field name made lowercase.
    comments = models.CharField(db_column='COMMENTS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    tag_position = models.SmallIntegerField(db_column='TAG_POSITION', blank=True, null=True)  # Field name made lowercase.
    barnacles = models.BooleanField(db_column='BARNACLES')  # Field name made lowercase.
    turtle_id = models.IntegerField(db_column='TURTLE_ID')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_RECORDED_TAGS'


class TrtSamples(models.Model):
    sample_id = models.AutoField(db_column='SAMPLE_ID', primary_key=True)  # Field name made lowercase.
    turtle = models.ForeignKey('TrtTurtles', models.DO_NOTHING, db_column='TURTLE_ID')  # Field name made lowercase.
    sample_date = models.DateTimeField(db_column='SAMPLE_DATE', blank=True, null=True)  # Field name made lowercase.
    tissue_type = models.ForeignKey('TrtTissueTypes', models.DO_NOTHING, db_column='TISSUE_TYPE')  # Field name made lowercase.
    arsenic = models.FloatField(db_column='ARSENIC', blank=True, null=True)  # Field name made lowercase.
    selenium = models.FloatField(db_column='SELENIUM', blank=True, null=True)  # Field name made lowercase.
    zinc = models.FloatField(db_column='ZINC', blank=True, null=True)  # Field name made lowercase.
    cadmium = models.FloatField(db_column='CADMIUM', blank=True, null=True)  # Field name made lowercase.
    copper = models.FloatField(db_column='COPPER', blank=True, null=True)  # Field name made lowercase.
    lead = models.FloatField(db_column='LEAD', blank=True, null=True)  # Field name made lowercase.
    mercury = models.FloatField(db_column='MERCURY', blank=True, null=True)  # Field name made lowercase.
    comments = models.CharField(db_column='COMMENTS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    observation_id = models.IntegerField(db_column='OBSERVATION_ID', blank=True, null=True)  # Field name made lowercase.
    sample_label = models.CharField(db_column='SAMPLE_LABEL', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_SAMPLES'


class TrtSighting(models.Model):
    sightingid = models.AutoField(db_column='SIGHTINGID', primary_key=True)  # Field name made lowercase.
    observation_time = models.DateTimeField(db_column='OBSERVATION_TIME', blank=True, null=True)  # Field name made lowercase.
    observation_date = models.DateTimeField(db_column='OBSERVATION_DATE', blank=True, null=True)  # Field name made lowercase.
    alive = models.CharField(db_column='ALIVE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    species_code = models.CharField(db_column='SPECIES_CODE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    sex = models.CharField(db_column='SEX', max_length=1, blank=True, null=True)  # Field name made lowercase.
    location_code = models.CharField(db_column='LOCATION_CODE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    turtle_status = models.CharField(db_column='TURTLE_STATUS', max_length=1, blank=True, null=True)  # Field name made lowercase.
    place_code = models.CharField(db_column='PLACE_CODE', max_length=4, blank=True, null=True)  # Field name made lowercase.
    activity_code = models.CharField(db_column='ACTIVITY_CODE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    beach_position_code = models.CharField(db_column='BEACH_POSITION_CODE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    datum_code = models.CharField(db_column='DATUM_CODE', max_length=5, blank=True, null=True)  # Field name made lowercase.
    latitude = models.CharField(db_column='LATITUDE', max_length=7, blank=True, null=True)  # Field name made lowercase.
    longitude = models.FloatField(db_column='LONGITUDE', blank=True, null=True)  # Field name made lowercase.
    comments = models.CharField(db_column='COMMENTS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    entered_by_person_id = models.IntegerField(db_column='ENTERED_BY_PERSON_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_SIGHTING'


class TrtSpecies(models.Model):
    species_code = models.CharField(db_column='SPECIES_CODE', primary_key=True, max_length=2)  # Field name made lowercase.
    scientific_name = models.CharField(db_column='SCIENTIFIC_NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    common_name = models.CharField(db_column='COMMON_NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.
    old_species_code = models.CharField(db_column='OLD_SPECIES_CODE', max_length=2, blank=True, null=True)  # Field name made lowercase.
    hide_dataentry = models.BooleanField(db_column='Hide_DataEntry')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_SPECIES'


class TrtTags(models.Model):
    tag_id = models.CharField(db_column='TAG_ID', primary_key=True, max_length=10)  # Field name made lowercase.
    tag_order_id = models.IntegerField(db_column='TAG_ORDER_ID', blank=True, null=True)  # Field name made lowercase.
    issue_location = models.CharField(db_column='ISSUE_LOCATION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    custodian_person_id = models.IntegerField(db_column='CUSTODIAN_PERSON_ID', blank=True, null=True)  # Field name made lowercase.
    turtle = models.ForeignKey('TrtTurtles', models.DO_NOTHING, db_column='TURTLE_ID', related_name='tags', blank=True, null=True)  # Field name made lowercase.
    side = models.CharField(db_column='SIDE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    tag_status = models.ForeignKey('TrtTagStatus', models.DO_NOTHING, db_column='TAG_STATUS', blank=True, null=True)  # Field name made lowercase.
    return_date = models.DateTimeField(db_column='RETURN_DATE', blank=True, null=True)  # Field name made lowercase.
    return_condition = models.CharField(db_column='RETURN_CONDITION', max_length=50, blank=True, null=True)  # Field name made lowercase.
    comments = models.CharField(db_column='COMMENTS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    field_person_id = models.IntegerField(db_column='FIELD_PERSON_ID', blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_TAGS'
        unique_together = (('tag_id', 'turtle'),)

    def __str__(self):
        return self.tag_id


class TrtTagOrders(models.Model):
    tag_order_id = models.AutoField(db_column='TAG_ORDER_ID', primary_key=True)  # Field name made lowercase.
    order_date = models.DateTimeField(db_column='ORDER_DATE', blank=True, null=True)  # Field name made lowercase.
    order_number = models.CharField(db_column='ORDER_NUMBER', max_length=20)  # Field name made lowercase.
    tag_prefix = models.CharField(db_column='TAG_PREFIX', max_length=10, blank=True, null=True)  # Field name made lowercase.
    start_tag_number = models.IntegerField(db_column='START_TAG_NUMBER', blank=True, null=True)  # Field name made lowercase.
    end_tag_number = models.IntegerField(db_column='END_TAG_NUMBER', blank=True, null=True)  # Field name made lowercase.
    total_tags = models.SmallIntegerField(db_column='TOTAL_TAGS', blank=True, null=True)  # Field name made lowercase.
    date_received = models.DateTimeField(db_column='DATE_RECEIVED', blank=True, null=True)  # Field name made lowercase.
    paid_by = models.CharField(db_column='PAID_BY', max_length=255, blank=True, null=True)  # Field name made lowercase.
    comments = models.CharField(db_column='COMMENTS', max_length=255, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_TAG_ORDERS'


class TrtTagStates(models.Model):
    tag_state = models.CharField(db_column='TAG_STATE', primary_key=True, max_length=10)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=50)  # Field name made lowercase.
    tag_status = models.CharField(db_column='TAG_STATUS', max_length=10, blank=True, null=True)  # Field name made lowercase.
    existing_tag_list = models.BooleanField(db_column='EXISTING_TAG_LIST')  # Field name made lowercase.
    new_tag_list = models.BooleanField(db_column='NEW_TAG_LIST')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_TAG_STATES'


class TrtTagStatus(models.Model):
    tag_status = models.CharField(db_column='TAG_STATUS', primary_key=True, max_length=10)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_TAG_STATUS'


class TrtTissueTypes(models.Model):
    tissue_type = models.CharField(db_column='TISSUE_TYPE', primary_key=True, max_length=5)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=50)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_TISSUE_TYPES'


class TrtTurtles(models.Model):
    turtle_id = models.IntegerField(db_column='TURTLE_ID', primary_key=True)  # Field name made lowercase.
    species_code = models.ForeignKey(TrtSpecies, models.DO_NOTHING, db_column='SPECIES_CODE')  # Field name made lowercase.
    identification_confidence = models.CharField(db_column='IDENTIFICATION_CONFIDENCE', max_length=1, blank=True, null=True)  # Field name made lowercase.
    sex = models.CharField(db_column='SEX', max_length=1)  # Field name made lowercase.
    turtle_status = models.ForeignKey('TrtTurtleStatus', models.DO_NOTHING, db_column='TURTLE_STATUS', blank=True, null=True)  # Field name made lowercase.
    location_code = models.ForeignKey(TrtLocations, models.DO_NOTHING, db_column='LOCATION_CODE', blank=True, null=True)  # Field name made lowercase.
    cause_of_death = models.ForeignKey(TrtCauseOfDeath, models.DO_NOTHING, db_column='CAUSE_OF_DEATH', blank=True, null=True)  # Field name made lowercase.
    re_entered_population = models.CharField(db_column='RE_ENTERED_POPULATION', max_length=1, blank=True, null=True)  # Field name made lowercase.
    comments = models.CharField(db_column='COMMENTS', max_length=255, blank=True, null=True)  # Field name made lowercase.
    entered_by = models.CharField(db_column='ENTERED_BY', max_length=50, blank=True, null=True)  # Field name made lowercase.
    date_entered = models.DateTimeField(db_column='DATE_ENTERED', blank=True, null=True)  # Field name made lowercase.
    original_turtle_id = models.IntegerField(db_column='ORIGINAL_TURTLE_ID', blank=True, null=True)  # Field name made lowercase.
    entry_batch_id = models.IntegerField(db_column='ENTRY_BATCH_ID', blank=True, null=True)  # Field name made lowercase.
    tag = models.CharField(db_column='Tag', max_length=255, blank=True, null=True)  # Field name made lowercase.
    mund_id = models.CharField(db_column='Mund_ID', max_length=255, blank=True, null=True)  # Field name made lowercase.
    turtle_name = models.CharField(db_column='TURTLE_NAME', max_length=50, blank=True, null=True)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_TURTLES'
        ordering = ('turtle_id',)

    def __str__(self):
        if self.turtle_name:
            return f'{self.turtle_id}: {self.species_code.common_name} ({self.sex}) - {self.turtle_name}'
        else:
            return f'{self.turtle_id}: {self.species_code.common_name} ({self.sex})'

    def get_absolute_url(self):
        return reverse('wamtram:turtle_detail', kwargs={'pk': self.pk})


class TrtTurtleStatus(models.Model):
    turtle_status = models.CharField(db_column='TURTLE_STATUS', primary_key=True, max_length=1)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=100)  # Field name made lowercase.
    new_tag_list = models.BooleanField(db_column='NEW_TAG_LIST')  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_TURTLE_STATUS'


class TrtYesNo(models.Model):
    code = models.CharField(db_column='CODE', primary_key=True, max_length=1)  # Field name made lowercase.
    description = models.CharField(db_column='DESCRIPTION', max_length=10)  # Field name made lowercase.

    class Meta:
        managed = False
        db_table = 'TRT_YES_NO'
