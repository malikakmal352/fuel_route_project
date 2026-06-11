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

    fieldsets = (
        ('Basic Information', {
            'fields': (
                'truckstop_name',
                'address',
                'city',
                'state'
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
            )
        }),
    )

    def has_delete_permission(self, request, obj=None):
        # Optional: prevent deletion like your BillingSettings pattern
        return True  # change to False if you want protection