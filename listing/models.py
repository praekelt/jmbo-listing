from django.db import models
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from listing.listing_styles import LISTING_CLASSES
from listing.managers import PermittedManager


class AttributeWrapper:
    """Wrapper that allows attributes to be added or overridden on an object"""

    def __init__(self, obj, **kwargs):
        self._obj = obj
        self._attributes = {}
        for k, v in kwargs.items():
            self._attributes[k] = v

    def __getattr__(self, key):
        if key in self._attributes:
            return self._attributes[key]
        return getattr(self._obj, key)

    def __setstate__(self, dict):
        self.__dict__.update(dict)

    @property
    def klass(self):
        """Can"t override __class__ and making it a property also does not
        work. Could be because of Django metaclasses."""
        return self._obj.__class__


class Listing(models.Model):

    title = models.CharField(
        max_length=256,
        help_text="A short descriptive title.",
    )
    subtitle = models.CharField(
        max_length=256,
        blank=True,
        null=True,
        help_text="Some titles may be the same. A subtitle makes a distinction. It is not displayed on the site.",
    )
    slug = models.SlugField(
        editable=True,
        max_length=32,
        db_index=True,
    )
    content_types = models.ManyToManyField(
        ContentType,
        help_text="Content types to display, eg. post or gallery.",
        blank=True,
        null=True,
    )
    content = models.ManyToManyField(
        "jmbo.ModelBase",
        help_text="""Individual items to display. Setting this will ignore \
any setting for <i>Content Type</i>, <i>Categories</i> and <i>Tags</i>.""",
        blank=True,
        null=True,
        related_name="listing_content",
        through="ListingContent",
    )
    categories = models.ManyToManyField(
        "category.Category",
        help_text="Categories for which to collect items.",
        blank=True,
        null=True,
        related_name="listing_categories"
    )
    tags = models.ManyToManyField(
        "category.Tag",
        help_text="Tags for which to collect items.",
        blank=True,
        null=True,
        related_name="listing_tags"
    )
    pinned = models.ManyToManyField(
        "jmbo.ModelBase",
        help_text="""Individual items to pin to the top of the listing. These
items are visible across all pages when navigating the listing.""",
        blank=True,
        null=True,
        related_name="listing_pinned",
        through="ListingPinned",
    )
    count = models.IntegerField(
        default=0,
        help_text="""Number of items to display (excludes any pinned items).
Set to zero to display all items.""",
    )
    style = models.CharField(
        choices=[(klass.__name__, klass.__name__) for klass in LISTING_CLASSES],
        max_length=64
    )
    items_per_page = models.PositiveIntegerField(
        default=0,
        help_text="Number of items displayed on a page (excludes any pinned items). Set to zero to disable paging."
    )
    sites = models.ManyToManyField(
        "sites.Site",
        blank=True,
        null=True,
        help_text="Sites that this listing will appear on.",
    )

    objects = models.Manager()
    permitted = PermittedManager()

    class Meta:
        ordering = ("title", "subtitle")

    def __unicode__(self):
        if self.subtitle:
            return "%s (%s)" % (self.title, self.subtitle)
        else:
            return self.title

    def get_absolute_url(self):
        return reverse("listing-detail", args=[self.slug])

    @property
    def queryset(self):
        # See https://docs.djangoproject.com/en/1.8/topics/db/queries/#using-a-custom-reverse-manager.
        # Django 1.7 will remove the need for this slow workaround for the
        # content field. Due to the workaround we"re not always returning a
        # real queryset.
        content = self.content_queryset
        if content:
            return content

        q = ModelBase.permitted.all()
        one_match = False
        if self.content_type.exists():
            q = q.filter(content_type__in=self.content_type.all())
            one_match = True
        if self.categories.exists():
            q1 = Q(primary_category__in=self.categories.all())
            q2 = Q(categories__in=self.categories.all())
            q = q.filter(q1|q2)
            one_match = True
        if self.tags.exists():
            q = q.filter(tags__in=self.tags.all())
            one_match = True
        if not one_match:
            q = ModelBase.objects.none()
        q = q.exclude(id__in=self.pinned.all())

        # Ensure there are no duplicates. Oracle bugs require special handling
        # around distinct which incur a performance penalty when fetching
        # attributes. Avoid the penalty for other databases by doing database
        # detection.
        if "oracle" in connection.vendor.lower():
            q = q.only("id").distinct()
        else:
            q = q.distinct("publish_on", "created", "id").order_by(
                "-publish_on", "-created"
            )

        if self.count:
            q = q[:self.count]

        return q

    def set_pinned(self, iterable):
        for n, obj in enumerate(iterable):
            ListingPinned.objects.create(
                modelbase_obj=obj, listing=self, position=n
            )

    def set_content(self, iterable):
        for n, obj in enumerate(iterable):
            ListingContent.objects.create(
                modelbase_obj=obj, listing=self, position=n
            )

    @property
    def pinned_queryset(self):
        # See https://docs.djangoproject.com/en/1.8/topics/db/queries/#using-a-custom-reverse-manager.
        # Django 1.7 will remove the need for this slow workaround. Note we
        # return an emulated queryset.
        li = [o for o in ModelBase.permitted.filter(listing_pinned=self)]
        order = [o.modelbase_obj.id for o in ListingPinned.objects.filter(
            listing=self).order_by("position")]
        li.sort(lambda a, b: cmp(order.index(a.id), order.index(b.id)))
        return AttributeWrapper(li, exists=len(li))

    @property
    def content_queryset(self):
        # See https://docs.djangoproject.com/en/1.8/topics/db/queries/#using-a-custom-reverse-manager.
        # Django 1.7 will remove the need for this slow workaround. Note we
        # return an emulated queryset.
        li = [o for o in ModelBase.permitted.filter(listing_content=self)\
            .exclude(id__in=self.pinned.all())]
        order = [o.modelbase_obj.id for o in ListingContent.objects.filter(
            listing=self).order_by("position")]
        li.sort(lambda a, b: cmp(order.index(a.id), order.index(b.id)))
        return AttributeWrapper(li, exists=len(li))


class ListingContent(models.Model):
    """Through model to facilitate ordering"""

    modelbase_obj = models.ForeignKey('jmbo.ModelBase')
    listing = models.ForeignKey(Listing, related_name="content_link_to_listing")
    position = models.PositiveIntegerField(default=0)


class ListingPinned(models.Model):
    """Through model to facilitate ordering"""

    modelbase_obj = models.ForeignKey('jmbo.ModelBase')
    listing = models.ForeignKey(Listing, related_name="pinned_link_to_listing")
    position = models.PositiveIntegerField(default=0)
