from rest_framework import serializers
from rest_framework import viewsets
from rest_framework.reverse import reverse
import rest_framework_extras

from listing.models import Listing, ListingContent, ListingPinned


class ListingSerializer(serializers.HyperlinkedModelSerializer):

    class Meta:
        model = Listing


class ListingCreateUpdateContentSerializer(
    serializers.HyperlinkedModelSerializer
):
    """The many-to-many with a through requires this serializer"""

    class Meta:
        model = ListingContent
        fields = ("modelbase_obj", "position")


class ListingCreateUpdateSerializer(serializers.HyperlinkedModelSerializer):
    content = ListingCreateUpdateContentSerializer(many=True)

    class Meta:
        model = Listing

    def create(self, validated_data):
        content = validated_data.pop("content", [])
        listing = super(ListingCreateUpdateSerializer, self).create(
            validated_data
        )

        for di in content:
            di["listing"] = listing
            ListingContent.objects.create(**di)

        return listing

    def update(self, instance, validated_data):
        content = validated_data.pop("content", [])
        listing = super(ListingCreateUpdateSerializer, self).update(
            instance, validated_data
        )

        ListingContent.objects.filter(listing=listing).delete()
        for di in content:
            di["listing"] = listing
            ListingContent.objects.create(**di)

        return listing


class ListingObjectsViewSet(viewsets.ModelViewSet):
    queryset = Listing.objects.all()
    serializer_class = ListingSerializer

    def get_serializer_class(self):
        if self.action in ("create", "update", "partial_update"):
            return ListingCreateUpdateSerializer
        else:
            return ListingSerializer


class ListingPermittedViewSet(ListingObjectsViewSet):
    queryset = Listing.permitted.all()


def register(router):
    return rest_framework_extras.register(
        router,
        (
            ("listing-listing-permitted", ListingPermittedViewSet),
            ("listing-listing", ListingObjectsViewSet)
        )
    )


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

