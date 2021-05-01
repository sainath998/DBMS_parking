from django.shortcuts import render

from .models import parking_slot, SLOT_COLUMN, SLOT_ROW, Vehicle, Booking_model

from django.template.defaulttags import register

from .forms import SlotBookingForm, add_vehicle_form, changeParkingForm

from django.shortcuts import redirect

from account.models import Account

from datetime import datetime, date

# Create your views here.
# home view,
def home_view(request):
    return render(request, 'siteHome.html', {})

def user_home_view(request):
    context = {}
    
    if request.user.is_authenticated :
        # print(Booking_model.objects.all())
        the_vehicles = Vehicle.objects.filter(owner=request.user)
        context['the_vehicles'] = the_vehicles

        for the_vehicle in the_vehicles :
            if the_vehicle.parked :
                the_slot = parking_slot.objects.get(slot_id=the_vehicle.parked_slot_id)
                now = datetime.now().time() # time object
                print("curr time : " + str(now))
                print("end time : " + str(the_slot.end_time))
                if now > the_slot.end_time :
                    print("late")
                    
                    the_vehicle.parked = False
                    the_vehicle.parked_slot_id = None
                    the_vehicle.save()
                    
                    the_slot.is_occupied = False
                    the_slot.vehicle_id = None
                    the_slot.save()
                else :
                    print("not late")

    return render(request, 'userHome.html', context)


def aboutus_view(request) :
    return render(request, 'aboutus.html', {})

def slot_status_view(request) :
    context = {}
    context['slots'] = parking_slot.objects.all()
    context['col'] = SLOT_COLUMN
    context['row'] = SLOT_ROW
    return render(request, 'personal/slot_status.html', context)

@register.filter
def my_get(i, j) :
    slots = parking_slot.objects.all()
    ind1 = i - 1
    ind2 = j - 1
    slot_ind = ind1*8 + ind2
    return slots[slot_ind]

def slot_booking_view(request, slot_id) :
    context = {}
    username = request.user.username
    try :
        the_owner = Account.objects.get(username=username)
    except Account.DoesNotExist :
        the_owner = None

    now = datetime.now().time() # time object

    if request.POST :
        form = SlotBookingForm(request.POST, initial={'slot_id' : slot_id, 'username' : username})

        if form.is_valid() :
            form.save()

            the_vehicle_id = request.POST['vehicle_id']
            the_vehicles = Vehicle.objects.filter(owner=request.user)

            vehicle_flag = False

            for vehicle in the_vehicles :
                if the_vehicle_id == vehicle.vehicle_id :
                    vehicle_flag = True
                    break

            if vehicle_flag :
                the_vehicle = Vehicle.objects.get(vehicle_id=the_vehicle_id)

                # check if this vehcile is not parked,
                if the_vehicle.parked :
                    print("vehicle already parked")
                    return redirect('userHome')
                else :
                    print("vehicle not parked")
                    # update the_vehicle object,
                    the_vehicle.parked = True
                    the_vehicle.parked_slot_id = slot_id
                     # after updating save in DB,
                    the_vehicle.save()
                    print(the_vehicle.parked)

                    # print("1")
                    # print(Booking_model.objects.all())


                    # update the user's 'booked_slot' field,
                    the_slot = parking_slot.objects.get(slot_id=slot_id)
                    the_slot.booked_time = now
                    the_slot.is_occupied = True
                    the_slot.vehicle_id = the_vehicle_id
                    the_slot.end_time = request.POST['end_time']
                    print("availabe increment " + str(the_slot.available_increment))
                    end_time_time = datetime.strptime(the_slot.end_time, '%H:%M').time()
                    if now > end_time_time :          # not supported operand,
                        print("not future time")
                        return redirect('userHome')
                    print("future time")
                    the_slot.save()
                    print(the_slot.vehicle_id + " " + str(the_slot.end_time))

                    # print("2")
                    # print(Booking_model.objects.all())

                    # create a new booking,
                    booking = Booking_model(
                        booking_id = "bkng" + str(slot_id) + str(the_vehicle_id),
                        vehicle_id=the_slot.vehicle_id,
                        slot_id = slot_id,
                        want_to_book_the_slot=True,
                        username=request.user.username,
                        # booked_time = now,
                    )

                    # print("3")
                    # print(Booking_model.objects.all())

                    # booking.booking_id = "bkng" + str(slot_id) + str(the_vehicle_id)
                    booking.save()

                    # print("4")
                    # print(Booking_model.objects.all())

                    # print(booking)

                    # print("5")
                    # print(Booking_model.objects.all())

                    return redirect('userHome')
                    # return render(request, 'userHome.html', context)

            else :
                print("no vehicle")
                # context['booking_form'] = form
                return redirect('userHome')

        else :
            print("not valid")
            context['booking_form'] = form

    else :
        form = SlotBookingForm(initial={'slot_id' : slot_id, 'username' : username})
        context['booking_form'] = form
    
    return render(request, 'personal/slot_booking.html', context)


