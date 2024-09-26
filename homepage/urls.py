from django.urls import include, path
from . import views

urlpatterns =[

    path('',views.index,name='index'),
    path('main/', views.main1, name="main"),

    path('tour/muktinath',views.tour_muktinath, name ="muktinath"),
    path('tour/pathivara',views.tour_pathivara, name ="pathivara"),
    path('tour/kalinchowk',views.tour_kalinchowk, name ="kalinchowk"),
    path('tour/ktmpkr',views.tour_ktmpkr, name ="ktmpkr"),
    path('tour/kailash',views.tour_kailash, name ="kailash"),
]