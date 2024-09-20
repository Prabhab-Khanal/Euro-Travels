from django.contrib import admin
from django.urls import include, path
from django.conf import settings
from django.conf.urls.static import static

# Admin Panel Changes
admin.site.site_header = "Euro Tour Travels"
admin.site.site_title = "Euro Tour Travels Admin Portal"
admin.site.index_title = "Welcome to Euro Tour Travels Portal"

urlpatterns = [
    # homepage
    path('',include('homepage.urls')),
    path('package_list/',include('homepage.urls')),
    path('main/',include('homepage.urls')),
    path('tour/muktinath/',include('homepage.urls')),
    path('tour/pathivara/',include('homepage.urls')),
    path('tour/ktmpkr/',include('homepage.urls')),
    path('tour/kalinchowk/',include('homepage.urls')),
    path('tour/kailash/',include('homepage.urls')),


   

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
