from django.contrib import admin
from django.urls import path
from core.views import *

urlpatterns = [
    path("admin/", admin.site.urls),

    # urls for admin panel
    path("euro-tour/login/", adminlogin, name="admin-login"),
    path("euro-tour/logout/", adminlogout, name="admin-logout"),
    path("package/", package, name="package"),
    path("driver/", driver, name="driver"),
    path("air/ticketing/", ticket, name="ticket"),
    path("hotels/", hotels, name="hotels"),
]
