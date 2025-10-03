from django.contrib.auth.models import User
from django.db import models
from django.utils import timezone
import uuid

# Create your models here.
class BaseModel(models.Model):
    uid = models.UUIDField(default=uuid.uuid4, editable=False, primary_key=True)
    created_at = models.DateField(auto_now_add=True)
    updated_at = models.DateField(auto_now_add=True)

    class Meta:
        abstract = True

# Hotel
class Room(BaseModel):
    room_name = models.CharField(max_length=100)
    room_price = models.IntegerField(default=0)
    room_count = models.IntegerField(default=10)

    def __str__(self):
        return self.room_name

# HotelBooking
class RoomBooking(BaseModel):
    room = models.ForeignKey('hsp1.Room', related_name="room_bookings", on_delete=models.CASCADE)
    name = models.CharField(max_length=100, default="John Doe")
    email = models.EmailField(default="default@example.com")
    nationality = models.CharField(max_length=100, default="1234567890")
    national_id_number = models.CharField(max_length=20, default="1234567890")
    start_date = models.DateField()
    end_date = models.DateField()


class HotelImages(BaseModel):
    room = models.ForeignKey(Room, related_name="images", on_delete=models.CASCADE)
    images = models.ImageField(upload_to="images")

    def __str__(self):
        return f"Image for {self.room.room_name}"
