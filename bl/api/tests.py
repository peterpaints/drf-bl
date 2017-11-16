from django.test import TestCase
from .models import Bucketlist
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class BucketlistTestCase(TestCase):
    """This class contains tests for bucketlists."""
    def setUp(self):
        """Define test variables."""
        user = User.objects.create_user(username="Peter")
        self.name = 'Attend TomorrowLand'
        self.bucketlist = Bucketlist(name=self.name, created_by=user)

    def test_bucketlist_creation_in_model(self):
        old_count = Bucketlist.objects.count()
        self.bucketlist.save()
        new_count = Bucketlist.objects.count()
        self.assertEqual(new_count - old_count, 1)


class ViewTestCase(TestCase):
    """Test the API views."""

    def setUp(self):
        """Define test variables."""
        user = User.objects.create_user(username="Peter")
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        self.bucketdict = {'name': 'Go to Mars or something', 'created_by': user.id}
        self.response = self.client.post(
            reverse('create'),
            self.bucketdict,
            format="JSON"
        )

    def test_api_create_bucketlist(self):
        """Test creation of a bucketlist via the API."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_authorization_was_enforced(self):
        """Test authorization."""
        new_client = APIClient()
        response = new_client.get('/bucketlists/', kwargs={'pk': 1}, format="JSON")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_get_bucketlist(self):
        """Test get endpoint."""
        bucketlist = Bucketlist.objects.get(id=1)
        response = self.client.get(
            reverse('details'), kwargs={'pk': bucketlist.id}, format="JSON"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, bucketlist)

    def test_api_update_bucketlist(self):
        bucketlist = Bucketlist.objects.get(id=1)
        new_bucketlist = {'name': 'Do some other stuff'}
        response = self.client.put(
            reverse('details'), kwargs={'pk': bucketlist.id},
            new_bucketlist, format="JSON"
        )

        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_delete_bucketlist(self):
        bucketlist = Bucketlist.objects.get(id=1)
        response = self.client.delete(
            reverse('details'), kwargs={'pk': bucketlist.id},
            format="JSON", follow=True
        )

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
