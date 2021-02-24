# -*- coding: utf-8 -*-
"""wastd.observations view test suite testing URLs, templates, and views."""
from __future__ import unicode_literals

from django.utils import timezone  # noqa

from django.contrib.auth import get_user_model
from django.contrib.gis.geos import GEOSGeometry
from django.test import TestCase
from django.urls import reverse  # noqa
from model_mommy import mommy  # noqa
from mommy_spatial_generators import MOMMY_SPATIAL_FIELDS  # noqa

from wastd.observations.models import (  # noqa
    NA,
    TAXON_CHOICES_DEFAULT,
    AnimalEncounter,
    Area,
    DispatchRecord,
    DugongMorphometricObservation,
    Encounter,
    Expedition,
    FieldMediaAttachment,
    HatchlingMorphometricObservation,
    LineTransectEncounter,
    LoggerEncounter,
    ManagementAction,
    MediaAttachment,
    NestTagObservation,
    SiteVisit,
    Survey,
    TagObservation,
    TemperatureLoggerDeployment,
    TemperatureLoggerSettings,
    TrackTallyObservation,
    TurtleDamageObservation,
    TurtleMorphometricObservation,
    TurtleNestDisturbanceObservation,
    TurtleNestDisturbanceTallyObservation,
    TurtleNestEncounter,
    TurtleNestObservation,
    PathToSea,
    TurtleHatchlingEmergenceObservation,
    TurtleHatchlingEmergenceOutlierObservation,
    LightSourceObservation,
    LoggerObservation
)

class EncounterViewTests(TestCase):
    """Encounter view tests."""

    def setUp(self):
        """Setup: create a new list."""
        self.user = get_user_model().objects.create_superuser(
            username="superuser",
            email="super@gmail.com",
            password="test")
        self.cl = Encounter.objects.create(
            where=GEOSGeometry('POINT (115 -32)', srid=4326),
            when=timezone.now(),
            source_id='12345',
            observer=self.user,
            reporter=self.user
        )
        self.user.save()
        self.client.force_login(self.user)

    def test_absolute_admin_url(self):
        """Test absolute admin url."""
        response = self.client.get(self.cl.absolute_admin_url)
        self.assertEqual(response.status_code, 200)

    def test_absolute_url(self):
        """Test absolute url."""
        response = self.client.get(self.cl.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def encounter_list_loads(self):
        """Test "encounter_list" view."""
        response = self.client.get(reverse("encounter_list"))
        self.assertEqual(response.status_code, 200)

    def encounter_list_loads(self):
        """Test "observations:animalencounter-list" view."""
        response = self.client.get(reverse("observations:encounter-list"))
        self.assertEqual(response.status_code, 200)

    def encounter_detail_loads(self):
        """Test "observations:animalencounter-detail" view."""
        response = self.client.get(reverse("observations:encounter-detail", pk=self.cl.pk))
        self.assertEqual(response.status_code, 200)



class AnimalEncounterViewTests(TestCase):
    """AnimalEncounter view tests."""

    def setUp(self):
        """Setup: create a new list."""
        self.user = get_user_model().objects.create_superuser(
            username="superuser",
            email="super@gmail.com",
            password="test")
        self.cl = AnimalEncounter.objects.create(
            where=GEOSGeometry('POINT (115 -32)', srid=4326),
            when=timezone.now(),
            taxon=TAXON_CHOICES_DEFAULT,
            species=NA,
            source_id='12345',
            observer=self.user,
            reporter=self.user
        )
        self.user.save()
        self.client.force_login(self.user)

    def test_absolute_admin_url(self):
        """Test absolute admin url."""
        response = self.client.get(self.cl.absolute_admin_url)
        self.assertEqual(response.status_code, 200)

    def test_absolute_url(self):
        """Test absolute url."""
        response = self.client.get(self.cl.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def encounter_list_loads(self):
        """Test "encounter_list" view."""
        response = self.client.get(reverse("encounter_list"))
        self.assertEqual(response.status_code, 200)

    def animalencounter_list_loads(self):
        """Test "observations:animalencounter-list" view."""
        response = self.client.get(reverse("observations:animalencounter-list"))
        self.assertEqual(response.status_code, 200)

    def animalencounter_detail_loads(self):
        """Test "observations:animalencounter-detail" view."""
        response = self.client.get(reverse("observations:animalencounter-detail", pk=self.cl.pk))
        self.assertEqual(response.status_code, 200)


class TurtleNestEncounterViewTests(TestCase):
    """TurtleNestEncounter view tests."""

    def setUp(self):
        """Setup: create a new list."""
        self.user = get_user_model().objects.create_superuser(
            username="superuser",
            email="super@gmail.com",
            password="test")
        self.cl = TurtleNestEncounter.objects.create(
            where=GEOSGeometry('POINT (115 -32)', srid=4326),
            when=timezone.now(),
            species="natator-depressus",
            source_id='12345',
            observer=self.user,
            reporter=self.user
        )
        self.user.save()
        self.client.force_login(self.user)

    def test_absolute_admin_url(self):
        """Test absolute admin url."""
        response = self.client.get(self.cl.absolute_admin_url)
        self.assertEqual(response.status_code, 200)

    def test_absolute_url(self):
        """Test absolute url."""
        response = self.client.get(self.cl.get_absolute_url())
        self.assertEqual(response.status_code, 200)

    def encounter_list_loads(self):
        """Test "encounter_list" view."""
        response = self.client.get(reverse("encounter_list"))
        self.assertEqual(response.status_code, 200)

    def turtlenestencounter_list_loads(self):
        """Test "observations:turtlenestencounter-list" view."""
        response = self.client.get(reverse("observations:turtlenestencounter-list"))
        self.assertEqual(response.status_code, 200)

    def turtlenestencounter_detail_loads(self):
        """Test "observations:turtlenestencounterdetail" view."""
        response = self.client.get(reverse("observations:turtlenestencounter-detail", pk=self.cl.pk))
        self.assertEqual(response.status_code, 200)
