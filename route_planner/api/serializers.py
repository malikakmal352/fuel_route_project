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