from django.contrib import admin

from .models import City, Hotel


@admin.register(Hotel)
class HotelAdmin(admin.ModelAdmin):
    list_display = ('code', 'name', 'city')
    search_fields = ('code', 'name')


class HotelInline(admin.TabularInline):
    model = Hotel
    extra = 0


@admin.register(City)
class CityAdmin(admin.ModelAdmin):
    list_display = ('code', 'name')
    search_fields = ('code', 'name')

    inlines = [HotelInline]
