from rest_framework import permissions


class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_customer


class IsAgent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_agent


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin
