from django.core.cache import cache
from .models import Property

def get_all_properties():
    """
    Retrieves all properties with caching.
    - Checks Redis for 'all_properties'.
    - If not cached, fetch from DB and store in cache for 1 hour.
    """
    all_properties = cache.get('all_properties')

    if all_properties is None:
        all_properties = list(Property.objects.all().values())  # convert to list of dicts for serialization
        cache.set('all_properties', all_properties, 3600)  # cache for 1 hour (3600s)

    return all_properties