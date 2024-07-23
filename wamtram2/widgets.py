# widgets.py
from django_select2.forms import ModelSelect2Widget
from .models import TrtTags, TrtPitTags, TrtPersons, TrtPlaces
from .utils import get_cached_queryset

# Custom widget with caching mechanism
class CachedModelSelect2Widget(ModelSelect2Widget):
    def __init__(self, queryset, *args, **kwargs):
        super().__init__(queryset=queryset, *args, **kwargs)
        self.queryset = queryset

    def filter_queryset(self, term, queryset=None, **dependent_fields):
        if queryset is None:
            queryset = get_cached_queryset(self.model)
        return super().filter_queryset(term, queryset=queryset, **dependent_fields)

    
    def get_queryset(self):
        return get_cached_queryset(self.model)

tagWidget = ModelSelect2Widget(
    queryset=TrtTags.objects.all(),
    model=TrtTags,
    search_fields=[
        "tag_id__icontains",
    ],
)

unAssignedTagWidget = ModelSelect2Widget(
    queryset=TrtTags.objects.filter(tag_status="U"),
    model=TrtTags,
    search_fields=[
        "tag_id__icontains",
    ],
)

pitTagWidget = ModelSelect2Widget(
    queryset=TrtPitTags.objects.all(),
    model=TrtPitTags,
    search_fields=[
        "pittag_id__icontains",
    ],
)

unassignedPitTagWidget = ModelSelect2Widget(
    queryset=TrtPitTags.objects.filter(pit_tag_status="U"),
    model=TrtPitTags,
    search_fields=[
        "pittag_id__icontains",
    ],
)

personWidget = CachedModelSelect2Widget(
    queryset=TrtPersons.objects.all(),
    model=TrtPersons,
    search_fields=["first_name__icontains", "surname__icontains"],
)

placeWidget = CachedModelSelect2Widget(
    queryset=TrtPlaces.objects.all(),
    model=TrtPlaces,
    search_fields=["place_name__icontains", "location_code__location_name__icontains"],
    attrs={'data-required': 'true'} 
)

# Custom widget that combines TrtTags and TrtPitTags
class CustomModelSelect2Widget(ModelSelect2Widget):
    model = TrtTags  # Default model

    def filter_queryset(self, request, term, queryset=None, **dependent_fields):
        trt_tags = TrtTags.objects.filter(tag_id__icontains=term)
        trt_pit_tags = TrtPitTags.objects.filter(pittag_id__icontains=term)
        return list(trt_pit_tags) + list(trt_tags)

    def get_queryset(self):
        return self.model.objects.all()
