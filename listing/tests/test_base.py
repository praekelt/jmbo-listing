import os
import unittest

from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.contrib.contenttypes.models import ContentType
from django.test.client import Client, RequestFactory

from listing.models import Listing
from listing.listing_styles import LISTING_CLASSES
from listing.tests.models import TestModel, TestWithTitleModel


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

        obj = TestModel.objects.create()
        cls.test_obj = obj

        obj = TestWithTitleModel.objects.create(title="testmodel")
        cls.test_with_title_obj = obj

    def test_content_type(self):
        listing = Listing.objects.create()
        listing.content_types = [ContentType.objects.get_for_model(TestModel)]
        listing.save()
        from django.db.models import Q
        from itertools import chain
        #q = None
        li = []
        for ct in ContentType.objects.all():
            li.append(ct.get_all_objects_for_this_type())
            #if q is None:
            #    q = f
            #else:
            #    q = q | f
        aaa = chain(*li)
        print aaa
        print "cool"
        #print listing.queryset

