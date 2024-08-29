from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required

# for admin panel
@login_required
def dashboard(request):
    return render(request, 'admin/dashboard.html')

@login_required
def package(request):
    return render(request, 'admin/package.html')

@login_required
def driver(request):
    return render(request, 'admin/driver.html')

@login_required
def ticket(request):
    return render(request, 'admin/ticket.html')

# logic for the login page

def adminlogin(request):
    if request.user.is_authenticated:
        return redirect('dashboard')
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Checking if username exists in the database
        user = authenticate(request, username=username, password=password)
        
        if user is not None:
            if user.is_staff:
                # Successful login, redirect to dashboard
                login(request, user)
                return redirect('dashboard')
                      
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
