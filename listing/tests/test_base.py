import os
import unittest

from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test.client import Client, RequestFactory

from listing.models import Listing
from listing.listing_styles import LISTING_CLASSES
from listing.tests.models import ModelA, ModelB


RES_DIR = os.path.join(os.path.dirname(__file__), "res")
IMAGE_PATH = os.path.join(RES_DIR, "image.jpg")


def set_image(obj):
    obj.image.save(
        os.path.basename(IMAGE_PATH),
        ContentFile(open(IMAGE_PATH, "rb").read())
    )


class BaseTestCase(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
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

        obj = ModelA.objects.create(title="ModelA", slug="model-a")
        cls.model_a = obj

        obj = ModelB.objects.create(title="ModelB", slug="model-b")
        cls.model_b = obj

    def test_content_types(self):
        listing = Listing.objects.create()
        listing.content_types = [ContentType.objects.get_for_model(ModelA)]
        listing.save()
        qs = listing.queryset
        self.assertEqual(len(qs), 1)
        self.failUnless(self.model_a.modelbase_obj in qs)

