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

from homepage.models import *

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


def message(request):
    # importing data from package database
    messages = Contact.objects.all().order_by('-date')
    context = {
        'contacts' : messages
    }
    
    return render(request, 'admin/contact.html', context=context)

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
    # importing data from package database
    hotels = Hotel.objects.all()
    context = {
        'hotels' : hotels
    }
    
    return render(request, 'admin/hotels.html', context=context)

@login_required
@user_passes_test(user_has_air_ticketing_management_role)
def ticket(request):
    tickets = AirTicket.objects.all()
    context = {
        'air_ticket' : tickets
    }
    
    return render(request, 'admin/ticket.html',context= context)

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
        messages.error(request, "Package details deleted successfully.")

    except Package.DoesNotExist:
        messages.error(request, "Package not found...")
    
    return redirect('package')

# for drivers
@login_required
@user_passes_test(user_has_driver_management_role)
def delete_driver(request, driverId):
    try:
        driver = Driver.objects.get(driverId=driverId)

        # Delete the driver object
        driver.delete()
        messages.error(request, "Driver details deleted successfully.")
        
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
                is_staff=True,
                is_superuser=False
            )
            
            # Linking created user's data into Profile table along with the role
            Profile.objects.create(
                user=user,
                driver_management=driver_management,
                package_management=package_management,
                hotel_management=hotel_management,
                air_ticketing_management=air_ticketing_management
            )

            messages.success(request, "User created successfully!")
            return redirect('add-user')

    # Retrieving all users and their roles
    users = User.objects.filter(is_superuser=False)
    user_roles = []
    for user in users:
        # Use get_or_create to ensure a profile exists
        profile, created = Profile.objects.get_or_create(user=user)
        roles = {
            'driver_management': profile.driver_management,
            'package_management': profile.package_management,
            'hotel_management': profile.hotel_management,
            'air_ticketing_management': profile.air_ticketing_management
        }
        user_roles.append({
            'userid': user.id,
            'username': user.username,
            'roles': roles
        })

    return render(request, 'admin/form/adduser.html', {'user_roles': user_roles})

@login_required
@user_passes_test(lambda u: u.is_superuser)
def delete_user(request, user_id):
    try:
        # Retrieving the user and its associated profile
        user = User.objects.get(id=user_id)
        profile = Profile.objects.get(user=user)
        
        # Delete the profile first and then user
        profile.delete()
        user.delete()
        
        # Display a success message
        messages.error(request, "User's details deleted successfully!")

    except User.DoesNotExist:
        messages.error(request, "User does not exist.")

    except Profile.DoesNotExist:
        # If the user exists but the profile doesn't, still delete the user
        user.delete()
        messages.warning(request, "User deleted, but no associated profile was found.")
    
    return redirect('add-user') 
    




@login_required
@user_passes_test(user_has_hotel_management_role)
def addhotel(request):
    if request.method == 'POST':
        hotelname = request.POST.get('hotelname')
        location = request.POST.get('location')
        rating = request.POST.get('rating')
        price_per_night = request.POST.get('price_per_night')
        hotel_description = request.POST.get('hotel_description')
        image = request.FILES.get('hotel_image')

        # Validation for hotel name and rating
        pattern = re.compile(r'[A-Za-z]')  # Checks for alphabets in hotel name
        if not pattern.search(hotelname):
            messages.error(request, "Hotel name should contain at least one alphabet...")
            return render(request, 'admin/form/hoteladd.html')

        if not rating.isdigit() or float(rating) > 5:
            messages.error(request, "Rating must be a number between 0 and 5...")
            return render(request, 'admin/form/hoteladd.html')

        try:
            # Creating a new instance of Hotel to save in the database
            hotel = Hotel(
                hotelname=hotelname,
                location=location,
                rating=rating,
                price_per_night=price_per_night,
                hotel_description=hotel_description,
                image=image
            )
            hotel.save()  # Saving the instance
            messages.success(request, "Hotel details saved successfully...")
            return redirect('hotels')

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return render(request, 'admin/form/hoteladd.html')

    return render(request, 'admin/form/hoteladd.html')






