from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin

from .models import Account, PlantedTree, Profile, User, UserAccount, Tree


class ProfileInline(admin.StackedInline):
    model = Profile
    can_delete = False


class UserAccountInline(admin.TabularInline):
    model = UserAccount
    extra = 1
    autocomplete_fields = ['account']


@admin.register(User)
class UserAdmin(BaseUserAdmin):
    inlines = (ProfileInline, UserAccountInline,)


@admin.register(Account)
class AccountAdmin(admin.ModelAdmin):
    list_display = ('name', 'created', 'active')
    list_filter = ('active',)
    search_fields = ('name',)
    actions = ['activate_accounts', 'deactivate_accounts']

    @admin.action(description='Activate selected accounts')
    def activate_accounts(self, request, queryset):
        queryset.update(active=True)

    @admin.action(description='Deactivate selected accounts')
    def deactivate_accounts(self, request, queryset):
        queryset.update(active=False)


class PlantedTreeInline(admin.TabularInline):
    model = PlantedTree
    extra = 0
    fields = ('user', 'account', 'planted_at', 'latitude', 'longitude')
    can_delete = False
    readonly_fields = ('planted_at',)

    def has_add_permission(self, request, obj=None):
        return False


@admin.register(Tree)
class TreeAdmin(admin.ModelAdmin):
    list_display = ('name', 'scientific_name')
    search_fields = ('name', 'scientific_name')
    inlines = [PlantedTreeInline]


@admin.register(PlantedTree)
class PlantedTreeAdmin(admin.ModelAdmin):
    list_display = ('tree', 'user', 'account', 'planted_at')
    list_filter = ('account', 'user', 'tree')
    search_fields = ('user__username', 'tree__name')
