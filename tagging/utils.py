from django.db.models import Max
from django.utils import timezone
import logging
from wamtram.models import (
    TrtPlaces,
    TrtPersons,
    TrtEntryBatches,
    TrtTurtles,
    TrtObservations,
    TrtTagOrders,
    TrtTags,
    TrtPitTags,
    TrtMeasurementTypes,
    TrtMeasurements,
    TrtDamage,
    TrtRecordedTags,
    TrtRecordedPitTags,
    TrtSamples,
    TrtIdentification,
)
from users.models import User
from .models import (
    TurtleSpecies,
    Location,
    Place,
    EntryBatch,
    Turtle,
    TurtleObservation,
    TagOrder,
    TurtleTag,
    TurtlePitTag,
    MeasurementType,
    TurtleMeasurement,
    TurtleDamage,
    TurtleTagObservation,
    TurtlePitTagObservation,
    TurtleSample,
    TurtleIdentification,
)


LOGGER = logging.getLogger("turtles")
TRT_SPECIES_MAP = {
    'FB': {'scientific_name': 'Natator depressus', 'common_name': 'Flatback Turtle', 'old_species_code': 'F', 'hide_dataentry': False},
    'GN': {'scientific_name': 'Chelonia mydas', 'common_name': 'Green Turtle', 'old_species_code': 'G', 'hide_dataentry': False},
    'HK': {'scientific_name': 'Eretmochelys imbricata', 'common_name': 'Hawksbill Turtle', 'old_species_code': 'H', 'hide_dataentry': False},
    'LB': {'scientific_name': 'Dermochelys coriacea', 'common_name': 'Leatherback Turtle', 'old_species_code': 'LB', 'hide_dataentry': False},
    'LO': {'scientific_name': 'Caretta caretta', 'common_name': 'Loggerhead Turtle', 'old_species_code': 'LO', 'hide_dataentry': False},
    'OR': {'scientific_name': 'Lepidochelys olivacea', 'common_name': 'Olive Ridley Turtle', 'old_species_code': 'OR', 'hide_dataentry': False},
}
TRT_LOCATION_MAP = {
    'AI': {'name': 'Airlie Island'},
    'AR': {'name': 'Ashmore Reef area'},
    'BR': {'name': 'Browse Island'},
    'BW': {'name': 'Barrow Island'},
    'BZ': {'name': 'Brazil coastal'},
    'CD': {'name': 'Cape Domett'},
    'CL': {'name': 'Cape Lambert'},
    'DA': {'name': 'Dampier Archipelago area'},
    'DH': {'name': 'Dirk Hartog Island'},
    'DI': {'name': 'Dorre Island'},
    'EG': {'name': 'Exmouth Gulf area'},
    'EI': {'name': 'Eastern Indian Ocean region'},
    'EM': {'name': 'Eighty Mile Beach - WA'},
    'GA': {'name': 'Gascoyne coastal - Not Ningaloo MP'},
    'GC': {'name': 'Gulf of Carpentaria area'},
    'IN': {'name': 'Indonesian territory'},
    'IR': {'name': 'Imperieuse Reef - Rowley Shoals'},
    'KS': {'name': 'King Sound area'},
    'LA': {'name': 'Lacepede Islands'},
    'LO': {'name': 'Lowendal Islands area'},
    'MB': {'name': 'Monte Bello Islands'},
    'MI': {'name': 'Montgomery Islands (Yawajaba: Yawijibaya people)'},
    'MN': {'name': 'Mundabullangana coast'},
    'MU': {'name': 'Muiron Islands'},
    'NI': {'name': 'Ningaloo MP coastal'},
    'NK': {'name': 'North Kimberley coastal'},
    'NT': {'name': 'Northern Territory coastal'},
    'NW': {'name': 'North West Cape area'},
    'PB': {'name': 'Pilbara offshore & coastal area'},
    'PE': {'name': 'Perth area'},
    'PH': {'name': 'Port Hedland coastal'},
    'QD': {'name': 'Queensland'},
    'RI': {'name': 'Rosemary Island - Dampier Archipelago'},
    'SB': {'name': 'Shark Bay area'},
    'SC': {'name': 'Southern WA coastal'},
    'SE': {'name': 'S-Eastern WA coastal'},
    'SR': {'name': 'Scott Reef'},
    'SW': {'name': 'S-Western WA coastal'},
    'TH': {'name': 'Thevenard Island'},
    'VA': {'name': 'Varanus Island - Lowendals'},
    'WC': {'name': 'Mid-Western WA coastal'},
    'WK': {'name': 'West Kimberley coastal'},
    'XX': {'name': 'Not otherwise assigned'},
}


