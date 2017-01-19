# -*- coding: utf-8 -*-
"""Observation untilities."""
import json
import os
from pprint import pprint
import requests
import shutil

from django.conf import settings
from django.contrib.auth import get_user_model
from django.contrib.gis.geos import Point
from django.core.exceptions import ObjectDoesNotExist
from django.core.files import File
from django.utils.dateparse import parse_datetime

from wastd.observations.models import (
    Encounter, AnimalEncounter, LoggerEncounter, TurtleNestEncounter,
    TurtleNestDisturbanceObservation, MediaAttachment,
    NEST_AGE_CHOICES, NEST_TYPE_CHOICES, OBSERVATION_CHOICES,
    NEST_DAMAGE_CHOICES, CONFIDENCE_CHOICES
    )


def allocate_animal_names():
    """Reconstruct names of Animals from their first allocated Flipper Tag.

    Names are inferred as the first ever allocated flipper tag ID and written
    to each Encounter. Note this can include non-AnimalEncounters, such as
    incidents of tag returns, post-mortem necropsies and other incidentes related
    to an absent animal.

    Algorithm:

    * Find list of new captures (AnimalEncounters with at least one newly
      allocated FlipperTag and no other existing, resighted tags)
    * For each new capture, get the primary flipper tag name as animal name
    * Set the animal name of this and all related Encounters
    """
    ae = [a.set_name_and_propagate(a.primary_flipper_tag.name)
          for a in AnimalEncounter.objects.all() if a.is_new_capture]
    le = [a.save() for a in LoggerEncounter.objects.all()]
    return [ae, le]


def symlink_one_resource(t_dir, rj):
    """Symlink photographs of a resource JSON ``rj`` to a temp dir ``t_dir``."""
    if "photographs" in rj and len(rj["photographs"]) > 0:
        # Once per encounter, create temp_dir/media_path
        media_path = os.path.split(rj["photographs"][0]["attachment"])[0]
        print("pre_latex symlinking {0}".format(media_path))
        dest_dir = os.path.join(t_dir, "tex", media_path)
        os.makedirs(dest_dir)
        print("pre_latex created {0}".format(str(dest_dir)))

        for photo in rj["photographs"]:
            # Once per photo, symlink file to temp_dir
            src = photo["filepath"]
            rel_src = photo["attachment"]
            dest = os.path.join(t_dir, "tex", rel_src)
            if os.path.lexists(dest):
                # emulate ln -sf
                os.remove(dest)
            os.symlink(src, dest)
    else:
        print("No photographs found.")


def symlink_resources(t_dir, data):
    """Symlink photographs from an OrderedDict ``data`` of Encounters to a temp dir.

    ``data`` can be an OrderedDict of either:
    - a GeoJSON FeatureCollection of Encounters (rest_framework.gis serializer)
    - a GeoJSON Feature of one Encounter
    - a JSON list of Encounters (rest_framework model serializer)
    - a JSON dict of one Encounter
    """
    d = json.loads(json.dumps(data))
    if "type" in d.keys():

        if d["type"] == "FeatureCollection":
            print("Symlinking photographs of a GeoJSON FeatureCollection")
            [symlink_one_resource(t_dir, f["properties"]) for f in d["features"]]

        elif d["type"] == "Feature":
            print("Symlinking photographs of a GeoJSON Feature")
            symlink_one_resource(t_dir, d["properties"])

    elif "photographs" in d.keys():
        print("Symlinking photographs of a JSON object")
        symlink_one_resource(t_dir, d)
    else:
        print("Symlinking photographs of a list of JSON objects")
        [symlink_one_resource(t_dir, enc) for enc in d]


#------------------------------------------------------------------------------#
# Data import from ODK Aggregate
# TODO create and use writable API
#
def guess_user(un):
    """Find exact or fuzzy match of username, or create User.

    In order, return:

    * A user with username `un`, or
    * a user with username `icontain`ing the first five characters of `un`, or
    * a new user with username `un`.

    Arguments

    un A username

    Returns
    An instance of settings.AUTH_USER_MODEL
    """
    User = get_user_model()

    try:
        usr = User.objects.get(username=un)
        msg = "Username {0} found by exact match: returning {1}"
    except ObjectDoesNotExist:
        try:
            usr = User.objects.filter(username__icontains=un[0:4])[0]
            msg = "Username {0} found by fuzzy match: returning {1}"
        except ObjectDoesNotExist:
            msg = "Username {0} not found: created {1}"
            usr = User.objects.create(username=un, name=un)

    print(msg.format(un, usr))
    return usr


def map_values(d):
    """Return a dict of ODK:WAStD dropdown menu choices for a given choice dict.

    Arguments

    d The dict_name, e.g. NEST_TYPE_CHOICES

    Returns

    A dict of ODK (keys) to WAStD (values) choices, e.g. NEST_TYPE_CHOICES
    {u'falsecrawl': u'false-crawl',
     u'hatchednest': u'hatched-nest',
     u'nest': u'nest',
     u'successfulcrawl': u'successful-crawl',
     u'tracknotassessed': u'track-not-assessed',
     u'trackunsure': u'track-unsure'}
    """
    return {k.replace("-", ""): k for k in dict(d).keys()}


