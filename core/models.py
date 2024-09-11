from django.db import models
from django.contrib.auth.models import User

# database schema for packages details
class Package(models.Model):
    packageId = models.AutoField(primary_key=True)
    packagename = models.CharField(max_length=255, verbose_name="Package Name", null=True, blank=False, default="Blank")
    duration = models.CharField(max_length=200, verbose_name="Duration", null=True, blank=False, default="Blank")
    dateoftour = models.DateField(verbose_name="Date of Tour", null=True, blank=False)
    price = models.IntegerField(verbose_name="Price of Package", null=True, blank=False)
    packagedescription = models.CharField(max_length=10000, verbose_name="Package Description", null=True, blank=False, default="Blank")
    image = models.ImageField(upload_to="packages/images", verbose_name="Images", null=True, blank=False, default='')

    def __str__(self):
        return f"{self.packageId} - {self.packagename}"

# database schema for driver details
class Driver(models.Model):
    gender_choices = (
        ('Male', 'Male'),
        ('Female', 'Female'),
        ('Others', 'Others')
    )

    driverId = models.AutoField(primary_key=True)
    drivername = models.CharField(max_length=255, verbose_name="Driver Name", null=True, blank=False, default="")
    gender = models.CharField(max_length=20, verbose_name="Gender", null=True, blank=False, default="", choices=gender_choices)
    phone_number = models.CharField(max_length=20, verbose_name="Phone Number", null=True, blank=False, default="")
    vehicle_name = models.CharField(max_length=255, verbose_name="Vehicle Name", null=True, blank=False, default="")
    vehicle_number = models.CharField(max_length=255, verbose_name="Vehicle Number", null=True, blank=False, default="")

    def __str__(self):
        return f"{self.vehicle_number} - {self.drivername}"
    

# Creating different roles for the users
class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    driver_management = models.BooleanField(default=False)
    package_management = models.BooleanField(default=False) 
    hotel_management = models.BooleanField(default=False)
    air_ticketing_management = models.BooleanField(default=False)

    def __str__(self):
        return self.user.username
    


# database schema for hotel details
class Hotel(models.Model):
    hotelId = models.AutoField(primary_key=True)
    hotelname = models.CharField(max_length=255, verbose_name="Hotel Name", null=True, blank=False, default="")
    location = models.CharField(max_length=255, verbose_name="Location", null=True, blank=False, default="")
    rating = models.DecimalField(max_digits=3, decimal_places=1, verbose_name="Rating", null=True, blank=False)
    price_per_night = models.IntegerField(verbose_name="Price Per Night", null=True, blank=False)
    hotel_description = models.CharField(max_length=5000, verbose_name="Hotel Description", null=True, blank=False, default="")
    image = models.ImageField(upload_to="hotels/images", verbose_name="Images", null=True, blank=False, default='')

    def __str__(self):
        return f"{self.hotelId} - {self.hotelname}"


# database schema for air ticket details
class AirTicket(models.Model):
    airline = models.CharField(max_length=255, verbose_name="Airline", null=True, blank=False, default="")
    departure = models.CharField(max_length=255, verbose_name="Departure Location", null=True, blank=False, default="")
    destination = models.CharField(max_length=255, verbose_name="Destination", null=True, blank=False, default="")
    date_of_flight = models.DateField(verbose_name="Date of Flight", null=True, blank=False)
    price = models.IntegerField(verbose_name="Price of Ticket", null=True, blank=False)
    flight_number = models.CharField(max_length=50, verbose_name="Ticket Number", null=True, blank=False, default="")
    airline_logo = models.ImageField(upload_to='airline_logos/images', null=True, blank=True, verbose_name="Airline Logo")


    def __str__(self):
        return f"{self.airline} - Flight {self.flight_number} ({self.departure} to {self.destination})"

