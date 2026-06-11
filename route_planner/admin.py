from django.contrib import admin
from import_export.admin import ImportExportModelAdmin

from route_planner.models import TruckStop
from route_planner.resources import TruckStopResource


@admin.register(TruckStop)
class TruckStopAdmin(ImportExportModelAdmin):
    resource_class = TruckStopResource

    list_display = [
        'id',
        'truckstop_name',
        'city',
        'state',
        'rack_id',
        'retail_price',
        'latitude',
        'longitude',
        'created',
        'modified'
    ]

    list_filter = [
        'city',
        'state',
        'created',
        'modified'
    ]

    search_fields = [
        'truckstop_name',
        'city',
        'state',
        'rack_id'
    ]

    ordering = ['truckstop_name']
    
    # Exclude auto-generated timestamp fields from form
    readonly_fields = ['created', 'modified']

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'truckstop_name',
                'address',
                'city',
                'state'
            )
        }),
        ('Location Data', {
            'fields': (
                'latitude',
                'longitude'
            )
        }),
        ('Fuel Data', {
            'fields': (
                'rack_id',
                'retail_price'
            )
        }),
        ('System Info', {
            'fields': (
                'created',
                'modified'
            ),
            'classes': ('collapse',)
        }),
    )

    def has_delete_permission(self, request, obj=None):
        return True