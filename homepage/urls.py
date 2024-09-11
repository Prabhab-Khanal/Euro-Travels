from django.urls import include, path
from . import views

urlpatterns =[

    path('',views.index,name='index'),
    path('package_list/', views.package_list, name='packages'),
    path('main/',views.main1,name="main")
]