from rest_framework import serializers
from .models import Bucketlist
from django.contrib.auth.models import User


class BucketlistSerializer(serializers.ModelSerializer):
    """Serializer to map the Bucketlist table into JSON."""

    created_by = serializers.ReadOnlyField(source='created_by.username')

    class Meta:
        """Map serializer fields to the models fields."""
        model = Bucketlist
        fields = ('id', 'name', 'date_created', 'date_modified', 'created_by')
        read_only_fields = ('date_created', 'date_modified')


class UserSerializer(serializers.ModelSerializer):
    """Serializer to aid in auth."""

    bucketlists = serializers.PrimaryKeyRelatedField(
        many=True, queryset=Bucketlist.objects.all()
    )

    class Meta:
        """Map serializer fields to the default User model."""
        model = User
        fields = ('id', 'username', 'bucketlists')
