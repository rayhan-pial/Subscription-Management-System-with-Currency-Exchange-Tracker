from django.contrib import admin

from core.models import Plan, Subscription, ExchangeRateLog

@admin.register(Plan)
class PlanAdmin(admin.ModelAdmin):

    def has_module_permission(self, request):
        return request.user.is_staff

    def has_add_permission(self, request):
        return request.user.is_staff

    def has_change_permission(self, request):
        return request.user.is_staff

    def has_delete_permission(self, request):
        return request.user.is_staff

    def has_view_permission(self, request):
        return request.user.is_staff

@admin.register(Subscription)
class SubscriptionAdmin(admin.ModelAdmin):

    def has_module_permission(self, request):
        return request.user.is_staff

    def has_view_permission(self, request):
        return request.user.is_staff

@admin.register(ExchangeRateLog)
class ExchangeRateLogAdmin(admin.ModelAdmin):

    def has_module_permission(self, request):
        return request.user.is_staff

    def has_view_permission(self, request):
        return request.user.is_staff

