from django.shortcuts import render

# for admin panel
def dashboard(request):
    return render(request, 'admin/dashboard.html')

def package(request):
    return render(request, 'admin/package.html')

def driver(request):
    return render(request, 'admin/driver.html')

def ticket(request):
    return render(request, 'admin/ticket.html')