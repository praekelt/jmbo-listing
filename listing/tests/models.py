from django.db import models

from category.models import Category, Tag


class BaseModel(models.Model):
    category = models.ForeignKey(
        Category,
        blank=True,
        null=True,
    )
    categories = models.ManyToManyField(
        Category,
        blank=True,
        related_name="basemodel_categories",
    )
    tag = models.ForeignKey(
        Tag,
        blank=True,
        null=True,
    )
    tags = models.ManyToManyField(
        Tag,
        blank=True,
        related_name="basemodel_tags",
    )


class TestModel(BaseModel):

    def __unicode__(self):
        return "unicode = %s" % self.id


class TestWithTitleModel(BaseModel):
    title = models.CharField(max_length=32)

    def __unicode__(self):
        return self.title
