import re
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required, user_passes_test
from core.models import *

'''
 The following logics are being used to make custom role which will be used to restrict different pages
 It checks if user has role of superuser and also the respective role required
'''

# For driver management role
def user_has_driver_management_role(user):
    return user.is_superuser or (hasattr(user, 'profile') and user.profile.driver_management)

# For package management role
def user_has_package_management_role(user):
    return user.is_superuser or (hasattr(user, 'profile') and user.profile.package_management)

# For hotel management role
def user_has_hotel_management_role(user):
    return user.is_superuser or (hasattr(user, 'profile') and user.profile.hotel_management)

# For air ticketing management role
def user_has_air_ticketing_management_role(user):
    return user.is_superuser or (hasattr(user, 'profile') and user.profile.air_ticketing_management)

'''
    The code given below is used for the redirection of different user in different pages---
    This will help to eliminate infinite Test done by @user_pass_test for a role until its true---
    If this function is not made then the page will not load because
    of infinite request made by @user_pass_test---
'''
def redirect_different_user(request, user):
    if user.is_superuser:
        return redirect('package')  # Redirect superuser to package page
    
    elif hasattr(user, 'profile') and user.profile.driver_management:
        return redirect('driver')  # Redirect user with driver_management role
    
    elif hasattr(user, 'profile') and user.profile.package_management:
        return redirect('package')  # Redirect user with package_management role
    
    elif hasattr(user, 'profile') and user.profile.hotel_management:
        return redirect('hotels')
    
    elif hasattr(user, 'profile') and user.profile.air_ticketing_management:
        return redirect('tickets')

    else:
        messages.error(request, "Access denied. You do not have permission to access this page.")
        return redirect('admin-login')

# logic for the login page
def adminlogin(request):
    if request.user.is_authenticated:
        return redirect_different_user(request, request.user)
    
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
@user_passes_test(user_has_package_management_role)
def package(request):
    # importing data from package database
    packages = Package.objects.all()
    context = {
        'packages' : packages
    }
    
    return render(request, 'admin/package.html', context=context)

@login_required
@user_passes_test(user_has_driver_management_role)
def driver(request):
    # importing data from Driver database
    drivers = Driver.objects.all()
    context = {
        'drivers' : drivers
    }

    return render(request, 'admin/driver.html', context=context)

@login_required
@user_passes_test(user_has_hotel_management_role)
def hotels(request):
    return render(request, 'admin/hotels.html')

@login_required
@user_passes_test(user_has_air_ticketing_management_role)
def ticket(request):
    return render(request, 'admin/ticket.html')

# to add packages
@login_required
@user_passes_test(user_has_package_management_role)
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
@user_passes_test(user_has_driver_management_role)
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
@user_passes_test(user_has_package_management_role)
def delete_package(request, packageId):
    try:
        package = Package.objects.get(packageId = packageId)

        package.delete()
        return redirect('package')
    
    except Package.DoesNotExist:
        messages.error(request, "Package not found...")

# for drivers
@login_required
@user_passes_test(user_has_driver_management_role)
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
@user_passes_test(user_has_package_management_role)
def updatepackage(request, packageId):
    package = Package.objects.get(packageId = packageId)

    context = {
        'package' : package
    }

    return render(request, 'admin/form/packageupdate.html', context=context)

@login_required
@user_passes_test(user_has_package_management_role)
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
@user_passes_test(user_has_driver_management_role)
def updatedriver(request, driverId):
    driver = Driver.objects.get(driverId = driverId)

    context = {
        'driver' : driver
    }

    return render(request, 'admin/form/driverupdate.html', context=context)

@login_required
@user_passes_test(user_has_driver_management_role)
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

''' 
to add user by superadmin
 this function only lets superuser to goto add user page
'''
@login_required
@user_passes_test(lambda u: u.is_superuser) 
def adduser(request):
    if request.method == 'POST':
        print(request.POST)
        username = request.POST.get('username')
        password = request.POST.get('password')
        driver_management = 'driver_management' in request.POST
        package_management = 'package_management' in request.POST
        hotel_management = 'hotel_management' in request.POST
        air_ticketing_management = 'air_ticketing_management' in request.POST

        # checking if username already exists
        if User.objects.filter(username=username).exists():
            messages.error(request, "Username already exists...")

        # creating user
        else:
            # Creation of new user
            user = User.objects.create_user(
                username=username, 
                password=password,
                is_staff = True,
                is_superuser = False
            )
            
            # Linking created user's data into Profile table along with the role
            Profile.objects.create(
                user = user,
                driver_management=driver_management,
                package_management=package_management,
                hotel_management=hotel_management,
                air_ticketing_management=air_ticketing_management
            )

            messages.success(request, "User created successfully!")
            return redirect('add-user')

    return render(request, 'admin/form/adduser.html')