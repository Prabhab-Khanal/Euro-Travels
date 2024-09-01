from django.db import models
from django.utils import timezone

# database schema for packages
class Package(models.Model):
    packageId = models.AutoField(primary_key=True)
    packagename = models.CharField(max_length=255, verbose_name="Package Name", null=True, blank=False, default="Blank")
    duration = models.CharField(max_length=200, verbose_name="Duration", null=True, blank=False, default="Blank")
    dataoftour = models.DateField(verbose_name="Date of Tour", null=True, blank=False)
    price = models.IntegerField(verbose_name="Price of Package", null=True, blank=False)
    packagedescription = models.CharField(max_length=10000, verbose_name="Package Description", null=True, blank=False, default="Blank")
    image = models.ImageField(upload_to="packages/images", verbose_name="Images", null=True, blank=False, default='')

    def __str__(self):
        return f"{self.packageId} - {self.packagename}"
    