from crispy_forms.helper import FormHelper
from crispy_forms.layout import Layout, Fieldset, Field, Submit, Div, HTML
from crispy_forms.bootstrap import FormActions
from datetime import datetime
from django import forms
from django.conf import settings
from django.core.exceptions import ValidationError
from django_select2.forms import Select2Widget
from easy_select2 import Select2

from users.models import User
from .models import (
    TurtleSpecies,
    Place,
    Turtle,
    TurtleObservation,
    TurtleTag,
    TurtlePitTag,
    TurtleDamage,
    TurtleSample,
)


BODY_PART_CHOICES = (
    (None, ''),
    ('A', 'Carapace - entire'),
    ('B', 'Left front flipper'),
    ('C', 'Right front flipper'),
    ('D', 'Left rear flipper'),
    ('E', 'Right rear flipper'),
    ('H', 'Head'),
    ('I', 'Center mid-carapace'),
    ('J', 'Right front carapace'),
    ('K', 'Left front carapace'),
    ('L', 'Left rear carapace'),
    ('M', 'Right rear carapace'),
    ('N', 'Front mid-carapace'),
    ('O', 'Rear mid-carapace'),
    ('P', 'Plastron - entire'),
    ('T', 'Tail'),
    ('W', 'Whole animal'),
)
DAMAGE_CHOICES = (
    (None, ''),
    ('1', 'Tip off - flipper'),
    ('2', 'Lost from nail - flipper'),
    ('3', 'Lost half - flipper'),
    ('4', 'Lost whole - flipper'),
    ('5', 'Minor wounds or cuts'),
    ('6', 'Major wounds or cuts'),
    ('7', 'Deformity'),
)


