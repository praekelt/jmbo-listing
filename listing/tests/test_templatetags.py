import os
import unittest

from django import template
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.contrib.sites.models import Site
from django.test import TestCase
from django.test.client import Client, RequestFactory

from category.models import Category

from listing.models import Listing
from listing.tests.models import ModelA


RES_DIR = os.path.join(os.path.dirname(__file__), "res")
IMAGE_PATH = os.path.join(RES_DIR, "image.jpg")


def set_image(obj):
    obj.image.save(
        os.path.basename(IMAGE_PATH),
        ContentFile(open(IMAGE_PATH, "rb").read())
    )


class TemplateTagsTestCase(TestCase):

    @classmethod
    def setUpTestData(cls):
        cls.client = Client()

        # Editor
        cls.editor = get_user_model().objects.create(
            username="editor",
            email="editor@test.com",
            is_superuser=True,
            is_staff=True
        )
        cls.editor.set_password("password")
        cls.editor.save()
        cls.client.login(username="editor", password="password")

        obj = Category.objects.create(title="CatA", slug="cat-a")
        cls.cat_a = obj

        obj = ModelA.objects.create(title="ModelA Published", slug="model-a-p")
        obj.categories = [cls.cat_a]
        obj.sites = Site.objects.all()
        obj.publish()
        cls.model_a_published = obj

    def test_listing_vertical(self):
        listing = Listing.objects.create(slug="listing-vertical", style="Vertical")
        listing.content_types = [ContentType.objects.get_for_model(ModelA)]
        listing.save()
        #import pdb;pdb.set_trace()
        t = template.Template("""{% load listing_tags %}
        {% listing 'listing-vertical' %}
        """)
        result = t.render(template.RequestContext({}))
        print result