def add_vehicle_view(request) :
    context = {}

    if request.POST :
        form = add_vehicle_form(request.POST)

        if form.is_valid() :
            form.save()

            the_vehicle = Vehicle(
                vehicle_id = request.POST['vehicle_id'],
                company = request.POST['company'],
                vehicle_model = request.POST['vehicle_model'],
                owner = request.user
            )

            the_vehicle.save()

            return redirect('userHome')

        else :
            context['add_vehicle_form'] = form

    else :
        form = add_vehicle_form()
        context['add_vehicle_form'] = form

    return render(request, 'personal/add_vehicle.html', context)


def all_vehicles_view(request) :
    vehicles = Vehicle.objects.filter(owner=request.user)
    context = {}
    context['vehicles'] = vehicles

    return render(request, 'personal/all_vehicles.html', context)

def all_bookings_view(request) :
    bookings = Booking_model.objects.all()
    context = {}
    context['bookings'] = bookings

    return render(request, 'personal/all_bookings.html', context)


def changeParkingView(request, parked_slot_id) :
    context = {}
    the_vehicle = Vehicle.objects.get(parked_slot_id=parked_slot_id)
    the_slot = parking_slot.objects.get(slot_id=parked_slot_id)
    actual_end_time = the_slot.end_time
    now = datetime.now().time() # time object
    # the_vehicle = queryset.first()

    if request.POST :
        print("post")
        form = changeParkingForm(request.POST, instance = the_vehicle)
        print(request.POST.get('is_occupied') == None)
        print(request.POST.get('slt_id'))
        print(request.POST.get('end_time'))
        # print(request.POST.get('is_occupied'))
        # form.save()
        if request.POST.get('is_occupied') == None :
            # print(the_vehicle.parked)
            the_vehicle.parked = False
            # print(the_vehicle.parked)
            the_vehicle.parked_slot_id = None
            the_vehicle.save()

            
            # print(the_slot)
            the_slot.is_occupied = False
            the_slot.vehicle_id = None
            # the_slot.slot_id = None
            the_slot.save()
            # print(the_slot.is_occupied)

        else :
            print("\nnot change occ")
            print("time of booking : " + str(the_slot.booked_time))
            changed_end_time = datetime.strptime(request.POST.get('end_time'), '%H:%M:%S').time()
            if changed_end_time < actual_end_time and changed_end_time > now :
                print("time ok")
                the_slot.end_time = changed_end_time
                the_slot.save()
            else :
                if changed_end_time > actual_end_time :
                    print("ooh increasing,,,")
                    delta = datetime.combine(date.today(), changed_end_time) - datetime.combine(date.today(), actual_end_time)

                    if the_slot.available_increment - delta.seconds/60 > 0 :
                        print("\nincrement available : " + str(the_slot.available_increment))
                        print("time diff in minutes : " + str(delta.seconds/60))
                        # upadte the available_increment,
                        the_slot.available_increment = the_slot.available_increment - delta.seconds/60
                        # print("remaining : " + str(the_slot.available_increment))

                        the_slot.end_time = changed_end_time

                        the_slot.save()

                    else :
                        print("\nincrement not available")
                else :
                    print("\ntime not ok")
        print("remaining : " + str(the_slot.available_increment))
        print("now end time : " + str(the_slot.end_time))

        return redirect('userHome')

    else :
        print("else")
        form = changeParkingForm(
            initial= {
                "slot_id" : the_vehicle.parked_slot_id,
                "is_occupied" : the_vehicle.parked,
                "vehicle_id" : the_vehicle.vehicle_id,
                "end_time" : the_slot.end_time,
            }
        )
        context['changeParkingForm'] = form
    return render(request, 'personal/change_parking_status.html', context)