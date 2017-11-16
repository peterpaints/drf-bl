from rest_framework import serializers, pagination
from .models import Bucketlist, Item
from django.contrib.auth.models import User


class ItemSerializer(serializers.ModelSerializer):
    """Serializer to map the Item table into JSON."""

    class Meta:
        """Map serializer fields to the models fields."""
        model = Item
        fields = ('id', 'name', 'bucketlist', 'date_created', 'date_modified', 'done')
        read_only_fields = ('date_created', 'date_modified')


class BucketlistSerializer(serializers.ModelSerializer):
    """Serializer to map the Bucketlist table into JSON."""

    created_by = serializers.ReadOnlyField(source='created_by.username')
    items = ItemSerializer(read_only=True, many=True)

    class Meta:
        """Map serializer fields to the models fields."""
        model = Bucketlist
        fields = ('id', 'name', 'items', 'date_created', 'date_modified', 'created_by')
        read_only_fields = ('date_created', 'date_modified')


class UserSerializer(serializers.ModelSerializer):
    """Serializer to aid in auth."""

    bucketlists = serializers.PrimaryKeyRelatedField(
        many=True, read_only=True
    )

    class Meta:
        """Map serializer fields to the default User model."""
        model = User
        fields = ('id', 'username', 'password', 'email', 'bucketlists')
        write_only_fields = ('password',)
        read_only_fields = ('id',)

    def create(self, validated_data):
        user = User.objects.create(
            username=validated_data['username'],
            email=validated_data['email']
        )

        user.set_password(validated_data['password'])
        user.save()

        return user


class StandardResultsSetPagination(pagination.PageNumberPagination):
    page_size = 5
    page_size_query_param = 'per_page'
    max_page_size = 20