def import_wamtram(reload=False):
    """Utility function to import/convert data from wamtram (SQL Server) to turtle_data (local).
    The function is idempotent, and may be run multiple times safely without creating duplicate data.

    If `reload` is False, some existing records will be skipped (those having the PK brought across).
    """
    admin = User.objects.get(pk=1)

    LOGGER.info("Importing species")
    TurtleSpecies.objects.get_or_create(
        scientific_name='Unknown', common_name='Not recorded - uncertain', old_species_code=None, hide_dataentry=False
    )
    for sp in TRT_SPECIES_MAP.values():
        TurtleSpecies.objects.get_or_create(**sp)
    LOGGER.info(f"TurtleSpecies object count: {TurtleSpecies.objects.count()}")

    LOGGER.info("Importing locations")
    for loc in TRT_LOCATION_MAP.values():
        Location.objects.get_or_create(**loc)
    LOGGER.info(f"Location object count: {Location.objects.count()}")

    LOGGER.info("Importing places")
    for pl in TrtPlaces.objects.all():
        if not Place.objects.filter(name=pl.place_name).exists():
            # First, match the newly-created Location obj.
            location = Location.objects.get(name=pl.location_code.location_name)
            Place.objects.get_or_create(
                location=location,
                name=pl.place_name,
                rookery=True if pl.rookery == "Y" else False if pl.rookery == "N" else None,
                beach_approach=pl.beach_approach,
                aspect=pl.aspect,
                point=pl.get_point(),
                comments=pl.comments,
            )
    LOGGER.info(f"Place object count: {Place.objects.count()}")

    LOGGER.info("Importing measurement types")
    for t in TrtMeasurementTypes.objects.all():
        MeasurementType.objects.get_or_create(
            short_desc=t.measurement_type,
            description=t.description,
            unit=t.measurement_units,
            minimum_value=t.minimum_value,
            maximum_value=t.maximum_value,
            comments=t.comments,
        )
    LOGGER.info(f"MeasurementType object count: {MeasurementType.objects.count()}")

    LOGGER.info("Importing persons")
    for p in TrtPersons.objects.all():
        name = p.get_name()
        if not User.objects.filter(name__iexact=name.lower(), is_active=True).exists():
            User.objects.create(
                username=p.email if p.email else "_".join([p.first_name, p.surname if p.surname else ""]),
                first_name=p.first_name,
                last_name=p.surname if p.surname else "",
                email=p.email if p.email else "",
                name=name,
                phone=p.mobile if p.mobile else p.telephone,
                role=" ".join([p.specialty if p.specialty else "", p.comments if p.comments else ""]).strip(),
            )
        elif User.objects.filter(name__iexact=name.lower(), is_active=True).count() > 1:
            LOGGER.info(f"POSSIBLE DUPLICATE USER: {p}")
    LOGGER.info(f"User object count: {User.objects.count()}")

    LOGGER.info("Importing entry batches")
    for b in TrtEntryBatches.objects.all():
        if b.entered_person_id:
            try:
                person = TrtPersons.objects.get(person_id=b.entered_person_id)
                name = f"{person.first_name} {person.surname}".strip()
                user = User.objects.get(name__iexact=name.lower(), is_active=True)
            except:
                user = admin
        else:
            user = admin

        if EntryBatch.objects.filter(pk=b.entry_batch_id).exists():
            if reload:
                eb = EntryBatch.objects.get(pk=b.entry_batch_id)
                eb.entry_date = b.entry_date.date() if b.entry_date else None
                eb.entered_by = user
                eb.filename = b.filename
                eb.comments = b.comments
                eb.pr_date_convention = b.pr_date_convention
                eb.save()
            else:
                continue
        else:
            EntryBatch.objects.get_or_create(
                pk=b.entry_batch_id,
                entry_date=b.entry_date.date() if b.entry_date else None,
                entered_by=user,
                filename=b.filename,
                comments=b.comments,
                pr_date_convention=b.pr_date_convention,
            )
    LOGGER.info(f"EntryBatch object count: {EntryBatch.objects.count()}")

    LOGGER.info("Importing tag orders")
    for o in TrtTagOrders.objects.all():
        if TagOrder.objects.filter(pk=o.tag_order_id).exists():
            if reload:
                to = TagOrder.objects.get(pk=o.tag_order_id)
                to.order_number = o.order_number
                to.order_date = o.order_date.date() if o.order_date else None
                to.tag_prefix = o.tag_prefix
                to.start_tag_number = o.start_tag_number
                to.end_tag_number = o.end_tag_number
                to.total_tags = o.total_tags
                to.date_received = o.date_received.date() if o.date_received else None
                to.paid_by = o.paid_by
                to.comments = o.comments
                to.save()
            else:
                continue
        else:
            TagOrder.objects.get_or_create(
                pk=o.tag_order_id,
                order_number=o.order_number,
                order_date=o.order_date.date() if o.order_date else None,
                tag_prefix=o.tag_prefix,
                start_tag_number=o.start_tag_number,
                end_tag_number=o.end_tag_number,
                total_tags=o.total_tags,
                date_received=o.date_received.date() if o.date_received else None,
                paid_by=o.paid_by,
                comments=o.comments,
            )
    LOGGER.info(f"TagOrder object count: {TagOrder.objects.count()}")

    LOGGER.info("Importing turtles")
    count = 0
    bobp = User.objects.get(username='bobp')
    turtle_ids = TrtTurtles.objects.values_list('turtle_id', flat=True)

    for id in turtle_ids:
        # Fast-path skip existing records, no reload.
        if Turtle.objects.filter(pk=id).exists() and not reload:
            continue
        else:
            t = TrtTurtles.objects.get(turtle_id=id)
            if t.species_code_id == "?":
                species = TurtleSpecies.objects.get(scientific_name='Unknown')
            elif t.species_code_id == "0":
                species = None
            else:
                species = TurtleSpecies.objects.get(scientific_name=t.species_code.scientific_name)
            if t.location_code:
                location = Location.objects.get(name=TRT_LOCATION_MAP[t.location_code_id]['name'])
            else:
                location = None
            if t.entered_by == 'bobp':
                entered_by = bobp
            else:
                entered_by = admin
            if t.sex == 'I':
                sex = 'U'  # Unknown
            else:
                sex = t.sex

            if Turtle.objects.filter(pk=t.turtle_id).exists():
                if reload:
                    tu = Turtle.objects.get(pk=t.turtle_id)
                    tu.created = t.date_entered if t.date_entered else timezone.now()
                    tu.entered_by = entered_by
                    tu.species = species
                    tu.sex = sex
                    tu.status = t.turtle_status.turtle_status if t.turtle_status else None
                    tu.name = t.turtle_name
                    tu.location = location
                    tu.cause_of_death = t.cause_of_death_id if t.cause_of_death else None
                    tu.re_entered_population = t.re_entered_population
                    tu.comments = t.comments
                    tu.original_turtle_id = t.original_turtle_id
                    tu.entry_batch = EntryBatch.objects.get(pk=t.entry_batch_id) if t.entry_batch_id else None
                    tu.mund_id = t.mund_id
                    tu.identification_confidence = t.identification_confidence
                    tu.save()
                else:
                    continue
            else:
                tu = Turtle.objects.get_or_create(
                    pk=t.turtle_id,
                    created=t.date_entered if t.date_entered else timezone.now(),
                    entered_by=entered_by,
                    species=species,
                    status=t.turtle_status.turtle_status if t.turtle_status else None,
                    name=t.turtle_name,
                    location=location,
                    cause_of_death=t.cause_of_death_id if t.cause_of_death else None,
                    re_entered_population=t.re_entered_population,
                    comments=t.comments,
                    original_turtle_id=t.original_turtle_id,
                    entry_batch=EntryBatch.objects.get(pk=t.entry_batch_id) if t.entry_batch_id else None,
                    mund_id=t.mund_id,
                    identification_confidence=t.identification_confidence,
                    sex=sex,
                )[0]

            for ti in TrtIdentification.objects.filter(turtle=t):
                TurtleIdentification.objects.get_or_create(
                    turtle_id=tu.pk,
                    identification_type=ti.identification_type.identification_type,
                    identifier=ti.identifier,
                    comments=ti.comments,
                )

            count += 1
            if count % 1000 == 0:
                LOGGER.info(f"{count} imported")
    LOGGER.info(f"Turtle object count: {Turtle.objects.count()}")
    LOGGER.info(f"TurtleIdentification object count: {TurtleIdentification.objects.count()}")

    LOGGER.info("Importing tags")
    count = 0
    tag_serials = TrtTags.objects.values_list('tag_id', flat=True)
    tag_serials = [(t.replace(" ", "").strip(), t) for t in tag_serials]

    for serials in tag_serials:
        # Fast-path skip existing records, no reload.
        if TurtleTag.objects.filter(serial=serials[0]).exists() and not reload:
            continue
        else:
            t = TrtTags.objects.get(tag_id=serials[1])

            if t.custodian_person_id and TrtPersons.objects.filter(person_id=t.custodian_person_id).exists():
                person = TrtPersons.objects.get(person_id=t.custodian_person_id)
                custodian = User.objects.get(name__iexact=person.get_name(), is_active=True)
            else:
                custodian = None
            if t.field_person_id and TrtPersons.objects.filter(person_id=t.field_person_id).exists():
                person = TrtPersons.objects.get(person_id=t.field_person_id)
                field_person = User.objects.get(name__iexact=person.get_name(), is_active=True)
            else:
                field_person = None
            serial = serials[0]

            if TurtleTag.objects.filter(serial=serial).exists():
                if reload:
                    tag = TurtleTag.objects.get(serial=serial)
                    tag.turtle_id = t.turtle_id
                    tag.issue_location = t.issue_location
                    tag.custodian = custodian
                    tag.side = t.side
                    tag.status = t.tag_status.tag_status
                    tag.return_date = t.return_date.date() if t.return_date else None
                    tag.return_condition = t.return_condition
                    tag.comments = t.comments
                    tag.field_person = field_person
                    tag.tag_order_id = t.tag_order_id if TagOrder.objects.filter(pk=t.tag_order_id).exists() else None
                    tag.save()
                else:
                    continue
            else:
                TurtleTag.objects.get_or_create(
                    serial=serial,
                    turtle_id=t.turtle_id,
                    issue_location=t.issue_location,
                    custodian=custodian,
                    side=t.side,
                    status=t.tag_status.tag_status,
                    return_date=t.return_date.date() if t.return_date else None,
                    return_condition=t.return_condition,
                    comments=t.comments,
                    field_person=field_person,
                    tag_order_id=t.tag_order_id if TagOrder.objects.filter(pk=t.tag_order_id).exists() else None,
                )
            count += 1
            if count % 1000 == 0:
                LOGGER.info(f"{count} imported")
    LOGGER.info(f"TurtleTag object count: {TurtleTag.objects.count()}")

    LOGGER.info("Importing pit tags")
    count = 0
    tag_serials = TrtPitTags.objects.values_list('pit_tag_id', flat=True)
    tag_serials = [(t.replace(" ", "").strip(), t) for t in tag_serials]

    for serials in tag_serials:
        # Fast-path skip existing records, no reload.
        if TurtlePitTag.objects.filter(serial=serials[0]).exists() and not reload:
            continue
        else:
            t = TrtPitTags.objects.get(pit_tag_id=serials[1])
            if t.custodian_person_id and TrtPersons.objects.filter(person_id=t.custodian_person_id).exists():
                person = TrtPersons.objects.get(person_id=t.custodian_person_id)
                custodian = User.objects.get(name__iexact=person.get_name(), is_active=True)
            else:
                custodian = None
            if t.field_person_id and TrtPersons.objects.filter(person_id=t.field_person_id).exists():
                person = TrtPersons.objects.get(person_id=t.field_person_id)
                field_person = User.objects.get(name__iexact=person.get_name(), is_active=True)
            else:
                field_person = None
            serial = serials[0]

            if TurtlePitTag.objects.filter(serial=serial).exists():
                if reload:
                    tag = TurtlePitTag.objects.get(serial=serial)
                    tag.turtle_id = t.turtle_id
                    tag.issue_location = t.issue_location
                    tag.custodian = custodian
                    tag.status = t.pit_tag_status
                    tag.return_date = t.return_date.date() if t.return_date else None
                    tag.return_condition = t.return_condition
                    tag.comments = t.comments
                    tag.field_person = field_person
                    tag.tag_order_id = t.tag_order_id if TagOrder.objects.filter(pk=t.tag_order_id).exists() else None
                    tag.batch_number = t.batch_number
                    tag.box_number = t.box_number
                    tag.save()
                else:
                    continue
            else:
                TurtlePitTag.objects.get_or_create(
                    serial=serial,
                    turtle_id=t.turtle_id,
                    issue_location=t.issue_location,
                    custodian=custodian,
                    status=t.pit_tag_status,
                    return_date=t.return_date.date() if t.return_date else None,
                    return_condition=t.return_condition,
                    comments=t.comments,
                    field_person=field_person,
                    tag_order_id=t.tag_order_id if TagOrder.objects.filter(pk=t.tag_order_id).exists() else None,
                    batch_number=t.batch_number,
                    box_number=t.box_number,
                )
            count += 1
            if count % 1000 == 0:
                LOGGER.info(f"{count} imported")
    LOGGER.info(f"TurtlePitTag object count: {TurtlePitTag.objects.count()}")

    LOGGER.info("Importing observations")
    count = 0
    turtle_observation_ids = TrtObservations.objects.values_list('observation_id', flat=True)

    for id in turtle_observation_ids:
        # Fast-path skip existing records, no reload.
        if TurtleObservation.objects.filter(pk=id).exists() and not reload:
            continue
        else:
            obs = TrtObservations.objects.get(observation_id=id)
            if obs.measurer_person:
                measurer = User.objects.get(name__iexact=obs.measurer_person.get_name(), is_active=True)
            else:
                measurer = None
            if obs.measurer_reporter_person:
                measurer_reporter = User.objects.get(name__iexact=obs.measurer_reporter_person.get_name(), is_active=True)
            else:
                measurer_reporter = None
            if obs.tagger_person:
                tagger = User.objects.get(name__iexact=obs.tagger_person.get_name(), is_active=True)
            else:
                tagger = None
            if obs.reporter_person:
                tagger_reporter = User.objects.get(name__iexact=obs.reporter_person.get_name(), is_active=True)
            else:
                tagger_reporter = None
            if obs.place_code and Place.objects.filter(name=obs.place_code.place_name).count() == 1:
                place = Place.objects.get(name=obs.place_code.place_name)
            else:
                place = None  # There are a couple of places with identical names but different locations.
            if obs.entered_by_person:
                entered_by = User.objects.get(name__iexact=obs.entered_by_person.get_name(), is_active=True)
            else:
                entered_by = admin
            if obs.clutch_completed and obs.clutch_completed == 'y':
                clutch_completed = 'Y'
            elif obs.clutch_completed and obs.clutch_completed == 'n':
                clutch_completed = 'U'
            else:
                clutch_completed = 'U'

            if TurtleObservation.objects.filter(pk=obs.observation_id).exists():
                if reload:
                    o = TurtleObservation.objects.get(pk=obs.observation_id)
                    o.created = obs.date_entered if obs.date_entered else timezone.now()
                    o.entered_by = entered_by
                    o.turtle_id = obs.turtle_id
                    o.observed = obs.get_observation_datetime_utc()
                    o.observation_date_old = obs.observation_date_old.date() if obs.observation_date_old else None
                    o.alive = True if obs.alive == "Y" else False if obs.alive == "N" else None
                    o.measurer = measurer
                    o.measurer_reporter = measurer_reporter
                    o.tagger = tagger
                    o.tagger_reporter = tagger_reporter
                    o.place = place
                    o.place_description = obs.place_description
                    o.point = obs.get_point()
                    o.activity = obs.activity_code.activity_code if obs.activity_code else None
                    o.beach_position = obs.beach_position_code.beach_position_code if obs.beach_position_code else None
                    o.condition = obs.condition_code.condition_code if obs.condition_code else None
                    o.nesting = True if obs.nesting == "Y" else False if obs.nesting == "N" else None
                    o.clutch_completed = clutch_completed
                    o.number_of_eggs = obs.number_of_eggs
                    o.egg_count_method = obs.egg_count_method.egg_count_method if obs.egg_count_method else None
                    o.action_taken = obs.action_taken
                    o.comments = obs.comments
                    o.original_observation_id = obs.original_observation_id
                    o.entry_batch = EntryBatch.objects.get(pk=obs.entry_batch_id) if obs.entry_batch else None
                    o.comment_fromrecordedtagstable = obs.comment_fromrecordedtagstable
                    o.scars_left = obs.scars_left
                    o.scars_right = obs.scars_right
                    o.transferid = obs.transferid
                    o.mund = obs.mund
                    o.scars_left_scale_1 = obs.scars_left_scale_1
                    o.scars_left_scale_2 = obs.scars_left_scale_2
                    o.scars_left_scale_3 = obs.scars_left_scale_3
                    o.scars_right_scale_1 = obs.scars_right_scale_1
                    o.scars_right_scale_2 = obs.scars_right_scale_2
                    o.scars_right_scale_3 = obs.scars_right_scale_3
                    o.cc_length_not_measured = obs.cc_length_not_measured
                    o.cc_notch_length_not_measured = obs.cc_notch_length_not_measured
                    o.cc_width_not_measured = obs.cc_width_not_measured
                    o.tagscarnotchecked = obs.tagscarnotchecked
                    o.didnotcheckforinjury = obs.didnotcheckforinjury
                    o.date_convention = obs.date_convention
                    o.status = obs.observation_status
                    o.corrected_date = obs.corrected_date.date() if obs.corrected_date else None
                    o.curation_status = TurtleObservation.CURATION_STATUS_IMPORTED
                    o.save()
                else:
                    continue
            else:
                o = TurtleObservation.objects.create(
                    pk=obs.observation_id,
                    created=obs.date_entered if obs.date_entered else timezone.now(),
                    entered_by=entered_by,
                    turtle_id=obs.turtle_id,
                    observed=obs.get_observation_datetime_utc(),
                    observation_date_old=obs.observation_date_old.date() if obs.observation_date_old else None,
                    alive=True if obs.alive == "Y" else False if obs.alive == "N" else None,
                    measurer=measurer,
                    measurer_reporter=measurer_reporter,
                    tagger=tagger,
                    tagger_reporter=tagger_reporter,
                    place=place,
                    place_description=obs.place_description,
                    point=obs.get_point(),
                    activity=obs.activity_code.activity_code if obs.activity_code else None,
                    beach_position=obs.beach_position_code.beach_position_code if obs.beach_position_code else None,
                    condition=obs.condition_code.condition_code if obs.condition_code else None,
                    nesting=True if obs.nesting == "Y" else False if obs.nesting == "N" else None,
                    clutch_completed=clutch_completed,
                    number_of_eggs=obs.number_of_eggs,
                    egg_count_method=obs.egg_count_method.egg_count_method if obs.egg_count_method else None,
                    action_taken=obs.action_taken,
                    comments=obs.comments,
                    original_observation_id=obs.original_observation_id,
                    entry_batch=EntryBatch.objects.get(pk=obs.entry_batch_id) if obs.entry_batch else None,
                    comment_fromrecordedtagstable=obs.comment_fromrecordedtagstable,
                    scars_left=obs.scars_left,
                    scars_right=obs.scars_right,
                    transferid=obs.transferid,
                    mund=obs.mund,
                    scars_left_scale_1=obs.scars_left_scale_1,
                    scars_left_scale_2=obs.scars_left_scale_2,
                    scars_left_scale_3=obs.scars_left_scale_3,
                    scars_right_scale_1=obs.scars_right_scale_1,
                    scars_right_scale_2=obs.scars_right_scale_2,
                    scars_right_scale_3=obs.scars_right_scale_3,
                    cc_length_not_measured=obs.cc_length_not_measured,
                    cc_notch_length_not_measured=obs.cc_notch_length_not_measured,
                    cc_width_not_measured=obs.cc_width_not_measured,
                    tagscarnotchecked=obs.tagscarnotchecked,
                    didnotcheckforinjury=obs.didnotcheckforinjury,
                    date_convention=obs.date_convention,
                    status=obs.observation_status,
                    corrected_date=obs.corrected_date.date() if obs.corrected_date else None,
                    curation_status=TurtleObservation.CURATION_STATUS_IMPORTED,
                )

            for m in TrtMeasurements.objects.filter(observation=obs):
                mtype = MeasurementType.objects.get(short_desc=m.measurement_type.measurement_type)
                try:
                    TurtleMeasurement.objects.get_or_create(
                        observation=o,
                        measurement_type=mtype,
                        value=m.measurement_value,
                        comments=m.comments,
                    )
                except:
                    pass  # Pass on exception.

            for d in TrtDamage.objects.filter(observation=obs):
                try:
                    TurtleDamage.objects.get_or_create(
                        observation=o,
                        body_part=d.body_part_id,
                        damage=d.damage_code_id,
                        cause=d.damage_cause_code_id,
                        comments=d.comments,
                    )
                except:
                    pass  # Pass on exception.

            for t in TrtRecordedTags.objects.filter(observation_id=obs.pk):
                try:
                    tag = TurtleTag.objects.get(serial=t.tag_id)
                    TurtleTagObservation.objects.get_or_create(
                        tag=tag,
                        observation=o,
                        status=t.tag_state,
                        position=t.tag_position,
                        barnacles=t.barnacles,
                        comments=t.comments,
                    )
                except:
                    pass  # Pass on exception.

            for t in TrtRecordedPitTags.objects.filter(observation_id=obs.pk):
                try:
                    pit_tag = TurtlePitTag.objects.get(serial=t.pit_tag_id)
                    TurtlePitTagObservation.objects.get_or_create(
                        tag=pit_tag,
                        observation=o,
                        status=t.pit_tag_state.pit_tag_state,
                        position=t.pit_tag_position,
                        checked=t.checked,
                        comments=t.comments,
                    )
                except:
                    pass  # Pass on exception.

            for t in TrtSamples.objects.filter(observation_id=obs.pk):
                try:
                    TurtleSample.objects.get_or_create(
                        observation=o,
                        tissue_type=t.tissue_type.tissue_type,
                        label=t.sample_label,
                        sample_date=t.sample_date.date() if t.sample_date else None,
                        arsenic=t.arsenic,
                        selenium=t.selenium,
                        zinc=t.zinc,
                        cadmium=t.cadmium,
                        copper=t.copper,
                        lead=t.lead,
                        mercury=t.mercury,
                        comments=t.comments,
                    )
                except:
                    pass  # Pass on exception.

            count += 1
            if count % 1000 == 0:
                LOGGER.info(f"{count} imported")

    LOGGER.info(f"TurtleObservation object count: {TurtleObservation.objects.count()}")
    LOGGER.info(f"TurtleMeasurement object count: {TurtleMeasurement.objects.count()}")
    LOGGER.info(f"TurtleDamage object count: {TurtleDamage.objects.count()}")
    LOGGER.info(f"TurtleTagObservation object count: {TurtleTagObservation.objects.count()}")
    LOGGER.info(f"TurtlePitTagObservation object count: {TurtlePitTagObservation.objects.count()}")
    LOGGER.info(f"TurtleSample object count: {TurtleSample.objects.count()}")

    LOGGER.info("Complete")
    LOGGER.info("Set sequence values for: EntryBatch, TagOrder, Turtle, TurtleObservation")
    entrybatch_id_max = EntryBatch.objects.aggregate(Max('pk'))['pk__max']
    LOGGER.info(f"SELECT setval('tagging_entrybatch_id_seq', {entrybatch_id_max}, true);")
    tagorder_id_max = TagOrder.objects.aggregate(Max('pk'))['pk__max']
    LOGGER.info(f"SELECT setval('tagging_tagorder_id_seq', {tagorder_id_max}, true);")
    turtle_id_max = Turtle.objects.aggregate(Max('pk'))['pk__max']
    LOGGER.info(f"SELECT setval('tagging_turtle_id_seq', {turtle_id_max}, true);")
    turtleobservation_id_max = TurtleObservation.objects.aggregate(Max('pk'))['pk__max']
    LOGGER.info(f"SELECT setval('tagging_turtleobservation_id_seq', {turtleobservation_id_max}, true);")
    ident_id_max = TurtleIdentification.objects.aggregate(Max('pk'))['pk__max']
    LOGGER.info(f"SELECT setval('tagging_turtleidentification_id_seq', {ident_id_max}, true);")