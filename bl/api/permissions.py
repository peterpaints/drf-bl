from rest_framework.permissions import BasePermission
from .models import Bucketlist


class IsOwner(BasePermission):
    """Custom permissions so only bucketlist owners can edit them."""
    def has_object_permission(self, request, view, obj):
        """Return True if user is bucketlist's owner."""
        if isinstance(obj, Bucketlist):
            return obj.owner == request.user
        return obj.owner == request.user
