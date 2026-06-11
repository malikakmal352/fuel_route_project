from rest_framework import serializers

class RouteRequestSerializer(serializers.Serializer):
    start = serializers.CharField(
        required=True,
        help_text="Starting location (address, city, state)"
    )
    destination = serializers.CharField(
        required=True,
        help_text="Destination location (address, city, state)"
    )


class RouteResponseSerializer(serializers.Serializer):
    """Complete route response with fuel stops using ModelSerializer"""
    start_location = serializers.DictField()
    end_location = serializers.DictField()
    total_distance_miles = serializers.FloatField()
    total_distance_km = serializers.FloatField()
    total_duration_hours = serializers.FloatField()
    total_fuel_gallons = serializers.FloatField()
    total_fuel_cost = serializers.DecimalField(max_digits=10, decimal_places=2)
    route_geometry = serializers.DictField(help_text="Route geometry with key points including addresses, prices, and distances")