from django.core.cache import cache
from .models import Property
import logging
from django_redis import get_redis_connection

logger = logging.getLogger(__name__)

def get_redis_cache_metrics():
    try:
        redis_conn = get_redis_connection("default")
        info = redis_conn.info("stats")

        hits = info.get("keyspace_hits", 0)
        misses = info.get("keyspace_misses", 0)
        total_requests = hits + misses
        hit_ratio = hits / total_requests if total_requests > 0 else 0

        metrics = {
            "hits": hits,
            "misses": misses,
            "hit_ratio": hit_ratio,
        }

        logger.info(f"Cache Metrics: {metrics}")
        return metrics

    except Exception as e:
        logger.error(f"Error retrieving cache metrics: {e}")
        return {"error": str(e)}



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