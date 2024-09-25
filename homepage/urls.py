from django.urls import include, path
from . import views

urlpatterns =[

    path('',views.index,name='index'),
    path('package_list/', views.package_list, name='packages'),
    path('main/', views.main1, name="main"),

    # for contact me pages
<<<<<<< Updated upstream
    path('contact/', views.contact_view, name="contact-me"),
    path('success/', views.success, name="success-page"),
    path('error/', views.error, name="error-page"),
    path('error/', views.email_non_exist, name="email-page"),
=======
    # path('contact/', views.contact_view, name="contact-me"),
    # path('success/', views.success, name="success-page"),
    # path('error/', views.error, name="error-page"),
    # path('error/', views.email_non_exist, name="email-page"),
    path('tour/muktinath',views.tour_muktinath, name ="muktinath"),
    path('tour/pathivara',views.tour_pathivara, name ="pathivara"),
    path('tour/kalinchowk',views.tour_kalinchowk, name ="kalinchowk"),
    path('tour/ktmpkr',views.tour_ktmpkr, name ="ktmpkr"),
    path('tour/kailash',views.tour_kailash, name ="kailash"),
>>>>>>> Stashed changes
]