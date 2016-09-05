from rest_framework import serializers
from rest_framework import viewsets
import rest_framework_extras

from listing.models import Listing


'''
class PropertiesMixin(Serializer):
    content = ReadOnlyField()
    content_pages = ReadOnlyField()

    class Meta:
        fields = ("content", "content_pages")


class PostSerializer(
    PropertiesMixin, jmbo_api.ModelBaseSerializer
    ):

    class Meta(jmbo_api.ModelBaseSerializer.Meta):
        model = Post
'''


class ListingSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Listing


class ListingObjectsViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer


class ListingPermittedViewSet(viewsets.ModelViewSet):
    queryset = Listing.permitted.all()
    serializer_class = ListingSerializer


def register(router):
    return rest_framework_extras.register(
        router,
        (
            ("listing-listing-permitted", ListingPermittedViewSet),
            ("listing-listing", ListingObjectsViewSet)
        )
    )
