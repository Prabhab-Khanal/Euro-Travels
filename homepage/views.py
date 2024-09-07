

from datetime import datetime
from django.http import HttpResponse
from django.shortcuts import redirect, render
from .models import Contact
# Create your views here.
def index(request):
    if request.method == "POST":
        contact = Contact()
        name = request.POST.get('name')
        email = request.POST.get('email')
        subject= request.POST.get('subject')

        contact.name=name
        contact.email = email
        contact.subject = subject
        contact.date = datetime.now()

        contact.save()

        return redirect('')


    return render(request, 'main.html')