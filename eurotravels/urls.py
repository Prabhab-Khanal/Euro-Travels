from django.contrib import admin
from django.urls import include, path
from core.views import *
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


    path("admin/", admin.site.urls),

    # urls for admin panel
    path("euro-tour/login/", adminlogin, name="admin-login"),
    path("euro-tour/logout/", adminlogout, name="admin-logout"),
    path("package/", package, name="package"),
    path("driver/", driver, name="driver"),
    path("air/ticketing/", ticket, name="ticket"),
    path("hotels/", hotels, name="hotels"),
    path("message/", message, name="message"),

    #urls for updating form of admin panel
    path("package/add/", addpackage, name="add-package"),
    path("driver/add/", adddriver, name="add-driver"),
    path('hotels/add/', addhotel, name='add-hotel'),
    path('tickets/add/', addairticket, name='add-airticket'),

    # for updating packages & drivers
    path("package/update/<str:packageId>/", updatepackage, name="update-package"),
    path("driver/update/<str:driverId>/", updatedriver, name="update-driver"),
    path('updatehotel/<str:hotelId>/', updatehotel, name='updatehotel'),
    path('updateairticket/<str:ticketId>/', updateairticket, name='updateairticket'),
   

    # saving new changes
    path("package/save/<str:packageId>/", save_package_update, name="update-package-save"),
    path("driver/save/<str:driverId>/", save_driver_update, name="update-driver-save"),
    path('save_hotel_update/<str:hotelId>/', save_hotel_update, name='save_hotel_update'),
    path('save_air_ticket_update/<str:ticketId>/', save_air_ticket_update, name='save_air_ticket_update'),

    # url for deleting package and driver details
    path("delete/<str:packageId>/", delete_package, name="delete-package"),
    path("delete/drv/<str:driverId>/", delete_driver, name="delete-driver"),
    path('delete_hotel/<str:hotelId>/', delete_hotel, name='delete_hotel'),
    path('delete_airticket/<str:ticketId>/', delete_air_ticket, name='delete_airticket'),
   

    # url for user management by superuser
    path("usermanagement/add-user", adduser, name="add-user"),
    path('delete-user/<str:user_id>/', delete_user, name='delete-user'),

] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
