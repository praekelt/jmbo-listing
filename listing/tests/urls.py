from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings

from rest_framework import routers
from rest_framework_extras import discover

from listing import api as listing_api


admin.autodiscover()

router = routers.DefaultRouter()
discover(router)
listing_api.register(router)

urlpatterns = [
    url(r"^admin/", include(admin.site.urls)),
    url(r"^api/(?P<version>(v1))/", include(router.urls)),
    url(r"^jmbo/", include("jmbo.urls")),
]
