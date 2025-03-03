from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Booking(models.Model):
    id = models.AutoField(primary_key=True)
    user_id = models.ForeignKey(User, on_delete=models.DO_NOTHING)
    name = models.CharField(max_length=255)
    no_of_guests = models.IntegerField()
    bookingDate = models.DateField()
    reservation_time = models.SmallIntegerField()
    

class Menu(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=255)
    description = models.TextField(max_length=500)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    inventory = models.IntegerField()
    
    def get_item(self):
        return '{self.title} : {self.price}'
    
    def __str__(self):
        return self.title
    

    