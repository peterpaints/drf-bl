from rest_framework.permissions import BasePermission
from .models import Bucketlist, Item


class IsOwner(BasePermission):
    """Custom permissions so only bucketlist owners can edit them."""
    def has_object_permission(self, request, view, obj):
        """Return True if user is bucketlist's owner."""
        if isinstance(obj, Bucketlist):
            return obj.created_by == request.user
        elif isinstance(obj, Item):
            bucket = Bucketlist.objects.get(id=obj.bucketlist.id)
            if bucket:
                return True
            else:
                return False
