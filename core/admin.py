from django.contrib import admin
from core.models import *

# models of packages and drivers
admin.site.register(Package)
admin.site.register(Driver)
admin.site.register(Profile)