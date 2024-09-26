from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Contact
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