def make_photo_foldername(photo_id):
    return os.path.join(settings.MEDIA_ROOT, "photos", photo_id)


def dl_photo(photo_id, photo_url, photo_filename):
    """Download a photo if not already done.

    Arguments

    photo_id The WAStD source_id of the record, to which this photo belongs
    photo_url A URL to download the photo from
    """
    pdir = make_photo_foldername(photo_id)
    if not os.path.exists(pdir):
        print("Creating folder {0}".format(pdir))
        os.mkdir(pdir)
    else:
        print(("Found folder {0}".format(pdir)))
    pname = os.path.join(pdir, photo_filename)

    if not os.path.exists(pname):
        print("Downloading file {0}...".format(pname))
        response = requests.get(photo_url, stream=True)
        with open(pname, 'wb') as out_file:
            shutil.copyfileobj(response.raw, out_file)
        del response
    else:
        print("Found file {0}".format(pname))


def handle_photo(p, e, title="Track"):
    """Create a MediaAttachment of photo p to Encounter e with a given title.

    Arguments

    p The filepath of a locally accessible photograph
    e The related encounter (must exist)
    title The attachment's title (default: "Track")
    """
    # Does the file exist locally?
    if os.path.exists(p):
        print("File {0} exists".format(p))
        with open(p, 'rb') as photo:
            f = File(photo)
            # Is the file a dud?
            if f.size > 0:
                print("File size is {0}".format(f.size))

                # Does the MediaAttachment exist already?
                if MediaAttachment.objects.filter(encounter=e, title=title).exists():
                    m = MediaAttachment.objects.filter(encounter=e, title=title)[0]
                    action = "updated"
                else:
                    m = MediaAttachment(encounter=e, title=title)
                    action = "Created"

                # Update the file
                m.attachment.save(title, f, save=True)
                print("Photo {0}: {1}".format(action, m))
            else:
                print("[ERROR] zero size file {0}".format(p))
    else:
        print("[ERROR] missing file {0}".format(p))


def handle_turtlenestdistobs(d, e, m):
    """Get or create TurtleNestDisturbanceObservation.

    Arguments

    d A dictionary like
        {
            "disturbance_cause": "human",
            "disturbance_cause_confidence": "expertopinion",
            "disturbance_severity": "na",
            "photo_disturbance": {
                "filename": "1479173301849.jpg",
                "type": "image/jpeg",
                "url": "https://dpaw-data.appspot.com/view/binaryData?blobKey=build_TrackCount-0-10_1479172852%5B%40version%3Dnull+and+%40uiVersion%3Dnull%5D%2Fdata%5B%40key%3Duuid%3Af23177b3-2234-49be-917e-87b2096c921e%5D%2Fdisturbanceobservation%5B%40ordinal%3D1%5D%2Fphoto_disturbance"
            },
            "comments": null
        }
    e The related TurtleNestEncounter (must exist)
    m The ODK_MAPPING
    """

    print("Found disturbance obs")
    pprint(d)

    dd, created = TurtleNestDisturbanceObservation.objects.get_or_create(
        encounter=e,
        disturbance_cause=m["disturbance_cause"][d["disturbance_cause"]],
        disturbance_cause_confidence=m["disturbance_cause_confidence"][d["disturbance_cause_confidence"]],
        disturbance_severity=m["disturbance_severity"][d["disturbance_severity"]],
        comments=d["comments"]
        )
    dd.save()
    e.save()  # cache distobs in HTML

    if d["photo_disturbance"] is not None:
        dl_photo(e.source_id,
                 d["photo_disturbance"]["url"],
                 d["photo_disturbance"]["filename"])
        pdir = make_photo_foldername(e.source_id)
        pname = os.path.join(pdir, d["photo_disturbance"]["filename"])
        handle_photo(pname, e, title="Disturbance {0}".format(dd.disturbance_cause))
    pprint(dd)


