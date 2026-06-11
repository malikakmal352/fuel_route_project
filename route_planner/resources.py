from import_export import resources, fields
from route_planner.models import TruckStop


class TruckStopResource(resources.ModelResource):
    # Map CSV column names to model fields
    truckstop_name = fields.Field(
        column_name='Truckstop Name',
        attribute='truckstop_name'
    )
    address = fields.Field(
        column_name='Address',
        attribute='address'
    )
    city = fields.Field(
        column_name='City',
        attribute='city'
    )
    state = fields.Field(
        column_name='State',
        attribute='state'
    )
    rack_id = fields.Field(
        column_name='Rack ID',
        attribute='rack_id'
    )
    retail_price = fields.Field(
        column_name='Retail Price',
        attribute='retail_price'
    )

    class Meta:
        model = TruckStop

        fields = (
            'truckstop_name',
            'address',
            'city',
            'state',
            'rack_id',
            'retail_price',
            'created',
            'modified',
        )
       
        import_id_fields = (
            'truckstop_name',
            'address',
            'city',
            'state',
            'rack_id',
            'retail_price',
        )
        export_order = fields

        skip_unchanged = True
        report_skipped = True
        raise_errors = False