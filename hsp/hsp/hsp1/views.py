from django.shortcuts import render, redirect,HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
# below import is done for sending emails
from django.conf import settings
from django.core.mail import send_mail
from django.core import mail
from django.core.mail.message import EmailMessage
from django.template.loader import render_to_string
from django.http import HttpResponseRedirect
from datetime import datetime
from .models import (Room,RoomBooking)
def index(request):
    return render(request,'index.html')
def check_booking(start_date  , end_date ,uid , room_count):
    qs = RoomBooking.objects.filter(
        start_date__lte=start_date,
        end_date__gte=end_date,
        room__uid = uid
        )
    
    if len(qs) >= room_count:
        return False
    
    return True
def form(request, uid):
    room= Room.objects.get(uid=uid)
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        nationality = request.POST.get('nationality')
        nationalid= request.POST.get('nationalid')
        checkin = request.POST.get('checkin')
        checkout = request.POST.get('checkout')
        hotel = Room.objects.get(uid = uid)
        if not check_booking(checkin ,checkout  , uid , hotel.room_count):
            messages.warning(request, 'SORRY ! Hotel is already booked in these dates. ' 'Try For Another Dates')
            print("Warning message set!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        RoomBooking.objects.create(room=hotel ,  name=name, email= email, nationality= nationality,
         national_id_number=nationalid,start_date=checkin, end_date = checkout)
        
         # emails sending starts from here
        from_email=settings.EMAIL_HOST_USER
        connection=mail.get_connection()
        connection.open()
        email_message=mail.EmailMessage(f'Email from {name}',f'UserEmail : {email}\nCheckinDate : {checkin}\nCkeckoutDate : {checkout}\nRoomName : {hotel}\nDue Amount : {hotel.room_price}',from_email,['fahmidayasmin099@gmail.com'],connection=connection)
        email_client=mail.EmailMessage('Your Booking Information',f'Client Name : {name}\nUserEmail : {email}\nCheckinDate : {checkin}\nCkeckoutDate : {checkout}\nRoomName : {hotel}\nDue Amount : {hotel.room_price}',from_email,[email],connection=connection)
        connection.send_messages([email_message,email_client])
        connection.close()
        messages.success(request, 'Your Booking Has Been Done. ' 'Thank You')
        print("Success message set!") 
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
        

    context = {'room': room}
    return render(request, 'form.html', context)           

def room(request):
    # Get the check-in and check-out dates from the request
    checkin = request.GET.get('checkin')
    checkout = request.GET.get('checkout')

    # Convert the date strings to datetime objects
    checkin_date = datetime.strptime(checkin, "%Y-%m-%d").date() if checkin else None
    checkout_date = datetime.strptime(checkout, "%Y-%m-%d").date() if checkout else None

    # Get all rooms
    rooms_objs = Room.objects.all()
    # If both check-in and check-out dates are provided, filter available rooms
    if checkin_date and checkout_date:
        available_rooms = []
        for room in rooms_objs:
            if check_booking(checkin_date, checkout_date, room.uid, room.room_count):
                available_rooms.append(room)
        context = {'rooms_objs': available_rooms, 'checkin': checkin, 'checkout': checkout}
    else:
        context = {'rooms_objs': rooms_objs, 'checkin': checkin, 'checkout': checkout}

    return render(request, 'room.html', context)
def resturent(request):
    return render(request,'resturent.html')
def contact(request):
    return render(request,'contact.html')
def success(request):
    return render(request,'success.html')