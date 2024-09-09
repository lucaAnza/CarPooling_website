from rest_framework import permissions

#Create your custom permission for API

class IsReadOnly(permissions.BasePermission):
    
    def has_object_permission(self, request, view, obj):
        # SAFE_METHODS include read-only HTTP method
        if request.method in permissions.SAFE_METHODS:
            return True
        else:
            return False # You can do other check