def import_one_record_tc010(r, m):
    """Import one ODK Track Count 0.10 record into WAStD.

    Arguments

    r The record as dict
    m The mapping of ODK to WAStD choices

    Existing records will be overwritten.
    Make sure to skip existing records which should be retained.
    """

    src_id = r["instanceID"]

    new_data = dict(
        source="odk",
        source_id=src_id,
        where=Point(r["observed_at:Longitude"], r["observed_at:Latitude"]),
        when=parse_datetime(r["observation_start_time"]),
        location_accuracy="10",
        observer=m["users"][r["reporter"]],
        reporter=m["users"][r["reporter"]],
        nest_age=m["nest_age"][r["nest_age"]],
        nest_type=m["nest_type"][r["nest_type"]],
        species=m["species"][r["species"]],
        # comments
        )
    if r["nest_type"] in ["successfulcrawl", "nest", "hatchednest"]:
        new_data["habitat"] = m["habitat"][r["habitat"]]
        new_data["disturbance"] = m["disturbance"][r["disturbance"]]

    if src_id in m["overwrite"]:
        print("Found record {0}, updating...".format(src_id))
        TurtleNestEncounter.objects.filter(source_id=src_id).update(**new_data)
        e = TurtleNestEncounter.objects.get(source_id=src_id)
    else:
        print("New record {0}, creating...".format(src_id))
        e = TurtleNestEncounter.objects.create(**new_data)

    e.save()
    pprint(e)

    # MediaAttachment "Photo of track"
    if r["photo_track"] is not None:
        pdir = make_photo_foldername(src_id)
        pname = os.path.join(pdir, r["photo_track"]["filename"])
        handle_photo(pname, e, title="Track")

    # MediaAttachment "Photo of nest"
    if r["photo_nest"] is not None:
        pdir = make_photo_foldername(src_id)
        pname = os.path.join(pdir, r["photo_nest"]["filename"])
        handle_photo(pname, e, title="Nest")

    # TurtleNestDisturbanceObservation, MediaAttachment "Photo of disturbance"
    [handle_turtlenestdistobs(distobs, e, m)
     for distobs in r["disturbanceobservation"]
     if len(r["disturbanceobservation"]) > 0]


def import_odk(jsonfile, flavour="odk-trackcount-010"):
    """Import ODK Track Count 0.10 data.

    Arguments

    jsonfile A filepath to the JSON exported from ODK Aggregate
    flavour The ODK form with version

    Preparation:

    * https://dpaw-data.appspot.com/ > Submissions > Form "TrackCount 0.10"
    * Export > JSON > Export
    * Submissions > Exported Submissions > download JSON

    Behaviour:

    * Records in JSON that are not in db will be created in db
    * Records in JSON that are in db, but have status NEW (not QA'd yet) will
      be created in db
    * Records in JSON that are in db, but have status **above** NEW (QA'd and
      possibly locally changed) will be ignored

    Example:

        >>> from django.conf import settings
        >>> json_file = os.path.join(settings.STATIC_ROOT, 'data', 'TrackCount_0_10_results.json')
        >>> import_odk(json_file)
    """

    with open(jsonfile) as df:
        d = json.load(df)
        print("Loaded {0} records from {1}".format(len(d), jsonfile))

    # generate a fresh mapping... once
    ODK_MAPPING = {
        # some values can be derived
        "nest_age": map_values(NEST_AGE_CHOICES),
        "nest_type": map_values(NEST_TYPE_CHOICES),

        # some are custom
        "species": {
            'flatback': 'Natator depressus',
            'green': 'Chelonia mydas',
            'hawksbill': 'Eretmochelys imbricata',
            'loggerhead': 'Caretta caretta',
            'oliveridley': 'Lepidochelys olivacea',
            'leatherback': 'Dermochelys coriacea',
            'turtle': 'Cheloniidae fam.'
            },

        "habitat": {
            'abovehwm': 'beach-above-high-water',
            'belowhwm': 'beach-below-high-water',
            'edgeofvegetation': 'beach-edge-of-vegetation',
            'vegetation': 'in-dune-vegetation',
            'na': 'na',
            },
        "disturbance": map_values(OBSERVATION_CHOICES),
        "disturbance_cause": map_values(NEST_DAMAGE_CHOICES),
        "disturbance_cause_confidence": map_values(CONFIDENCE_CHOICES),
        "disturbance_severity": map_values(
            TurtleNestDisturbanceObservation.NEST_VIABILITY_CHOICES),

        # some have to be guessed
        "users": {u: guess_user(u) for u in set([r["reporter"] for r in d])},
        "keep":  [t.source_id for t in TurtleNestEncounter.objects.exclude(
            status=Encounter.STATUS_NEW).filter(source="odk")],
        "overwrite": [t.source_id for t in TurtleNestEncounter.objects.filter(
            source="odk", status=Encounter.STATUS_NEW)]
        }
    print("\n\nMapping:\n\n")
    pprint(ODK_MAPPING)

    if flavour == "odk-trackcount-010":
        print("Using flavour ODK Track Count 0.10...")

        # Download photos
        pt = [[r["instanceID"],
               r["photo_track"]["url"],
               r["photo_track"]["filename"]]
              for r in d
              if r["photo_track"] is not None]
        pn = [[r["instanceID"],
               r["photo_nest"]["url"],
               r["photo_nest"]["filename"]]
              for r in d
              if r["photo_nest"] is not None]
        print("Downloading photos of {0} tracks and {1} nests".format(
            len(pt), len(pn)))
        all_photos = pt + pn
        [dl_photo(p[0], p[1], p[2]) for p in all_photos]

        [import_one_record_tc010(r, ODK_MAPPING) for r in d
         if r["instanceID"] not in ODK_MAPPING["keep"]]     # retain local edits
        print("Done!")
