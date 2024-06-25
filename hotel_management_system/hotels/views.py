from django.http import HttpResponse, HttpRequest, Http404
from django.shortcuts import render, redirect
from django.core.paginator import Paginator
from django.db.models import ObjectDoesNotExist

from .models import City, Hotel


def index(request: HttpRequest) -> HttpResponse:
    return redirect(to=cities)


def cities(request: HttpRequest) -> HttpResponse:
    cities = City.objects.all()
    paginator = Paginator(object_list=cities, per_page=1)
    page_number = request.GET.get('page')
    cities = paginator.get_page(page_number)
    data = {
        'title': 'Cities',
        'cities': cities,
    }
    return render(request=request, template_name='hotels/cities.html', context=data)


def hotels(request: HttpRequest, city_code: str) -> HttpResponse:
    try:
        city = City.objects.get(code=city_code)
    except ObjectDoesNotExist as e:
        raise Http404('City code does not exist')
    hotels = Hotel.objects.filter(city__code=city_code)
    paginator = Paginator(object_list=hotels, per_page=1)
    page_number = request.GET.get('page')
    hotels = paginator.get_page(page_number)
    data = {
        'title': 'Hotels',
        'city': city,
        'hotels': hotels,
    }
    return render(request=request, template_name='hotels/hotels.html', context=data)
