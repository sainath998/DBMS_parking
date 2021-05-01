from django.contrib import admin
from .models import (
    Vehicle,
    Car,
    Bike,
    Person,
    parking_slot,
    Booking_model,
)

from .forms import parkingForm

# Register your models here.
class vehicleAdmin(admin.ModelAdmin) :
    list_display = ('vehicle_id', 'owner')
    exclude = ['parked', 'parked_slot_id',]

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class bikeAdmin(admin.ModelAdmin) :
    list_display = ('vehicle_id', 'owner')
    exclude = ['parked', 'parked_slot_id',]

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

class carAdmin(admin.ModelAdmin) :
    list_display = ('vehicle_id', 'owner')
    exclude = ['parked', 'parked_slot_id',]

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()


admin.site.register(Vehicle, vehicleAdmin)
admin.site.register(Car, carAdmin)
admin.site.register(Bike, bikeAdmin)
admin.site.register(Person)
admin.site.register(Booking_model)

class parkingSlotAdmin(admin.ModelAdmin) :
    form = parkingForm
    list_display = ('slot_id', 'is_occupied', 'vehicle_id')
    exclude = ['end_time',]

    filter_horizontal = ()
    list_filter = ()
    fieldsets = ()

admin.site.register(parking_slot, parkingSlotAdmin)
