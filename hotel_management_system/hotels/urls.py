from django.urls import path

from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('cities/', views.cities, name='cities'),
    path('cities/<slug:city_code>/hotels', views.hotels, name='hotels'),
]
