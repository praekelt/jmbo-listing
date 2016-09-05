from django.core.urlresolvers import reverse
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.test.client import Client


class AdminTestCase(TestCase):

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

    def setUp(self):
        self.client.login(username="editor", password="password")

    def test_add(self):
        response = self.client.get("/admin/listing/listing/add/")
        self.assertEqual(response.status_code, 200)
