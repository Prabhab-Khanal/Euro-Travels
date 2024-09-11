

from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Contact
from core.models import Package, Hotel, AirTicket


# Create your views here.


def main1(request):
    if request.method == "POST":
        contact = Contact()
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject= request.POST.get('message')

        contact.name=name
        contact.email = email
        contact.subject = subject
        contact.date = datetime.now()

        contact.save()
    return render(request, 'main.html')



def index(request):
    if request.method == "POST":
        contact = Contact()
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject= request.POST.get('message')

        contact.name=name
        contact.email = email
        contact.subject = subject
        contact.date = datetime.now()

        contact.save()

        return redirect('index')


    return render(request, 'main.html')



def package_list(request):
    packages = Package.objects.all()
    hotels = Hotel.objects.all()
    airtickets = AirTicket.objects.all()
    return render(request, 'packages.html', {
        'packages': packages,
        'hotels': hotels,
        'airtickets': airtickets
        })