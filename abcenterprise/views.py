from django.shortcuts import render

from django.shortcuts import render
from accounts.models import Announcement

def home(request):

    announcements = Announcement.objects.filter(active=True).order_by('-date_posted')[:5]

    return render(request,'home.html',{
        'announcements': announcements
    })

def services(request):
    return render(request,'services.html')

def contact(request):
    return render(request,'contact.html')
