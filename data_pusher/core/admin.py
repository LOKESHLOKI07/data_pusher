from django.contrib import admin
from .models import Account, Destination, Webhook

@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('email', 'account_id', 'account_name', 'app_secret_token', 'website')
    search_fields = ('email', 'account_name')

@admin.register(Destination)
class DestinationAdmin(admin.ModelAdmin):
    list_display = ('account', 'url', 'http_method')
    search_fields = ('account__account_name', 'url')

@admin.register(Webhook)
class WebhookAdmin(admin.ModelAdmin):
    list_display = ('account', 'event', 'destination', 'enabled')
    search_fields = ('account__account_name', 'event')
