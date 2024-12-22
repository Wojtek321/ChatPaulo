from rest_framework.permissions import BasePermission, SAFE_METHODS


class ChatbotOrReadOnly(BasePermission):
    def has_permission(self, request, view):
        if request.method in SAFE_METHODS:
            return True

        auth_header = request.headers.get('Authorization')
        if not auth_header or not auth_header.startswith('Bearer '):
            return False

        token = auth_header.split(' ')[1]
        if token != "SUPER_SECRET_TOKEN":
            return False

        if view.basename == 'items' and request.method in SAFE_METHODS:
            return True
        if view.basename == 'ingredients' and request.method in SAFE_METHODS:
            return True
        if view.basename == 'orders':
            return True

        return False
