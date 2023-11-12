from django.http import JsonResponse
from django.db.models import F, Value
from django.db.models.functions import Concat
from .models import City, State

def search_locations(request):
    query = request.GET.get('query', '')
    if not query:
        return JsonResponse({'error': 'Missing query parameter'}, status=400)
    
    city_results = City.objects.filter(name__icontains=query).annotate(
        full_name=Concat('name', Value(', '), 'state__name')
    )
    state_results = State.objects.filter(name__icontains=query).annotate(
        full_name=F('name')
    )
    data = {
        'locations': list(city_results.values('full_name')) + list(state_results.values('full_name')),
    }
    return JsonResponse(data, safe=False)