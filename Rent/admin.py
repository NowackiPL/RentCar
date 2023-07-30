from django.contrib import admin
from django.contrib.admin import ModelAdmin

from .models import Car, Client, Rent, CompanyBranches


# Register your models here.

class CarAdmin(ModelAdmin):
    ordering = ['id']
    list_display = ['id', 'brand', 'model', 'cars_type', 'engine', 'capacity', 'year', 'number_of_seats', 'Consumption',
                    'power', 'car_mileage', 'transmission', 'drive', 'price', 'deposit']


admin.site.register(Car, CarAdmin)
admin.site.register(Client)
admin.site.register(Rent)
admin.site.register(CompanyBranches)
