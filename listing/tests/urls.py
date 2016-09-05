from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings


admin.autodiscover()

urlpatterns = [
    url(r"^jmbo/", include("jmbo.urls")),
    url(r"^admin/", include(admin.site.urls)),
]
