import re
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from core.models import *

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

@login_required
def updatepackage(request):
    return render(request, 'admin/form/packageupdate.html')

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

# to update driver detail
@login_required
def updatedriver(request):
    return render(request, 'admin/form/driverupdate.html')

