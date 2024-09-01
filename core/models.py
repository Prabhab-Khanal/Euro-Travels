from django.db import models
from django.utils import timezone

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