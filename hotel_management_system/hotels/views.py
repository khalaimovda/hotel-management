from django.conf import settings
from django.core.paginator import Paginator
from django.db.models import ObjectDoesNotExist
from django.http import HttpResponse, HttpRequest, Http404
from django.shortcuts import render, redirect
from django.views.decorators.http import require_GET

from .models import City, Hotel


@require_GET
def index(request: HttpRequest) -> HttpResponse:
    return redirect(to=cities)


@require_GET
def cities(request: HttpRequest) -> HttpResponse:
    search = request.GET.get('search')
    if search:
        cities = City.objects.filter(name__icontains=search)
    else:
        cities = City.objects.all()
    cities = cities.order_by('code', 'name')
    paginator = Paginator(object_list=cities, per_page=settings.ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    cities = paginator.get_page(page_number)
    data = {
        'title': 'Cities',
        'search': search,
        'cities': cities,
    }
    return render(request=request, template_name='hotels/cities.html', context=data)


@require_GET
def hotels(request: HttpRequest, city_code: str) -> HttpResponse:
    try:
        city = City.objects.get(code=city_code)
    except ObjectDoesNotExist as e:
        raise Http404('City code does not exist')

    search = request.GET.get('search')
    if search:
        hotels = Hotel.objects.filter(city__code=city_code, name__icontains=search)
    else:
        hotels = Hotel.objects.filter(city__code=city_code)

    # I understand that this sorting is by digits (not numbers)
    # This can be adjusted if the code format for hotels is clearly defined
    hotels = hotels.order_by('code', 'name')

    paginator = Paginator(object_list=hotels, per_page=settings.ITEMS_PER_PAGE)
    page_number = request.GET.get('page')
    hotels = paginator.get_page(page_number)
    data = {
        'title': 'Hotels',
        'search': search,
        'city': city,
        'hotels': hotels,
    }
    return render(request=request, template_name='hotels/hotels.html', context=data)
