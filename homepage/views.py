from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Contact
from core.models import Package, Hotel, AirTicket
from django.core.mail import send_mail
from django.conf import settings


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

'''
    This code is used to send all the messages of the contact me to the mail used in .env
'''
def contact_view(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        email = request.POST.get('email')
        message = request.POST.get('message')

        # construction of email subject and message body
        subject = 'Enquiry for Booking Package'
        body = f"Name: {name}\n\nEmail: {email}\n\nMessage:\n{message}"

        # Send the email to the host user
        send_mail(
            subject,
            body,
            settings.EMAIL_HOST_USER,  # Email for sending the mail to the company
            [settings.EMAIL_HOST_USER],  # Company email address to receive mail
            fail_silently=False,
            )       
        
        return redirect('success-page')
    
    return render(request, 'main.html')

def success(request):
    return render(request, 'success.html')