from rest_framework import permissions


class IsCustomer(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_customer


class IsAgent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_agent and request.user.is_approved


class IsAdmin(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin


class IsAdminOrAgent(permissions.BasePermission):
    def has_permission(self, request, view):
        return request.user.is_admin or request.user.is_agent
