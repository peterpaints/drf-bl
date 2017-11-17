from django.test import TestCase
from .models import Bucketlist, Item
from rest_framework.test import APIClient
from rest_framework import status
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User


class AuthTestCase(TestCase):
    """Test the /users/register/ and /users/login/ endpoints."""
    def setUp(self):
        """Define test vars."""
        self.client = APIClient()
        self.register_data = {
            "username": "johndoe",
            "email": "johndoe@test.com",
            "password": "Testpassw0rd"
        }
        self.login_data = {
            "username": "johndoe",
            "password": "Testpassw0rd"
        }

    def register_user(self):
        """Register a test user."""
        return self.client.post('/users/register/', self.register_data, format="json")

    def login_user(self):
        """Log in a test user."""
        return self.client.post('/users/login/', self.login_data, format="json")

    def test_auth_register(self):
        """Test the /users/register/ endpoint."""
        response = self.register_user()
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_auth_login(self):
        """Test the /users/login/ endpoint."""
        self.register_user()
        response = self.login_user()
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(response.data['token'])


class BucketlistTestCase(TestCase):
    """Test the API views."""

    def setUp(self):
        """Define test variables."""
        user = User.objects.create_user(username="Peter")
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        self.bucketdict = {'name': 'Go to Mars or something', 'created_by': user.username}
        self.response = self.client.post(
            reverse('bucketlists'),
            self.bucketdict,
            format="json"
        )

    def test_api_create_bucketlist(self):
        """Test creation of a bucketlist via the API."""
        self.assertEqual(self.response.status_code, status.HTTP_201_CREATED)

    def test_authorization_was_enforced(self):
        """Test authorization."""
        new_client = APIClient()
        response = new_client.get('/bucketlists/', kwargs={'pk': 1}, format="json")
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_api_get_bucketlist(self):
        """Test bucketlist get endpoint."""
        bucketlist = Bucketlist.objects.get()
        response = self.client.get('/bucketlists/', kwargs={'pk': bucketlist.id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, bucketlist)

    def test_api_update_bucketlist(self):
        """Test bucketlist put endpoint."""
        bucketlist = Bucketlist.objects.get()
        new_bucketlist = {'name': 'Do some other stuff'}
        response = self.client.put('/bucketlists/{}/'.format(bucketlist.id), new_bucketlist, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_api_delete_bucketlist(self):
        """Test bucketlist delete endpoint."""
        bucketlist = Bucketlist.objects.get()
        response = self.client.delete('/bucketlists/{}/'.format(bucketlist.id), format="json", follow=True)
        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class ItemTestCase(TestCase):
    """Test the API views."""

    def setUp(self):
        """Define test variables."""
        user = User.objects.create_user(username="Peter")
        self.client = APIClient()
        self.client.force_authenticate(user=user)
        self.bucketdict = {'name': 'Go to Mars or something', 'created_by': user.username}
        self.response = self.client.post(
            reverse('bucketlists'),
            self.bucketdict,
            format="json"
        )
        bucketlist = Bucketlist.objects.get()
        self.itemdict = {'name': 'Find life on Mars', 'bucketlist': bucketlist.id}
        self.item_res = self.client.post(
            '/bucketlists/{}/items/'.format(bucketlist.id), self.itemdict,
            format="json"
        )

    def test_api_create_bucketlist_item(self):
        """Test creation of a bucketlist item via the API."""
        self.assertEqual(self.item_res.status_code, status.HTTP_201_CREATED)

    def test_api_get_bucketlist_item(self):
        """Test get endpoint."""
        bucketlist = Bucketlist.objects.get()
        response = self.client.get('/bucketlists/', kwargs={'pk': bucketlist.id}, format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertContains(response, bucketlist)
