from django.db.models import Q
from .models import Photo
from django.shortcuts import render

def search_items(request):
    query = request.GET.get('q') # assuming the search query is in the "q" parameter of the request
    if query:
        items = Photo.objects.filter(Q(name__icontains=query))
        # the above query will match all items whose name contains the search query (case-insensitive)
        return render(request, 'search_results.html', {'items': items, 'query': query})
    else:
        return render(request, 'search_form.html')