from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from apps.users.models import Account, Profile, User, UserAccount


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class UserAccountInline(admin.TabularInline):
    model = UserAccount
    extra = 1
    autocomplete_fields = ['account']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (
        ProfileInline,
        UserAccountInline,
    )


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'active')
    list_filter = ('active',)
    search_fields = ('name', 'users__username')
    inlines = [UserAccountInline]
    actions = ['activate_accounts', 'deactivate_accounts']

    @admin.action(description='Activate selected accounts')
    def activate_accounts(self, request, queryset):
        queryset.update(active=True)

    @admin.action(description='Deactivate selected accounts')
    def deactivate_accounts(self, request, queryset):
        queryset.update(active=False)
