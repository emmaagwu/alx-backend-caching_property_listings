from django.http import JsonResponse
from django.views.decorators.cache import cache_page
from django.utils.decorators import method_decorator
from django.views import View
from .models import Property

@cache_page(60 * 15)  # cache for 15 minutes
def property_list(request):
    properties = Property.objects.all().values()  # returns QuerySet of dicts
    return JsonResponse({
        "data": list(properties)  # wrap results under "data"
    }, safe=False)
