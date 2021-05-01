from django import forms

from .models import parking_slot, Vehicle, Booking_model
from account.models import Account

class parkingForm(forms.ModelForm) :
    vehicle_id = forms.ModelChoiceField(queryset=Vehicle.objects.all(), empty_label="(Nothing)", required=False)
    class Meta :
        model = parking_slot
        fields = ('slot_id', 'is_occupied', 'vehicle_id', 'end_time')

class SlotBookingForm(forms.ModelForm) :
    slot_id = forms.CharField(max_length=10, disabled=True)
    username = forms.CharField(max_length=20, disabled=True)
    end_time = forms.TimeField()
    # the_owner = Account.objects.get(username="user1")

    class Meta :
        model = Booking_model
        fields = ('username', 'slot_id', 'want_to_book_the_slot', 'vehicle_id', 'end_time')


class add_vehicle_form(forms.ModelForm) :
    class Meta :
        model = Vehicle
        fields = ('vehicle_id', 'company', 'vehicle_model')

class changeParkingForm(forms.ModelForm) :
    vehicle_id = forms.CharField(max_length=20, disabled=True)
    slot_id = forms.CharField(max_length=10, disabled=True)

    # vehicle_id = forms.ModelChoiceField(queryset=Vehicle.objects.all(), empty_label="(Nothing)", required=False, dis)
    class Meta :
        model = parking_slot
        fields = ('slot_id', 'is_occupied', 'vehicle_id', 'end_time')

    def save(self) :
        print("saving")
        print(self.is_valid())