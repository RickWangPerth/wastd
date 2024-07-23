# utils.py
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from .models import TrtTags, TrtPitTags, TrtPersons, TrtPlaces

CACHE_TIMEOUT = 60 * 60  # 60 minutes

def get_cached_queryset(model, filter_kwargs=None):
    cache_key = f"{model.__name__}_queryset"
    queryset = cache.get(cache_key)
    if not queryset:
        if filter_kwargs:
            queryset = model.objects.filter(**filter_kwargs)
        else:
            queryset = model.objects.all()
        cache.set(cache_key, queryset, CACHE_TIMEOUT)
    return queryset

def clear_cache(model):
    cache_key = f"{model.__name__}_queryset"
    cache.delete(cache_key)

@receiver(post_save, sender=TrtTags)
@receiver(post_delete, sender=TrtTags)
@receiver(post_save, sender=TrtPitTags)
@receiver(post_delete, sender=TrtPitTags)
@receiver(post_save, sender=TrtPersons)
@receiver(post_delete, sender=TrtPersons)
@receiver(post_save, sender=TrtPlaces)
@receiver(post_delete, sender=TrtPlaces)
def clear_model_cache(sender, **kwargs):
    clear_cache(sender)
    
def initialize_signals():
    # This function is intentionally left empty.
    # Its purpose is to ensure that the signal handlers are registered.
    pass

import logging

logger = logging.getLogger(__name__)

def get_cached_queryset(model, filter_kwargs=None):
    cache_key = f"{model.__name__}_queryset"
    queryset = cache.get(cache_key)
    if queryset:
        logger.debug(f"Cache hit for {cache_key}")
    else:
        if filter_kwargs:
            queryset = model.objects.filter(**filter_kwargs)
        else:
            queryset = model.objects.all()
        cache.set(cache_key, queryset, CACHE_TIMEOUT)
        logger.debug(f"Cache set for {cache_key}")
    return queryset
