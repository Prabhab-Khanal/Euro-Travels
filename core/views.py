import re
import os
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import *
from django.core.files.storage import default_storage

from homepage.models import *

# logic for the login page
def adminlogin(request):
    if request.user.is_authenticated:
        return redirect('package')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Checking if username exists in the database
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_staff:
                # Successful login, redirect to package
                login(request, user)
                return redirect('package')
                      
            else:
                # Denies access if "STAFF STATUS" in database is false
                messages.error(request, "Access denied. You do not have permission to access this page.")
                return redirect('admin-login') 
            
        else:
            # Failed login, return an error message
            messages.error(request, "Username or Password does not match....")
            return redirect('admin-login')

    return render(request, 'admin/adminlogin.html')

# logs out only if user is already logged in
@login_required
def adminlogout(request):
    logout(request)
    messages.success(request, "You have been logged out successfully.")
    return redirect('admin-login')

# for admin panel
@login_required
def package(request):
    # importing data from package database
    packages = Package.objects.all()
    context = {
        'packages' : packages
    }
    
    return render(request, 'admin/package.html', context=context)


def message(request):
    # importing data from package database
    messages = Contact.objects.all()
    context = {
        'contacts' : messages
    }
    
    return render(request, 'admin/contact.html', context=context)

@login_required
def driver(request):
    # importing data from Driver database
    drivers = Driver.objects.all()
    context = {
        'drivers' : drivers
    }

    return render(request, 'admin/driver.html', context=context)

@login_required
def hotels(request):
    return render(request, 'admin/hotels.html')

@login_required
def ticket(request):
    return render(request, 'admin/ticket.html')

# to add packages
@login_required
def addpackage(request):
    if request.method == 'POST':
        packagename = request.POST.get('package_name')
        duration = request.POST.get('duration')
        dateoftour = request.POST.get('date_of_tour')
        price = request.POST.get('price')
        packagedescription = request.POST.get('package_description')
        image = request.FILES.get('package_image')

        # declaring search for the characters
        pattern = re.compile(r'[A-Za-z]')  # this declares string from A to Z and a to z
        numeric_pattern = re.compile(r'[0-9]') # this declares string from 0 to 9

        # Validation of packagename and duration
        if not pattern.search(packagename):
            messages.error(request, "Package Name should contain atleast one alphabet...")
            return render(request, 'admin/form/packageadd.html')

        if not (pattern.search(duration) and numeric_pattern.search(duration)):
            messages.error(request, "Please write full duration eg... 7 days instead of just numbers or words")
            return render(request, 'admin/form/packageadd.html')

        try:
            # Creating new instance to save package details in database
            package = Package(
                packagename=packagename,
                duration=duration,
                dateoftour=dateoftour,
                price=price,
                packagedescription=packagedescription,
                image=image
            )
            package.save()  # Saving the instance
            messages.success(request, "Package Details Saved Successfully...")
            return redirect('package')

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return render(request, 'admin/form/packageadd.html')

    return render(request, 'admin/form/packageadd.html')

# to add drivers details
@login_required
def adddriver(request):
    if request.method == 'POST':
        drivername = request.POST.get('drivername')
        gender = request.POST.get('driver_gender')
        phone_number = request.POST.get('number')
        vehicle_name = request.POST.get('vehiclename')
        vehicle_number = request.POST.get('vehiclenumber')

        pattern = re.compile(r'[A-Za-z]')  # this declares string from A to Z and a to z
        numeric_pattern = re.compile(r'[0-9]') # this declares string from 0 to 9
        special_char_pattern = re.compile(r'[!@#$%^&*(),.?":{}|<>_-]') # this declares string for special characters

        # Validation of packagename and duration
        if (numeric_pattern.search(drivername) or special_char_pattern.search(drivername)):
            messages.error(request, "Name of a person does not contain numbers or special characters...")
            return render(request, 'admin/form/packageadd.html')

        if pattern.search(phone_number) or special_char_pattern.search(phone_number):
            messages.error(request, "Phone number cannot contain alphabets or special character...")
            return render(request, 'admin/form/driveradd.html')
        
        if len(phone_number) > 10:
            messages.error(request, "Phone number be longer than 10 digits...")
            return render(request, 'admin/form/driveradd.html')

        try:
            # Creating new instance to save package details in database
            driver = Driver(
                drivername = drivername,
                gender = gender,
                phone_number = phone_number,
                vehicle_name = vehicle_name,
                vehicle_number = vehicle_number
            )
            driver.save()  # Saving the instance
            messages.success(request, "Driver Details Saved Successfully...")
            return redirect('driver')

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return render(request, 'admin/form/driveradd.html')

    return render(request, 'admin/form/driveradd.html')


'''
    Function to delete package and drivers details
'''
# for packages
@login_required
def delete_package(request, packageId):
    try:
        package = Package.objects.get(packageId = packageId)

        package.delete()
        return redirect('package')
    
    except Package.DoesNotExist:
        messages.error(request, "Package not found...")

# for drivers
@login_required
def delete_driver(request, driverId):
    try:
        driver = Driver.objects.get(driverId=driverId)

        # Delete the driver object
        driver.delete()
        messages.success(request, "Driver details deleted successfully.")
        
    except Driver.DoesNotExist:
        messages.error(request, "Driver not found...")
        
    return redirect('driver')

# to update driver detail
@login_required
def updatepackage(request, packageId):
    package = Package.objects.get(packageId = packageId)

    context = {
        'package' : package
    }

    return render(request, 'admin/form/packageupdate.html', context=context)

@login_required
def save_package_update(request, packageId):
    # Getting the package from
    if request.method == 'POST':
        # getting details from form
        name_new = request.POST.get('package_name')
        duration_new = request.POST.get('duration')
        date_new = request.POST.get('date_of_tour')
        price_new = request.POST.get('price')
        packagedescription_new = request.POST.get('package_description')

        update_set = Package.objects.get(packageId=packageId)

        # Checking if a new image is being uploaded
        if 'package_image' in request.FILES:
            image_new = request.FILES['package_image']
            package.image = image_new

        # Changing old package details to the new one
        update_set.packagename = name_new
        update_set.duration = duration_new
        update_set.dateoftour = date_new
        update_set.price = price_new
        update_set.packagedescription = packagedescription_new

        update_set.save()

        return redirect('package')

    return render(request, 'package.html')

@login_required
def updatedriver(request, driverId):
    driver = Driver.objects.get(driverId = driverId)

    context = {
        'driver' : driver
    }

    return render(request, 'admin/form/driverupdate.html', context=context)

@login_required
def save_driver_update(request, driverId):
    # Getting the package from
    if request.method == 'POST':
        # getting details from form
        name_new = request.POST.get('drivername')
        gender_new = request.POST.get('driver_gender')
        number_new = request.POST.get('number')
        vehicle_name_new = request.POST.get('vehiclename')
        vehicle_number_new = request.POST.get('vehiclenumber')

        update_set = Driver.objects.get(driverId=driverId)

        # Changing old package details to the new one
        update_set.drivername = name_new
        update_set.gender = gender_new
        update_set.phone_number = number_new
        update_set.vehicle_name = vehicle_name_new
        update_set.vehicle_number = vehicle_number_new

        update_set.save()

        return redirect('driver')

    return render(request, 'driver.html')
