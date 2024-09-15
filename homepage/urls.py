from django.urls import include, path
from . import views

urlpatterns =[

    path('',views.index,name='index'),
    path('package_list/', views.package_list, name='packages'),
    path('main/', views.main1, name="main"),

    # for contact me pages
    path('contact/', views.contact_view, name="contact-me"),
    path('success/', views.success, name="success-page"),
    path('error/', views.error, name="error-page"),
    path('error/', views.email_non_exist, name="email-page"),
]