@login_required
@user_passes_test(user_has_air_ticketing_management_role)
def addairticket(request):
    if request.method == 'POST':
        airline = request.POST.get('airline')
        departure = request.POST.get('departure')
        destination = request.POST.get('destination')
        date_of_flight = request.POST.get('date_of_flight')
        price = request.POST.get('price')
        flight_number = request.POST.get('flight_number')
        airline_logo = request.FILES.get('airline_logo')

        

        # Validation for airline and flight number
        pattern = re.compile(r'[A-Za-z]')  # Checks for alphabets in airline name
        if not pattern.search(airline):
            messages.error(request, "Airline name should contain at least one alphabet.")
            return render(request, 'admin/form/ticketadd.html')

        try:
            # Creating a new instance of AirTicket to save in the database
            air_ticket = AirTicket(
                airline=airline,
                departure=departure,
                destination=destination,
                date_of_flight=date_of_flight,
                price=price,
                flight_number=flight_number,
                airline_logo=airline_logo  # Save the uploaded logo
            )
            air_ticket.save()  # Saving the instance
            messages.success(request, "Air Ticket details saved successfully...")
            return redirect('ticket')

        except Exception as e:
            messages.error(request, f"An error occurred: {e}")
            return render(request, 'admin/form/ticketadd.html')

    return render(request, 'admin/form/ticketadd.html')






@login_required
@user_passes_test(user_has_hotel_management_role)
def updatehotel(request, hotelId):
    hotel = Hotel.objects.get(hotelId=hotelId)

    context = {
        'hotel': hotel
    }

    return render(request, 'admin/form/hotelupdate.html', context=context)


@login_required
@user_passes_test(user_has_hotel_management_role)
def save_hotel_update(request, hotelId):
    if request.method == 'POST':
        hotelname = request.POST.get('hotel_name')
        location = request.POST.get('location')
        rating = request.POST.get('rating')
        price_per_night = request.POST.get('price_per_night')
        hotel_description = request.POST.get('hotel_description')

        update_set = Hotel.objects.get(hotelId=hotelId)

        if 'hotel_image' in request.FILES:
            image = request.FILES['hotel_image']
            update_set.image = image

        update_set.hotelname = hotelname
        update_set.location = location
        update_set.rating = rating
        update_set.price_per_night = price_per_night
        update_set.hotel_description = hotel_description

        update_set.save()

        messages.success(request, "Hotel details updated successfully...")
        return redirect('hotels')

    return render(request, 'admin/hotels.html')




@login_required
@user_passes_test(user_has_air_ticketing_management_role)
def updateairticket(request, ticketId):
    air_ticket = AirTicket.objects.get(flight_number =ticketId)

    context = {
        'air_ticket': air_ticket
    }

    return render(request, 'admin/form/ticketupdate.html', context=context)


@login_required
@user_passes_test(user_has_air_ticketing_management_role)
def save_air_ticket_update(request, ticketId):
    if request.method == 'POST':
        airline = request.POST.get('airline')
        departure = request.POST.get('departure')
        destination = request.POST.get('destination')
        date_of_flight = request.POST.get('date_of_flight')
        price = request.POST.get('price')
        flight_number = request.POST.get('flight_number')

        update_set = AirTicket.objects.get(flight_number=ticketId)

        # Handling file upload for airline_logo
        if request.FILES.get('airline_logo'):
            airline_logo = request.FILES['airline_logo']
            update_set.airline_logo = airline_logo

        update_set.airline = airline
        update_set.departure = departure
        update_set.destination = destination
        update_set.date_of_flight = date_of_flight
        update_set.price = price
        update_set.flight_number = flight_number

        update_set.save()

        messages.success(request, "Air ticket details updated successfully...")
        return redirect('ticket')

    return render(request, 'admin/ticket.html')




@login_required
@user_passes_test(user_has_hotel_management_role)
def delete_hotel(request, hotelId):
    try:
        hotel = Hotel.objects.get(hotelId=hotelId)
        hotel.delete()
        messages.success(request, "Hotel details deleted successfully.")
    except Hotel.DoesNotExist:
        messages.error(request, "Hotel not found...")
    
    return redirect('hotels')




@login_required
@user_passes_test(user_has_air_ticketing_management_role)
def delete_air_ticket(request, ticketId):
    try:
        air_ticket = AirTicket.objects.get(flight_number=ticketId)
        air_ticket.delete()
        messages.success(request, "Air ticket details deleted successfully.")
    except AirTicket.DoesNotExist:
        messages.error(request, "Air ticket not found...")
    
    return redirect('ticket')

