# -*- coding: utf-8 -*-
"""Tasks for WAStD."""
import logging
import os

from background_task import background
from django.conf import settings
from django.utils import timezone
from sentry_sdk import capture_message

from wastd.observations import utils, models

logger = logging.getLogger(__name__)


@background(queue="admin-tasks", schedule=timezone.now())
def update_names():
    """Update cached names on Encounters and reconstructs Surveys."""
    msg = "[wastd.observations.tasks.update_names] Start updating names..."
    logger.info(msg)
    capture_message(msg, level="info")
    encs = utils.reconstruct_animal_names()
    msg = ("[wastd.observations.tasks.update_names] "
           "{} animal names reconstructed. ".format(len(encs)))
    logger.info(msg)
    capture_message(msg, level="warning")


@background(queue="admin-tasks", schedule=timezone.now())
def resave_surveys():
    """Re-save Surveys."""
    msg = "[wastd.observations.tasks.resave_surveys] Start re-saving Surveys..."
    logger.info(msg)
    capture_message(msg, level="info")
    surveys = [s.save() for s in models.Survey.objects.all()]
   
    msg = "[wastd.observations.tasks.resave_surveys] {0} surveys reconstructed".format(len(surveys))
    logger.info(msg)
    capture_message(msg, level="warning")

@background(queue="admin-tasks", schedule=timezone.now())
def import_odka():
    """Download and import new ODKA submissions."""
    capture_message(
        "[wastd.observations.tasks.import_odka] Starting ODKA import.",
        level="warning"
    )
    path = os.path.join(settings.MEDIA_ROOT, "odka")
    os.makedirs(path, exist_ok=True)

    utils.save_all_odka(path=path)
    capture_message(
        "[wastd.observations.tasks.import_odka] ODKA submissions downloaded.",
        level="info"
    )

    utils.import_all_odka(path=path)
    capture_message(
        "[wastd.observations.tasks.import_odka] ODKA submissions imported.",
        level="info"
    )

    utils.reconstruct_missing_surveys()
    capture_message(
        "[wastd.observations.tasks.import_odka] "
        "ODKA surveys reconstructed, task successfully finished.",
        level="warning"
    )

@background(queue="admin-tasks", schedule=timezone.now())
def reconstruct_surveys():
    """Reconstruct missing surveys."""

    utils.reconstruct_missing_surveys()
    capture_message(
        "[wastd.observations.tasks.reconstruct_surveys] "
        "ODKA surveys reconstructed, task successfully finished.",
        level="warning"
    )
