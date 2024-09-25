from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Contact
from core.models import Package, Hotel, AirTicket
from django.core.mail import send_mail
from django.conf import settings
from django.contrib import messages
from django.core.exceptions import ValidationError
from django.core.validators import validate_email
from django.template.loader import render_to_string


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
    The mail is sent to the person who is using contact me and also the travel agency
'''
# def contact_view(request):
#     if request.method == 'POST':
#         name = request.POST.get('name')
#         email = request.POST.get('email')
#         message = request.POST.get('message')

#         special_characters = "!@#$%^&*()_-+=/?,<>'"

#         # checking if name contains special characters
#         if any(char in special_characters for char in name):
#             return redirect('error-page')

#         try:
#             # Validate the email address format
#             validate_email(email)
#         except ValidationError:
#             return redirect('email-page')

#         # Construct email subject and message body for the company
#         receiving_subject = 'Message Received From Customer'
#         received_body_html = render_to_string('admin_email_template.html',{
#             'name' : name,
#             'message' : message,
#             'email' : email,
#             })

#         try:
#             # Send the enquiry email to the company
#             send_mail(
#                 receiving_subject,
#                 '',
#                 settings.EMAIL_HOST_USER,  # Company email address (sender)
#                 [settings.EMAIL_HOST_USER],  # Company email address to receive the enquiry
#                 fail_silently=False,
#                 html_message=received_body_html  # The HTML message
#             )
                
#             # subject and body to send user the message that their enquiry is sent
#             thank_you_subject = "Thank you for Contacting Us"

#             # Render the HTML email template
#             thank_you_body_html = render_to_string('email_template.html', {
#                 'name': name,
#                 'message': message,
#             })

#             # Send the HTML email to the user
#             send_mail(
#                 thank_you_subject,
#                 '',
#                 settings.EMAIL_HOST_USER,  # Company email address (sender)
#                 [email],  # User's email address to receive the thank you email (receiver)
#                 fail_silently=False,
#                 html_message=thank_you_body_html  # The HTML message
#             )
#             return redirect('success-page')

#         except Exception as e:
#             # If any error occurs, this block will handle it
#             return redirect('error-page')

#     return render(request, 'main.html')

# # If sending message is successful
# def success(request):
#     return render(request, 'success.html')

# # If sending message is un-successful
# def error(request):
#     return render(request, 'error.html')

<<<<<<< Updated upstream
# If sending message is un-successful
def email_non_exist(request):
    return render(request, 'email_not_exist.html')
=======
# # If sending message is un-successful
# def email_non_exist(request):
#     return render(request, 'email_not_exist.html')

def tour_muktinath(request):
    return render(request, 'mustang.html')

def tour_pathivara(request):
    return render(request, 'pathivara.html')

def tour_ktmpkr(request):
    return render(request, 'ktmpkr.html')

def tour_kailash(request):
    return render(request, 'kailash.html')

def tour_kalinchowk(request):
    return render(request, 'kalinchowk.html')
>>>>>>> Stashed changes