class TurtleAddForm(forms.ModelForm):
    """A modified form to allow some additional recordkeeping on creation of new Turtle instances.
    """

    class Meta:
        model = Turtle
        fields = (
            'species',
            'sex',
            'name',
            'comments',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['species'].required = True


class TurtleChangeForm(forms.ModelForm):
    """A form to allow changes to existing Turtle instances.
    """
    class Meta:
        model = Turtle
        fields = (
            'species',
            'sex',
            'name',
            'cause_of_death',
            'comments',
        )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['species'].required = True


class TurtleObservationForm(forms.ModelForm):
    place = forms.ModelChoiceField(queryset=Place.objects.all(), widget=Select2())

    class Meta:
        model = TurtleObservation
        fields = '__all__'

    def clean_observed(self):
        observed = self.cleaned_data['observed']
        if observed >= datetime.now().astimezone(settings.AWST):
            raise ValidationError("Observations cannot be recorded in the future")
        return observed


class TurtleFlipperDamageForm(forms.ModelForm):
    FLIPPER_PART_CHOICES = (
        ('B', 'Left front flipper'),
        ('C', 'Right front flipper'),
        ('D', 'Left rear flipper'),
        ('E', 'Right rear flipper'),
    )
    FLIPPER_DAMAGE_CHOICES = (
        ('0', 'None significant'),
        ('1', 'Tip off'),
        ('2', 'Lost from Nail'),
        ('3', 'Lost half'),
        ('4', 'Lost whole'),
        ('7', 'Deformity'),
    )
    body_part = forms.ChoiceField(required=True, label='flipper', choices=FLIPPER_PART_CHOICES)
    damage = forms.ChoiceField(required=True, choices=FLIPPER_DAMAGE_CHOICES)

    class Meta:
        model = TurtleDamage
        fields = ('body_part', 'damage', 'comments')


class TurtleInjuryForm(forms.ModelForm):
    body_part = forms.ChoiceField(required=True, choices=BODY_PART_CHOICES)
    damage = forms.ChoiceField(required=True, choices=DAMAGE_CHOICES)

    class Meta:
        model = TurtleDamage
        fields = ('body_part', 'damage', 'comments')


class TurtleSampleForm(forms.ModelForm):

    class Meta:
        model = TurtleSample
        fields = ('tissue_type', 'label')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['label'].required = True


class TurtleTagForm(forms.ModelForm):

    class Meta:
        model = TurtleTag
        fields = ('serial', 'side', 'status', 'return_date', 'return_condition', 'comments')

    def clean_serial(self):
        """Only validate serial number uniqueness on creation of new tags.
        """
        serial = self.cleaned_data['serial'].strip()
        if not self.instance.pk:
            if TurtleTag.objects.filter(serial__iexact=serial).exists():
                existing_tag = TurtleTag.objects.get(serial__iexact=serial)
                if existing_tag.turtle:
                    raise ValidationError(f"Tag with serial {existing_tag.serial} already exists and is assigned to {existing_tag.turtle}")
                else:
                    raise ValidationError(f"Tag with serial {existing_tag.serial} already exists")
            return serial
        return serial


class TurtleTagAddForm(TurtleTagForm):
    """Override the normal form, to be used when creating a new turtle.
    """
    TAG_STATUS_CHOICES = (
        ('ATT', 'Tag attached to turtle'),
        ('POOR', 'Poor fix on turtle'),
    )
    status = forms.ChoiceField(required=True, choices=TAG_STATUS_CHOICES)

    class Meta(TurtleTagForm.Meta):
        fields = ('serial', 'side', 'status', 'comments')


class TurtlePitTagForm(forms.ModelForm):

    class Meta:
        model = TurtlePitTag
        fields = ('serial', 'status', 'return_date', 'return_condition', 'comments')

    def clean_serial(self):
        """Only validate serial number uniqueness on creation of new tags.
        """
        serial = self.cleaned_data['serial'].strip()
        if not self.instance.pk:
            if TurtlePitTag.objects.filter(serial__iexact=serial).exists():
                existing_tag = TurtlePitTag.objects.get(serial__iexact=serial)
                if existing_tag.turtle:
                    raise ValidationError(f"Pit tag with serial {existing_tag.serial} already exists and is assigned to {existing_tag.turtle}")
                else:
                    raise ValidationError(f"Pit tag with serial {existing_tag.serial} already exists")
        return serial


class TurtlePitTagAddForm(TurtlePitTagForm):
    """Override the normal form, to be used when creating a new turtle.
    """
    POSITION_CHOICES = (
        ('LF', 'Left front'),
        ('RF', 'Right front'),
        ('LR', 'Left rear'),
        ('RR', 'Right rear'),
    )
    PIT_TAG_STATUS_CHOICES = (
        ('ATT', 'Tag attached to turtle - Read OK'),
        ('POOR', 'Applied new - Did not read'),
    )
    status = forms.ChoiceField(required=True, choices=PIT_TAG_STATUS_CHOICES)
    position = forms.ChoiceField(required=False, choices=POSITION_CHOICES)

    class Meta(TurtlePitTagForm.Meta):
        fields = ('serial', 'status', 'position', 'comments')


class Row(Div):
    css_class = 'row'


class AjaxChoiceField(forms.ChoiceField):
    """An empty ChoiceField intended to be populated via an Ajax call.
    """
    def valid_value(self, value):
        '''Provided value is always a valid choice, even when no choices are defined.
        Reference: https://github.com/django/django/blob/main/django/forms/fields.py
        '''
        return True


class TurtleTagObservationAddForm(forms.Form):
    """A bespoke form that reproduces the paper turtle tagging datasheet(s).
    """
    SEX_CHOICES = (
        (None, ''),
        ('F', 'Female'),
        ('M', 'Male'),
        ('U', 'Unknown'),
    )
    CHECKED_CHOICES = (
        (None, ''),
        ('na', 'Did not check'),
        ('y', 'Yes'),
        ('n', 'No'),
    )
    YES_NO_CHOICES = (
        (None, ''),
        ('y', 'Yes'),
        ('n', 'No'),
    )
    SCALE_CHOICES = (
        (None, ''),
        ('1', '1'),
        ('2', '2'),
        ('3', '3'),
    )
    SAMPLE_TYPE_CHOICES = [(None, '')] + list(TurtleSample.TISSUE_TYPE_CHOICES)
    NEST_INTERRUPT_CHOICES = [
        (None, ''),
    ] + list(TurtleObservation.NEST_INTERRUPT_CHOICES)
    NESTED_CHOICES = [
        (None, ''),
    ] + list(TurtleObservation.NESTED_CHOICES)

    existing_turtle_id = forms.IntegerField(initial=0, widget=forms.HiddenInput)
    place = forms.ModelChoiceField(Place.objects.all(), label='Location/beach', widget=Select2Widget)
    latitude = forms.FloatField(required=False, help_text='WGS 84')
    longitude = forms.FloatField(required=False, help_text='WGS 84')
    species = forms.ModelChoiceField(TurtleSpecies.objects.all())
    observed = forms.DateTimeField(label='Calendar date & time', input_formats=settings.DATETIME_INPUT_FORMATS, help_text='AWST')
    sex = forms.ChoiceField(choices=SEX_CHOICES)
    recorded_by = AjaxChoiceField(label='Data captured by', help_text='User who recorded the survey data in the field')
    data_sheet = forms.FileField(required=False, help_text='Electronic copy of the field survey data sheet')

    flipper_tags_present = forms.ChoiceField(choices=CHECKED_CHOICES, help_text='Does this turtle have flipper tags present?')
    tag_l1 = AjaxChoiceField(required=False)
    tag_l1_new = forms.ChoiceField(choices=YES_NO_CHOICES, required=False)
    tag_l1_barnacles = forms.ChoiceField(choices=YES_NO_CHOICES, required=False)
    tag_l1_secure = forms.ChoiceField(choices=YES_NO_CHOICES, required=False)
    tag_l1_scars = forms.ChoiceField(choices=YES_NO_CHOICES, required=False)
    tag_l2 = AjaxChoiceField(required=False)
    tag_l2_new = forms.ChoiceField(choices=YES_NO_CHOICES, required=False)
    tag_l2_barnacles = forms.ChoiceField(choices=YES_NO_CHOICES, required=False)
    tag_l2_secure = forms.ChoiceField(choices=YES_NO_CHOICES, required=False)
    tag_l2_scars = forms.ChoiceField(choices=YES_NO_CHOICES, required=False)
    tag_l3 = AjaxChoiceField(required=False)
    tag_l3_new = forms.ChoiceField(choices=YES_NO_CHOICES, required=False)
    tag_l3_barnacles = forms.ChoiceField(choices=YES_NO_CHOICES, required=False)
    tag_l3_secure = forms.ChoiceField(choices=YES_NO_CHOICES, required=False)
    tag_l3_scars = forms.ChoiceField(choices=YES_NO_CHOICES, required=False)

    tag_r1 = AjaxChoiceField(required=False)
    tag_r1_new = forms.ChoiceField(choices=YES_NO_CHOICES, required=False)
    tag_r1_barnacles = forms.ChoiceField(choices=YES_NO_CHOICES, required=False)
    tag_r1_secure = forms.ChoiceField(choices=YES_NO_CHOICES, required=False)
    tag_r1_scars = forms.ChoiceField(choices=YES_NO_CHOICES, required=False)
    tag_r2 = AjaxChoiceField(required=False)
    tag_r2_new = forms.ChoiceField(choices=YES_NO_CHOICES, required=False)
    tag_r2_barnacles = forms.ChoiceField(choices=YES_NO_CHOICES, required=False)
    tag_r2_secure = forms.ChoiceField(choices=YES_NO_CHOICES, required=False)
    tag_r2_scars = forms.ChoiceField(choices=YES_NO_CHOICES, required=False)
    tag_r3 = AjaxChoiceField(required=False)
    tag_r3_new = forms.ChoiceField(choices=YES_NO_CHOICES, required=False)
    tag_r3_barnacles = forms.ChoiceField(choices=YES_NO_CHOICES, required=False)
    tag_r3_secure = forms.ChoiceField(choices=YES_NO_CHOICES, required=False)
    tag_r3_scars = forms.ChoiceField(choices=YES_NO_CHOICES, required=False)

    pit_tags_present = forms.ChoiceField(choices=CHECKED_CHOICES, help_text='Does this turtle have any pit tags present?')
    pit_tag_l = AjaxChoiceField(required=False)
    pit_tag_l_new = forms.ChoiceField(choices=YES_NO_CHOICES, required=False)
    pit_tag_r = AjaxChoiceField(required=False)
    pit_tag_r_new = forms.ChoiceField(choices=YES_NO_CHOICES, required=False)

    tagged_by = AjaxChoiceField(required=False)

    ccl_min = forms.IntegerField(required=False, label='CCL min (mm)')
    ccl_max = forms.IntegerField(required=False, label='CCL max (mm)')
    cc_width = forms.IntegerField(required=False, label='CC width (mm)')
    weight = forms.FloatField(required=False, label='Weight (kg)')
    measured_by = AjaxChoiceField(required=False)

    nesting_interrupted = forms.ChoiceField(label='Was the nesting process interruped?', choices=YES_NO_CHOICES, required=False)
    nesting_interruption_cause = forms.ChoiceField(choices=NEST_INTERRUPT_CHOICES, required=False)
    nested = forms.ChoiceField(label='Did the turtle lay?', choices=NESTED_CHOICES, required=False)
    egg_count = forms.IntegerField(required=False)

    damage = forms.ChoiceField(choices=CHECKED_CHOICES, help_text='Does this turtle have damage/distinguishing features?')
    damage_1_part = forms.ChoiceField(choices=BODY_PART_CHOICES, required=False)
    damage_1_type = forms.ChoiceField(choices=DAMAGE_CHOICES, required=False)
    damage_2_part = forms.ChoiceField(choices=BODY_PART_CHOICES, required=False)
    damage_2_type = forms.ChoiceField(choices=DAMAGE_CHOICES, required=False)
    damage_3_part = forms.ChoiceField(choices=BODY_PART_CHOICES, required=False)
    damage_3_type = forms.ChoiceField(choices=DAMAGE_CHOICES, required=False)
    damage_4_part = forms.ChoiceField(choices=BODY_PART_CHOICES, required=False)
    damage_4_type = forms.ChoiceField(choices=DAMAGE_CHOICES, required=False)
    damage_5_part = forms.ChoiceField(choices=BODY_PART_CHOICES, required=False)
    damage_5_type = forms.ChoiceField(choices=DAMAGE_CHOICES, required=False)

    biopsy_no = forms.CharField(required=False)
    photos = forms.ChoiceField(choices=YES_NO_CHOICES, required=False)
    sample_1_type = forms.ChoiceField(choices=SAMPLE_TYPE_CHOICES, required=False)
    sample_1_label = forms.CharField(required=False)
    sample_1_taken_by = forms.CharField(required=False)
    sample_2_type = forms.ChoiceField(choices=SAMPLE_TYPE_CHOICES, required=False)
    sample_2_label = forms.CharField(required=False)
    sample_2_taken_by = forms.CharField(required=False)
    comments = forms.CharField(widget=forms.Textarea, required=False)

    save_button = Submit('save', 'Save', css_class='btn-lg')
    save_flag_button = Submit('save-flag', 'Save and flag for curation', css_class='btn-warning')
    cancel_button = Submit('cancel', 'Cancel', css_class='btn-secondary')

    def __init__(self, *args, **kwargs):
        if "turtle_id" in kwargs:
            turtle_id = kwargs.pop("turtle_id")
        else:
            turtle_id = None
        super().__init__(*args, **kwargs)

        # Rigmarole to preserve any data input to user choice fields across form reloads.
        # Set the form field choice to be the previously-selected values.
        if 'data' in kwargs:
            if kwargs['data'].get('recorded_by', None):
                user = User.objects.get(pk=kwargs['data']['recorded_by'])
                self.fields['recorded_by'].choices = [(user.pk, user.name)]
            if kwargs['data'].get('tagged_by', None):
                user = User.objects.get(pk=kwargs['data']['tagged_by'])
                self.fields['tagged_by'].choices = [(user.pk, user.name)]
            if kwargs['data'].get('measured_by', None):
                user = User.objects.get(pk=kwargs['data']['measured_by'])
                self.fields['measured_by'].choices = [(user.pk, user.name)]
            if kwargs['data'].get('tag_l1', None):
                tag = TurtleTag.objects.get(pk=kwargs['data']['tag_l1'])
                self.fields['tag_l1'].choices = [(tag.pk, tag.serial)]
            if kwargs['data'].get('tag_l2', None):
                tag = TurtleTag.objects.get(pk=kwargs['data']['tag_l2'])
                self.fields['tag_l2'].choices = [(tag.pk, tag.serial)]
            if kwargs['data'].get('tag_l3', None):
                tag = TurtleTag.objects.get(pk=kwargs['data']['tag_l3'])
                self.fields['tag_l3'].choices = [(tag.pk, tag.serial)]
            if kwargs['data'].get('tag_r1', None):
                tag = TurtleTag.objects.get(pk=kwargs['data']['tag_r1'])
                self.fields['tag_r1'].choices = [(tag.pk, tag.serial)]
            if kwargs['data'].get('tag_r2', None):
                tag = TurtleTag.objects.get(pk=kwargs['data']['tag_r2'])
                self.fields['tag_r2'].choices = [(tag.pk, tag.serial)]
            if kwargs['data'].get('tag_r3', None):
                tag = TurtleTag.objects.get(pk=kwargs['data']['tag_r3'])
                self.fields['tag_r3'].choices = [(tag.pk, tag.serial)]
            if kwargs['data'].get('pit_tag_l', None):
                tag = TurtlePitTag.objects.get(pk=kwargs['data']['pit_tag_l'])
                self.fields['pit_tag_l'].choices = [(tag.pk, tag.serial)]
            if kwargs['data'].get('pit_tag_r', None):
                tag = TurtlePitTag.objects.get(pk=kwargs['data']['pit_tag_r'])
                self.fields['pit_tag_r'].choices = [(tag.pk, tag.serial)]

        self.helper = FormHelper()
        self.helper.form_method = 'POST'
        self.helper.attrs = {'novalidate': ''}  # Disable default in-browser form validation.

        # Add some additional classes to widget, for JavaScript purposes.
        self.fields['recorded_by'].widget.attrs['class'] = 'select-user-choice'
        self.fields['tagged_by'].widget.attrs['class'] = 'select-user-choice'
        self.fields['measured_by'].widget.attrs['class'] = 'select-user-choice'
        self.fields['tag_l1'].widget.attrs['class'] = 'select-tag-choice'
        self.fields['tag_l2'].widget.attrs['class'] = 'select-tag-choice'
        self.fields['tag_l3'].widget.attrs['class'] = 'select-tag-choice'
        self.fields['tag_r1'].widget.attrs['class'] = 'select-tag-choice'
        self.fields['tag_r2'].widget.attrs['class'] = 'select-tag-choice'
        self.fields['tag_r3'].widget.attrs['class'] = 'select-tag-choice'
        self.fields['pit_tag_l'].widget.attrs['class'] = 'select-pittag-choice'
        self.fields['pit_tag_r'].widget.attrs['class'] = 'select-pittag-choice'

        if turtle_id:
            self.fields['species'].disabled = True
            self.fields['sex'].disabled = True
        self.fields['data_sheet'].max_length = 220  # Allow 35 characters for the filepath

        # Remove labels from some fields
        self.fields['tag_l1'].label = False
        self.fields['tag_l1_new'].label = False
        self.fields['tag_l1_barnacles'].label = False
        self.fields['tag_l1_secure'].label = False
        self.fields['tag_l1_scars'].label = False
        self.fields['tag_l2'].label = False
        self.fields['tag_l2_new'].label = False
        self.fields['tag_l2_barnacles'].label = False
        self.fields['tag_l2_secure'].label = False
        self.fields['tag_l2_scars'].label = False
        self.fields['tag_l3'].label = False
        self.fields['tag_l3_new'].label = False
        self.fields['tag_l3_barnacles'].label = False
        self.fields['tag_l3_secure'].label = False
        self.fields['tag_l3_scars'].label = False
        self.fields['tag_r1'].label = False
        self.fields['tag_r1_new'].label = False
        self.fields['tag_r1_barnacles'].label = False
        self.fields['tag_r1_secure'].label = False
        self.fields['tag_r1_scars'].label = False
        self.fields['tag_r2'].label = False
        self.fields['tag_r2_new'].label = False
        self.fields['tag_r2_barnacles'].label = False
        self.fields['tag_r2_secure'].label = False
        self.fields['tag_r2_scars'].label = False
        self.fields['tag_r3'].label = False
        self.fields['tag_r3_new'].label = False
        self.fields['tag_r3_barnacles'].label = False
        self.fields['tag_r3_secure'].label = False
        self.fields['tag_r3_scars'].label = False
        self.fields['pit_tag_l'].label = False
        self.fields['pit_tag_l_new'].label = False
        self.fields['pit_tag_r'].label = False
        self.fields['pit_tag_r_new'].label = False
        self.fields['damage_1_part'].label = False
        self.fields['damage_1_type'].label = False
        self.fields['damage_2_part'].label = False
        self.fields['damage_2_type'].label = False
        self.fields['damage_3_part'].label = False
        self.fields['damage_3_type'].label = False
        self.fields['damage_4_part'].label = False
        self.fields['damage_4_type'].label = False
        self.fields['damage_5_part'].label = False
        self.fields['damage_5_type'].label = False

        # Form layout
        self.helper.layout = Layout(
            'existing_turtle_id',

            Fieldset(
                None,
                Row(
                    Field('place', wrapper_class='form-group col-8'),
                    Field('species', wrapper_class='form-group col-4'),
                ),
                Row(
                    Field('latitude', wrapper_class='form-group col-4'),
                    Field('longitude', wrapper_class='form-group col-4'),
                    Field('sex', wrapper_class='form-group col-4'),
                ),
                Row(
                    Field('observed', wrapper_class='form-group col-4'),
                    Field('recorded_by', wrapper_class='form-group col-4'),
                ),
                Row(
                    Field('data_sheet', wrapper_class='form-group col'),
                ),
                css_class='border px-2',
            ),

            HTML('<div class="my-3"><h5>Tags</h5></div>'),
            Fieldset(
                None,
                Row(
                    Field('flipper_tags_present', wrapper_class='form-group col-3'),
                ),
                Row(
                    HTML('<div class="col-2"></div>'),
                    HTML('<div class="col-5">Tag number</div>'),
                    HTML('<div class="col">New tag?</div>'),
                    HTML('<div class="col">Barnacles?</div>'),
                    HTML('<div class="col">Securely fixed?</div>'),
                    HTML('<div class="col">Tag scars?</div>'),
                    css_class='pb-2',
                ),
                Row(
                    HTML('<div class="col-2">Left scale 1</div>'),
                    Field('tag_l1', wrapper_class='form-group col-5'),
                    Field('tag_l1_new', wrapper_class='form-group col'),
                    Field('tag_l1_barnacles', wrapper_class='form-group col'),
                    Field('tag_l1_secure', wrapper_class='form-group col'),
                    Field('tag_l1_scars', wrapper_class='form-group col'),
                ),
                Row(
                    HTML('<div class="col-2">Left scale 2</div>'),
                    Field('tag_l2', wrapper_class='form-group col-5'),
                    Field('tag_l2_new', wrapper_class='form-group col'),
                    Field('tag_l2_barnacles', wrapper_class='form-group col'),
                    Field('tag_l2_secure', wrapper_class='form-group col'),
                    Field('tag_l2_scars', wrapper_class='form-group col'),
                ),
                Row(
                    HTML('<div class="col-2">Left scale 3</div>'),
                    Field('tag_l3', wrapper_class='form-group col-5'),
                    Field('tag_l3_new', wrapper_class='form-group col'),
                    Field('tag_l3_barnacles', wrapper_class='form-group col'),
                    Field('tag_l3_secure', wrapper_class='form-group col'),
                    Field('tag_l3_scars', wrapper_class='form-group col'),
                ),
                Row(
                    HTML('<div class="col-2">Right scale 1</div>'),
                    Field('tag_r1', wrapper_class='form-group col-5'),
                    Field('tag_r1_new', wrapper_class='form-group col'),
                    Field('tag_r1_barnacles', wrapper_class='form-group col'),
                    Field('tag_r1_secure', wrapper_class='form-group col'),
                    Field('tag_r1_scars', wrapper_class='form-group col'),
                ),
                Row(
                    HTML('<div class="col-2">Right scale 2</div>'),
                    Field('tag_r2', wrapper_class='form-group col-5'),
                    Field('tag_r2_new', wrapper_class='form-group col'),
                    Field('tag_r2_barnacles', wrapper_class='form-group col'),
                    Field('tag_r2_secure', wrapper_class='form-group col'),
                    Field('tag_r2_scars', wrapper_class='form-group col'),
                ),
                Row(
                    HTML('<div class="col-2">Right scale 3</div>'),
                    Field('tag_r3', wrapper_class='form-group col-5'),
                    Field('tag_r3_new', wrapper_class='form-group col'),
                    Field('tag_r3_barnacles', wrapper_class='form-group col'),
                    Field('tag_r3_secure', wrapper_class='form-group col'),
                    Field('tag_r3_scars', wrapper_class='form-group col'),
                ),
                Row(
                    Field('pit_tags_present', wrapper_class='form-group col-3'),
                ),
                Row(
                    HTML('<div class="col-1"></div>'),
                    HTML('<div class="col-9">Pit tag number</div>'),
                    HTML('<div class="col-2">New tag?</div>'),
                    css_class='pb-2',
                ),
                Row(
                    HTML('<div class="col-1">LEFT</div>'),
                    Field('pit_tag_l', wrapper_class='form-group col-9'),
                    Field('pit_tag_l_new', wrapper_class='form-group col-2'),
                ),
                Row(
                    HTML('<div class="col-1">RIGHT</div>'),
                    Field('pit_tag_r', wrapper_class='form-group col-9'),
                    Field('pit_tag_r_new', wrapper_class='form-group col-2'),
                ),
                Row(
                    Field('tagged_by', wrapper_class='form-group col-4'),
                ),
                css_class='border px-2',
            ),

            HTML('<div class="my-3"><h5>Measurements</h5></div>'),
            Fieldset(
                None,
                Row(
                    Field('ccl_min', wrapper_class='form-group col-4'),
                    Field('ccl_max', wrapper_class='form-group col-4'),
                    Field('measured_by', wrapper_class='form-group col-4'),
                ),
                Row(
                    Field('cc_width', wrapper_class='form-group col-4'),
                    Field('weight', wrapper_class='form-group col-4'),
                ),
                css_class='border px-2',
            ),

            HTML('<div class="my-3"><h5>Nesting</h5></div>'),
            Fieldset(
                None,
                Row(
                    Field('nesting_interrupted', wrapper_class='form-group col-6'),
                    Field('nesting_interruption_cause', wrapper_class='form-group col-6'),
                ),
                Row(
                    Field('nested', wrapper_class='form-group col-6'),
                    Field('egg_count', wrapper_class='form-group col-2'),
                ),
                css_class='border px-2',
            ),

            HTML('<div class="my-3"><h5>Damage</h5></div>'),
            Fieldset(
                None,
                Row(
                    Field('damage', wrapper_class='form-group col-6'),
                ),
                Row(
                    HTML('<div class="col-2"></div>'),
                    HTML('<div class="col-4">Body part</div>'),
                    HTML('<div class="col-4">Damage</div>'),
                    css_class='pb-2',
                ),
                Row(
                    HTML('<div class="col-2">Feature 1</div>'),
                    Field('damage_1_part', wrapper_class='form-group col-4'),
                    Field('damage_1_type', wrapper_class='form-group col-4'),
                ),
                Row(
                    HTML('<div class="col-2">Feature 2</div>'),
                    Field('damage_2_part', wrapper_class='form-group col-4'),
                    Field('damage_2_type', wrapper_class='form-group col-4'),
                ),
                Row(
                    HTML('<div class="col-2">Feature 3</div>'),
                    Field('damage_3_part', wrapper_class='form-group col-4'),
                    Field('damage_3_type', wrapper_class='form-group col-4'),
                ),
                Row(
                    HTML('<div class="col-2">Feature 4</div>'),
                    Field('damage_4_part', wrapper_class='form-group col-4'),
                    Field('damage_4_type', wrapper_class='form-group col-4'),
                ),
                Row(
                    HTML('<div class="col-2">Feature 5</div>'),
                    Field('damage_5_part', wrapper_class='form-group col-4'),
                    Field('damage_5_type', wrapper_class='form-group col-4'),
                ),
                css_class='border px-2',
            ),

            HTML('<div class="my-3"><h5>Samples</h5></div>'),
            Fieldset(
                None,
                Row(
                    Field('biopsy_no', wrapper_class='form-group col-4'),
                    Field('photos', wrapper_class='form-group col-4')
                ),
                Row(
                    Field('sample_1_type', wrapper_class='form-group col-4'),
                    Field('sample_1_label', wrapper_class='form-group col-4'),
                    Field('sample_1_taken_by', wrapper_class='form-group col-4'),
                ),
                Row(
                    Field('sample_2_type', wrapper_class='form-group col-4'),
                    Field('sample_2_label', wrapper_class='form-group col-4'),
                    Field('sample_2_taken_by', wrapper_class='form-group col-4'),
                ),
                css_class='border px-2',
            ),
            Row(
                Field('comments', wrapper_class='form-group col'),
            ),
            Div(
                HTML('<p>Where issues or questions exist relating to this observation, please record any relevant comments and select "Save and flag for curation".</p>'),
            ),

            FormActions(
                self.save_button,
                self.save_flag_button,
                self.cancel_button,
            ),
        )

    def clean_longitude(self):
        longitude = self.cleaned_data['longitude']
        # Western Australia bounds
        if longitude and (longitude > 130.0 or longitude < 108.0):
            raise ValidationError("Invalid longitude value")
        return longitude

    def clean_latitude(self):
        latitude = self.cleaned_data['latitude']
        # Western Australia bounds
        if latitude and (latitude > -10.0 or latitude < -42.0):
            raise ValidationError("Invalid latitude value")
        return latitude

    def clean_observed(self):
        observed = self.cleaned_data['observed']
        if observed >= datetime.now().astimezone(settings.AWST):
            raise ValidationError("Observations cannot be recorded in the future")
        return observed

    def clean_tag_l1(self):
        tag_l1 = self.cleaned_data['tag_l1']
        if tag_l1:
            tag = TurtleTag.objects.get(pk=tag_l1)
            if self.cleaned_data['existing_turtle_id']:
                existing_turtle = Turtle.objects.get(pk=self.cleaned_data.get('existing_turtle_id'))
            else:
                existing_turtle = None
            if (existing_turtle and tag.turtle and tag.turtle != existing_turtle) or (not existing_turtle and tag.turtle):
                self.add_error('tag_l1', f'Tag {tag.serial} is already assigned to turtle {tag.turtle}')
        return tag_l1

    def clean_tag_l1_new(self):
        # Note that this works because the tag_l1 field is cleaned prior.
        if self.cleaned_data['tag_l1'] and not self.cleaned_data['tag_l1_new']:
            raise ValidationError('You must record whether this tag is new or not')
        return self.cleaned_data['tag_l1']

    def clean_tag_l2(self):
        tag_l2 = self.cleaned_data['tag_l2']
        if tag_l2:
            tag = TurtleTag.objects.get(pk=tag_l2)
            if self.cleaned_data['existing_turtle_id']:
                existing_turtle = Turtle.objects.get(pk=self.cleaned_data.get('existing_turtle_id'))
            else:
                existing_turtle = None
            if (existing_turtle and tag.turtle and tag.turtle != existing_turtle) or (not existing_turtle and tag.turtle):
                self.add_error('tag_l2', f'Tag {tag.serial} is already assigned to turtle {tag.turtle}')
        return tag_l2

    def clean_tag_l2_new(self):
        # Note that this works because the tag_l2 field is cleaned prior.
        if self.cleaned_data['tag_l2'] and not self.cleaned_data['tag_l2_new']:
            raise ValidationError('You must record whether this tag is new or not')
        return self.cleaned_data['tag_l2']

    def clean_tag_l3(self):
        tag_l3 = self.cleaned_data['tag_l3']
        if tag_l3:
            tag = TurtleTag.objects.get(pk=tag_l3)
            if self.cleaned_data['existing_turtle_id']:
                existing_turtle = Turtle.objects.get(pk=self.cleaned_data.get('existing_turtle_id'))
            else:
                existing_turtle = None
            if (existing_turtle and tag.turtle and tag.turtle != existing_turtle) or (not existing_turtle and tag.turtle):
                self.add_error('tag_l3', f'Tag {tag.serial} is already assigned to turtle {tag.turtle}')
        return tag_l3

    def clean_tag_l3_new(self):
        # Note that this works because the tag_l3 field is cleaned prior.
        if self.cleaned_data['tag_l3'] and not self.cleaned_data['tag_l3_new']:
            raise ValidationError('You must record whether this tag is new or not')
        return self.cleaned_data['tag_l3']

    def clean_tag_r1(self):
        tag_r1 = self.cleaned_data['tag_r1']
        if tag_r1:
            tag = TurtleTag.objects.get(pk=tag_r1)
            if self.cleaned_data['existing_turtle_id']:
                existing_turtle = Turtle.objects.get(pk=self.cleaned_data.get('existing_turtle_id'))
            else:
                existing_turtle = None
            if (existing_turtle and tag.turtle and tag.turtle != existing_turtle) or (not existing_turtle and tag.turtle):
                self.add_error('tag_r1', f'Tag {tag.serial} is already assigned to turtle {tag.turtle}')
        return tag_r1

    def clean_tag_r1_new(self):
        # Note that this works because the tag_r1 field is cleaned prior.
        if self.cleaned_data['tag_r1'] and not self.cleaned_data['tag_r1_new']:
            raise ValidationError('You must record whether this tag is new or not')
        return self.cleaned_data['tag_r1']

    def clean_tag_r2(self):
        tag_r2 = self.cleaned_data['tag_r2']
        if tag_r2:
            tag = TurtleTag.objects.get(pk=tag_r2)
            if self.cleaned_data['existing_turtle_id']:
                existing_turtle = Turtle.objects.get(pk=self.cleaned_data.get('existing_turtle_id'))
            else:
                existing_turtle = None
            if (existing_turtle and tag.turtle and tag.turtle != existing_turtle) or (not existing_turtle and tag.turtle):
                self.add_error('tag_r2', f'Tag {tag.serial} is already assigned to turtle {tag.turtle}')
        return tag_r2

    def clean_tag_r2_new(self):
        # Note that this works because the tag_r2 field is cleaned prior.
        if self.cleaned_data['tag_r2'] and not self.cleaned_data['tag_r2_new']:
            raise ValidationError('You must record whether this tag is new or not')
        return self.cleaned_data['tag_r2']

    def clean_tag_r3(self):
        tag_r3 = self.cleaned_data['tag_r3']
        if tag_r3:
            tag = TurtleTag.objects.get(pk=tag_r3)
            if self.cleaned_data['existing_turtle_id']:
                existing_turtle = Turtle.objects.get(pk=self.cleaned_data.get('existing_turtle_id'))
            else:
                existing_turtle = None
            if (existing_turtle and tag.turtle and tag.turtle != existing_turtle) or (not existing_turtle and tag.turtle):
                self.add_error('tag_r3', f'Tag {tag.serial} is already assigned to turtle {tag.turtle}')
        return tag_r3

    def clean_tag_r3_new(self):
        # Note that this works because the tag_r3 field is cleaned prior.
        if self.cleaned_data['tag_r3'] and not self.cleaned_data['tag_r3_new']:
            raise ValidationError('You must record whether this tag is new or not')
        return self.cleaned_data['tag_r3']

    def clean_pit_tag_l(self):
        pit_tag_l = self.cleaned_data['pit_tag_l']
        if pit_tag_l:
            tag = TurtlePitTag.objects.get(pk=pit_tag_l)
            if self.cleaned_data['existing_turtle_id']:
                existing_turtle = Turtle.objects.get(pk=self.cleaned_data.get('existing_turtle_id'))
            else:
                existing_turtle = None
            if (existing_turtle and tag.turtle and tag.turtle != existing_turtle) or (not existing_turtle and tag.turtle):
                self.add_error('pit_tag_l', f'Pit tag {tag.serial} is already assigned to turtle {tag.turtle}')
        return pit_tag_l

    def clean_pit_tag_l_new(self):
        # Note that this works because the pit_tag_l field is cleaned prior.
        if self.cleaned_data['pit_tag_l'] and not self.cleaned_data['pit_tag_l_new']:
            raise ValidationError('You must record whether this tag is new or not')
        return self.cleaned_data['pit_tag_l']

    def clean_pit_tag_r(self):
        pit_tag_r = self.cleaned_data['pit_tag_r']
        if pit_tag_r:
            tag = TurtlePitTag.objects.get(pk=pit_tag_r)
            if self.cleaned_data['existing_turtle_id']:
                existing_turtle = Turtle.objects.get(pk=self.cleaned_data.get('existing_turtle_id'))
            else:
                existing_turtle = None
            if (existing_turtle and tag.turtle and tag.turtle != existing_turtle) or (not existing_turtle and tag.turtle):
                self.add_error('pit_tag_r', f'Pit tag {tag.serial} is already assigned to turtle {tag.turtle}')
        return pit_tag_r

    def clean_pit_tag_r_new(self):
        # Note that this works because the pit_tag_r field is cleaned prior.
        if self.cleaned_data['pit_tag_r'] and not self.cleaned_data['pit_tag_r_new']:
            raise ValidationError('You must record whether this tag is new or not')
        return self.cleaned_data['pit_tag_r']
