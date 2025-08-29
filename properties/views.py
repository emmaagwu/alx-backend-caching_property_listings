# properties/views.py
from django.http import JsonResponse
from .utils import get_all_properties

def property_list(request):
    """
    Returns the list of properties from cache or DB.
    """
    data = get_all_properties()
    return JsonResponse({"data": data})
