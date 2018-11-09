from rest_framework import permissions


class IsOwnerOrReadOnly(permissions.BasePermission):

    def has_object_permission(self, request, view, obj):
        """GETリクエストは通すがPOSTやPUTは所有者を確認する"""
        if request.method in permissions.SAFE_METHODS:
            return True
        return request.user == obj.user
