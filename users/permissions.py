from rest_framework import permissions


class IsOwner(permissions.BasePermission):
    """Проверка на владельца, чтобы только владелец мог смотреть свои привычки"""

    def has_object_permission(self, request, view, obj):
        if obj.user == request.user:
            return True
        return False
