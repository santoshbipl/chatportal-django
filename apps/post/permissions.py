from rest_framework import permissions
from .models import *
from .serializers import *

class IsOwnerPermission(permissions.DjangoModelPermissions):
    
    authenticated_users_only = True
    
    def has_permission(self, request, view):
        return super().has_permission(request, view)

    def has_object_permission(self, request, view, obj:Post):
        user = User.objects.get(id = get_user_id(request))
        return obj.author == user