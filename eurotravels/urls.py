from django.contrib import admin
from django.urls import path
from core.views import *
from django.conf import settings
from django.conf.urls.static import static

# Admin Panel Changes
admin.site.site_header = "Euro Tour Travels"
admin.site.site_title = "Euro Tour Travels Admin Portal"
admin.site.index_title = "Welcome to Euro Tour Travels Portal"

urlpatterns = [
    path("admin/", admin.site.urls),

    # urls for admin panel
    path("euro-tour/login/", adminlogin, name="admin-login"),
    path("euro-tour/logout/", adminlogout, name="admin-logout"),
    path("package/", package, name="package"),
    path("driver/", driver, name="driver"),
    path("air/ticketing/", ticket, name="ticket"),
    path("hotels/", hotels, name="hotels"),

    #urls for updating form of admin panel
    path("package/add/", addpackage, name="add-package"),
    path("driver/add/", adddriver, name="add-driver"),
    path("package/update/", updatepackage, name="update-package"),
    path("driver/update/", updatedriver, name="update-driver"),
] + static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)
