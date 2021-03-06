from django.conf.urls import include, url

from listing.views import ListingDetail


app_name = "listing"
urlpatterns = [
    url(
        r"^(?P<slug>[\w-]+)/$",
        ListingDetail.as_view(),
        name="listing-detail"
    ),
]
