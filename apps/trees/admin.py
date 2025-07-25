from django.contrib import admin

from .models import PlantedTree, Tree


class PlantedTreeInline(admin.TabularInline):
    model = PlantedTree
    extra = 0
    fields = ('user', 'account', 'planted_at', 'get_age', 'latitude', 'longitude')
    can_delete = False
    readonly_fields = ('planted_at', 'get_age')

    def has_add_permission(self, request, obj=None):
        return False

    @admin.display(description='Age (years)')
    def get_age(self, obj):
        if obj:
            return obj.age
        return ''


@admin.register(Tree)
class TreeAdmin(admin.ModelAdmin):
    list_display = ('name', 'scientific_name')
    search_fields = ('name', 'scientific_name')
    inlines = [PlantedTreeInline]


@admin.register(PlantedTree)
class PlantedTreeAdmin(admin.ModelAdmin):
    list_display = ('tree', 'user', 'account', 'planted_at', 'get_age')
    list_filter = ('account', 'user', 'tree')
    search_fields = ('user__username', 'tree__name')

    @admin.display(description='Age (years)')
    def get_age(self, obj):
        return obj.age