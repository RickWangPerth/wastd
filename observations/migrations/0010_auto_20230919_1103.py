# Generated by Django 3.2.21 on 2023-09-19 03:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('observations', '0009_auto_20230823_1001'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='encounter',
            name='as_html',
        ),
        migrations.AlterField(
            model_name='animalencounter',
            name='activity',
            field=models.CharField(choices=[('na', 'Not applicable'), ('arriving', 'Arriving on beach'), ('approaching', 'Approaching nesting site'), ('digging-body-pit', 'Digging body pit'), ('excavating-egg-chamber', 'Excavating egg chamber'), ('laying-eggs', 'Laying eggs'), ('filling-in-egg-chamber', 'Filling in egg chamber'), ('filling-in-nest', 'Filling in nest'), ('camouflaging-nest', 'Camouflaging nest'), ('returning-to-water', 'Returning to water'), ('general-breeding-activity', 'General breeding activity'), ('floating', 'Floating (dead, sick, unable to dive, drifting in water)'), ('beach-washed', 'Beach washed (dead, sick or stranded on beach/coast)'), ('beach-jumped', 'Beach jumped'), ('carcass-tagged-released', 'Carcass tagged and released'), ('carcass-inland', 'Carcass or butchered remains found removed from coast'), ('captivity', 'In captivity'), ('non-breeding', 'Non-breeding activity (swimming, sleeping, feeding, etc.)'), ('other', 'Other activity')], default='na', help_text="The animal's activity at the time of observation.", max_length=300, verbose_name='Activity'),
        ),
        migrations.AlterField(
            model_name='animalencounter',
            name='cause_of_death',
            field=models.CharField(choices=[('na', 'Not applicable'), ('indeterminate-decomposed', 'Indeterminate due to decomposition'), ('boat-strike', 'Boat strike'), ('trauma-human-induced', 'Human induced trauma'), ('trauma-animal-induced', 'Animal induced trauma'), ('drowned-entangled-fisheries', 'Drowned entangled in fisheries equipment'), ('drowned-entangled-infrastructure', 'Drowned entangled in infrastructure'), ('drowned-entangled-debris', 'Drowned entangled in debris'), ('drowned-entangled', 'Drowned entangled'), ('drowned-other', 'Drowned'), ('fishery-bycatch', 'Fishery bycatch'), ('handling-accident', 'Handling accident'), ('car-collision', 'Car collision'), ('ingested-debris', 'Ingested debris'), ('harvest', 'Harvested for human consumption'), ('poisoned', 'Poisoned'), ('misorientation', 'Misorientation on beach'), ('natural', 'Natural death'), ('birthing', 'Birthing complications'), ('still-born', 'Still birth'), ('calf-failure-to-thrive', 'Calf failed to thrive'), ('starved', 'Starvation'), ('stranded', 'Stranding'), ('euthanasia-firearm', 'Euthanasia by firearm'), ('euthanasia-injection', 'Euthanasia by injection'), ('euthanasia-implosion', 'Euthanasia by implosion'), ('euthanasia', 'Euthanasia'), ('predation', 'Predation')], default='na', help_text='If dead, is the case of death known?', max_length=300, verbose_name='Cause of death'),
        ),
        migrations.AlterField(
            model_name='animalencounter',
            name='cause_of_death_confidence',
            field=models.CharField(choices=[('na', 'Not applicable'), ('guess', 'Guess based on insuffient evidence'), ('expert-opinion', 'Expert opinion based on available evidence'), ('validated', 'Validated by authoritative source')], default='na', help_text='What is the cause of death, if known, based on?', max_length=300, verbose_name='Cause of death confidence'),
        ),
        migrations.AlterField(
            model_name='animalencounter',
            name='checked_for_flipper_tags',
            field=models.CharField(choices=[('na', 'Not applicable'), ('absent', 'Absent'), ('present', 'Present'), ('yes', 'Yes'), ('no', 'No')], default='na', help_text='Was the animal checked for flipper tags, were any found?', max_length=300, verbose_name='Checked for flipper tags'),
        ),
        migrations.AlterField(
            model_name='animalencounter',
            name='checked_for_injuries',
            field=models.CharField(choices=[('na', 'Not applicable'), ('absent', 'Absent'), ('present', 'Present'), ('yes', 'Yes'), ('no', 'No')], default='na', help_text='Was the animal checked for injuries, were any found?', max_length=300, verbose_name='Checked for injuries'),
        ),
        migrations.AlterField(
            model_name='animalencounter',
            name='maturity',
            field=models.CharField(choices=[('na', 'Unknown maturity'), ('hatchling', 'Hatchling'), ('post-hatchling', 'Post-hatchling'), ('juvenile', 'Juvenile'), ('pre-pubescent-immature', 'Pre-pubescent immature'), ('pubescent-immature', 'Pubescent immature'), ('sub-adult', 'Sub-adult'), ('adult-measured', 'Adult (status determined from carapace and tail measurements)'), ('unweaned', 'Unweaned immature'), ('weaned', 'Weaned immature'), ('adult', 'Adult')], default='na', help_text="The animal's maturity.", max_length=300, verbose_name='Maturity'),
        ),
        migrations.AlterField(
            model_name='animalencounter',
            name='nesting_disturbed',
            field=models.CharField(choices=[('na', 'Not applicable'), ('absent', 'Absent'), ('present', 'Present'), ('yes', 'Yes'), ('no', 'No')], default='na', help_text='Was the nesting interrupted? If so, specify disturbance in comments.', max_length=300, verbose_name='Nesting disturbed'),
        ),
        migrations.AlterField(
            model_name='animalencounter',
            name='nesting_event',
            field=models.CharField(choices=[('na', 'Not applicable'), ('nest-with-eggs', 'Nest with eggs - witnessed egg drop'), ('nest-unsure-of-eggs', 'Nest unsure of eggs - found covered up nest mound'), ('unsure-if-nest', "Unsure if nest - can't tell whether nest mound present or not"), ('no-nest', 'No nest - witnessed aborted nest or found track with no nest')], default='na', help_text='What indication of nesting success was observed?', max_length=300, verbose_name='Nesting success'),
        ),
        migrations.AlterField(
            model_name='animalencounter',
            name='scanned_for_pit_tags',
            field=models.CharField(choices=[('na', 'Not applicable'), ('absent', 'Absent'), ('present', 'Present'), ('yes', 'Yes'), ('no', 'No')], default='na', help_text='Was the animal scanned for PIT tags, were any found?', max_length=300, verbose_name='Scanned for PIT tags'),
        ),
        migrations.AlterField(
            model_name='animalencounter',
            name='sex',
            field=models.CharField(choices=[('na', 'Not applicable'), ('unknown', 'Unknown'), ('male', 'Male'), ('female', 'Female'), ('intersex', 'Hermaphrodite or intersex')], default='na', help_text="The animal's sex.", max_length=300, verbose_name='Sex'),
        ),
        migrations.AlterField(
            model_name='animalencounter',
            name='species',
            field=models.CharField(choices=[('na', 'Not applicable'), ('natator-depressus', 'Natator depressus (Flatback turtle)'), ('chelonia-mydas', 'Chelonia mydas (Green turtle)'), ('eretmochelys-imbricata', 'Eretmochelys imbricata (Hawksbill turtle)'), ('caretta-caretta', 'Caretta caretta (Loggerhead turtle)'), ('lepidochelys-olivacea', 'Lepidochelys olivacea (Olive ridley turtle)'), ('dermochelys-coriacea', 'Dermochelys coriacea (Leatherback turtle)'), ('chelonia-mydas-agassazzi', 'Chelonia mydas agassazzi (Black turtle or East Pacific Green)'), ('test-turtle', 'Test/training turtle'), ('cheloniidae-fam', 'Cheloniidae (Unidentified turtle)'), ('delphinus-delphis', 'Delphinus delphis (Short-beaked common dolphin)'), ('grampus-griseus', "Grampus griseus (Risso's dolphin)"), ('lagenodelphis-hosei', "Lagenodelphis hosei (Fraser's dolphin)"), ('lagenorhynchus-obscurus', 'Lagenorhynchus obscurus (Dusky dolphin)'), ('orcaella-heinsohni', 'Orcaella heinsohni (Australian snubfin dolphin)'), ('sousa-sahulensis', 'Sousa sahulensis (Australian humpback dolphin)'), ('sousa-chinensis', 'Sousa chinensis (Chinese white dolphin)'), ('stenella-attenuata', 'Stenella attenuata (Pantropical spotted dolphin)'), ('stenella-coeruleoalba', 'Stenella coeruleoalba (Striped dolphin)'), ('stenella-longirostris', 'Stenella longirostris (Spinner dolphin)'), ('stenella-sp', 'Stenella sp. (Unidentified spotted dolphin)'), ('steno-bredanensis', 'Steno bredanensis (Rough-toothed dolphin)'), ('tursiops-aduncus', 'Tursiops aduncus (Indo-Pacific bottlenose dolphin)'), ('tursiops-truncatus', 'Tursiops truncatus (Offshore bottlenose dolphin)'), ('tursiops-sp', 'Tursiops sp. (Unidentified bottlenose dolphin)'), ('delphinidae-fam', 'Unidentified dolphin'), ('balaenoptera-acutorostrata', 'Balaenoptera acutorostrata (Dwarf minke whale)'), ('balaenoptera-bonaerensis', 'Balaenoptera bonaerensis (Antarctic minke whale)'), ('balaenoptera-borealis', 'Balaenoptera borealis (Sei whale)'), ('balaenoptera-edeni', "Balaenoptera edeni (Bryde's whale)"), ('balaenoptera-musculus', 'Balaenoptera musculus (Blue whale)'), ('balaenoptera-musculus-brevicauda', 'Balaenoptera musculus brevicauda (Pygmy blue whale)'), ('balaenoptera-physalus', 'Balaenoptera physalus (Fin whale)'), ('balaenoptera-omurai', "Balaenoptera omurai (Omura's whale)"), ('balaenoptera-sp', 'Balaenoptera sp. (Unidentified Balaenoptera)'), ('caperea-marginata', 'Caperea marginata (Pygmy Right Whale)'), ('eubalaena-australis', 'Eubalaena australis (Southern right whale)'), ('feresa-attenuata', 'Feresa attenuata (Pygmy killer whale)'), ('globicephala-macrorhynchus', 'Globicephala macrorhynchus (Short-finned pilot whale)'), ('globicephala-melas', 'Globicephala melas (Long-finned pilot whale)'), ('globicephala-sp', 'Globicephala sp. (Unidentified pilot whale)'), ('indopacetus-pacificus', "Indopacetus pacificus (Longman's beaked whale)"), ('kogia-breviceps', 'Kogia breviceps (Pygmy sperm whale)'), ('kogia-sima', 'Kogia sima (Dwarf sperm whale)'), ('kogia-sp', 'Kogia sp. (Unidentified small sperm whale)'), ('megaptera-novaeangliae', 'Megaptera novaeangliae (Humpback whale)'), ('mesoplodon-bowdoini', "Mesoplodon bowdoini (Andew's beaked whale)"), ('mesoplodon-densirostris', "Mesoplodon densirostris (Blainville's beaked whale)"), ('mesoplodon-grayi', "Mesoplodon grayi (Gray's beaked whale)"), ('mesoplodon-hectori', "Mesoplodon hectori (Hector's beaked whale"), ('mesoplodon-layardii', 'Mesoplodon layardii (Strap-toothed whale)'), ('mesoplodon-mirus', "Mesoplodon mirus (True's beaked whale)"), ('mesoplodon-sp', 'Mesoplodon sp. (Beaked whale)'), ('berardius-arnuxii', 'Berardius arnuxii (Giant beaked whale)'), ('orcinus-orca', 'Orcinus orca (Killer whale)'), ('peponocephala-electra', 'Peponocephala electra (Melon-headed whale)'), ('physeter-macrocephalus', 'Physeter macrocephalus (Sperm whale)'), ('pseudorca-crassidens', 'Pseudorca crassidens (False killer whale)'), ('ziphius-cavirostris', "Ziphius cavirostris (Cuvier's beaked whale)"), ('tasmacetus-shepherdi', "Tasmacetus shepherdi (Shepherd's beaked whale)"), ('cetacea', 'Unidentified whale'), ('dugong-dugon', 'Dugong dugon (Dugong)'), ('arctocephalus-forsteri', 'Arctocephalus forsteri (New Zealand fur seal)'), ('neophoca-cinerea', 'Neophoca cinerea (Australian sea lion)'), ('arctocephalus-tropicalis', 'Arctocephalus tropicalis (Subantarctic fur seal)'), ('hydrurga-leptonyx', 'Hydrurga leptonyx (Leopard seal)'), ('lobodon-carcinophagus', 'Lobodon carcinophagus (Crabeater seal)'), ('mirounga-leonina', 'Mirounga leonina (Southern elephant seal)'), ('pinnipedia', 'Unidentified pinniped'), ('hydrophiinae-subfam', 'Hydrophiinae subfam. (Sea snakes and kraits)'), ('acalyptophis-sp', 'Acalyptophis sp. (Horned sea snake)'), ('aipysurus-sp', 'Aipysurus sp. (Olive sea snake)'), ('astrotia-sp', "Astrotia sp. (Stokes' sea snake)"), ('emydocephalus-sp', 'Emydocephalus sp. (Turtlehead sea snake)'), ('enhydrina-sp', 'Enhydrina sp. (Beaked sea snake)'), ('ephalophis-sp', "Ephalophis sp. (Grey's mudsnake)"), ('hydrelaps-sp', 'Hydrelaps sp. (Port Darwin mudsnake)'), ('hydrophis-sp', 'Hydrophis sp. (sea snake)'), ('kerilia-sp', "Kerilia sp. (Jerdon's sea snake)"), ('kolpophis-sp', 'Kolpophis sp. (bighead sea snake)'), ('lapemis-sp', "Lapemis sp. (Shaw's sea snake)"), ('laticauda-sp', 'Laticauda sp. (Sea krait)'), ('parahydrophis-sp', 'Parahydrophis (Northern mangrove sea snake)'), ('parapistocalamus-sp', "Parapistocalamus sp. (Hediger's snake)"), ('pelamis-sp', 'Pelamis sp. (Yellow-bellied sea snake)'), ('praescutata-sp', 'Praescutata sp. (Sea snake)'), ('thalassophis-sp', 'Thalassophis sp. (Sea snake)')], default='na', help_text='The species of the animal.', max_length=300, verbose_name='Species'),
        ),
        migrations.AlterField(
            model_name='animalencounter',
            name='taxon',
            field=models.CharField(choices=[('na', 'Not applicable'), ('Cheloniidae', 'Marine turtles'), ('Cetacea', 'Whales and Dolphins'), ('Pinnipedia', 'Seals'), ('Sirenia', 'Dugongs'), ('Elasmobranchii', 'Sharks and Rays'), ('Hydrophiinae', 'Sea snakes and kraits')], default='Cheloniidae', help_text='The taxonomic group of the animal.', max_length=300, verbose_name='Taxonomic group'),
        ),
        migrations.AlterField(
            model_name='tagobservation',
            name='name',
            field=models.CharField(db_index=True, help_text='The ID/serial number of the tag', max_length=1000, verbose_name='Tag ID'),
        ),
        migrations.AlterField(
            model_name='turtlehatchlingemergenceobservation',
            name='hatchling_emergence_time_accuracy',
            field=models.CharField(blank=True, choices=[('na', 'Not applicable'), ('same-night', 'Sometime that night'), ('plusminus-2h', 'Plus/minus 2h of estimate'), ('plusminus-30m', 'Correct to the hour')], default='na', max_length=300, null=True, verbose_name='Hatchling emergence time estimate accuracy'),
        ),
        migrations.AlterField(
            model_name='turtlehatchlingemergenceobservation',
            name='light_sources_present',
            field=models.CharField(choices=[('na', 'Not applicable'), ('absent', 'Absent'), ('present', 'Present'), ('yes', 'Yes'), ('no', 'No')], default='na', max_length=300, verbose_name='Light sources present during emergence'),
        ),
        migrations.AlterField(
            model_name='turtlehatchlingemergenceobservation',
            name='outlier_tracks_present',
            field=models.CharField(choices=[('na', 'Not applicable'), ('absent', 'Absent'), ('present', 'Present'), ('yes', 'Yes'), ('no', 'No')], default='na', max_length=300, verbose_name='Outlier tracks present'),
        ),
        migrations.AlterField(
            model_name='turtlenestdisturbanceobservation',
            name='disturbance_cause_confidence',
            field=models.CharField(choices=[('na', 'Not applicable'), ('guess', 'Guess based on insuffient evidence'), ('expert-opinion', 'Expert opinion based on available evidence'), ('validated', 'Validated by authoritative source')], default='na', help_text='What is the choice of disturbance cause based on?', max_length=300, verbose_name='Disturbance cause choice confidence'),
        ),
        migrations.AlterField(
            model_name='turtlenestencounter',
            name='disturbance',
            field=models.CharField(choices=[('na', 'Not applicable'), ('absent', 'Absent'), ('present', 'Present'), ('yes', 'Yes'), ('no', 'No')], default='na', help_text='Is there evidence of predation or other disturbance?', max_length=300, verbose_name='Evidence of predation or disturbance'),
        ),
        migrations.AlterField(
            model_name='turtlenestencounter',
            name='eggs_counted',
            field=models.CharField(choices=[('na', 'Not applicable'), ('absent', 'Absent'), ('present', 'Present'), ('yes', 'Yes'), ('no', 'No')], default='na', help_text='Was the nest excavated and were turtle eggs counted?', max_length=300, verbose_name='Nest excavated and eggs counted'),
        ),
        migrations.AlterField(
            model_name='turtlenestencounter',
            name='fan_angles_measured',
            field=models.CharField(choices=[('na', 'Not applicable'), ('absent', 'Absent'), ('present', 'Present'), ('yes', 'Yes'), ('no', 'No')], default='na', help_text='Were hatchling emergence track fan angles recorded?', max_length=300, verbose_name='Hatchling emergence recorded'),
        ),
        migrations.AlterField(
            model_name='turtlenestencounter',
            name='hatchlings_measured',
            field=models.CharField(choices=[('na', 'Not applicable'), ('absent', 'Absent'), ('present', 'Present'), ('yes', 'Yes'), ('no', 'No')], default='na', help_text='Were turtle hatchlings encountered and their morphometrics measured?', max_length=300, verbose_name='Hatchlings measured'),
        ),
        migrations.AlterField(
            model_name='turtlenestencounter',
            name='logger_found',
            field=models.CharField(choices=[('na', 'Not applicable'), ('absent', 'Absent'), ('present', 'Present'), ('yes', 'Yes'), ('no', 'No')], default='na', help_text='Was a data logger deployed, retrieved, or otherwise encountered?', max_length=300, verbose_name='Logger present'),
        ),
        migrations.AlterField(
            model_name='turtlenestencounter',
            name='nest_tagged',
            field=models.CharField(choices=[('na', 'Not applicable'), ('absent', 'Absent'), ('present', 'Present'), ('yes', 'Yes'), ('no', 'No')], default='na', help_text='Was a nest tag applied, re-sighted, or otherwise encountered?', max_length=300, verbose_name='Nest tag present'),
        ),
        migrations.AlterField(
            model_name='turtletrackobservation',
            name='tail_pokes',
            field=models.CharField(blank=True, choices=[('absent', 'Absent'), ('occasional', 'Occasional'), ('regular', 'Regular'), ('na', 'Not applicable')], help_text='Are regular dips in the middle of the track present?', max_length=300, null=True),
        ),
    ]
