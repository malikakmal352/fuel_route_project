from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from rest_framework.views import APIView
from drf_spectacular.utils import extend_schema, OpenApiResponse
from rest_framework import serializers


class HealthCheckResponseSerializer(serializers.Serializer):
    status = serializers.CharField()


class HealthCheckAPIView(APIView):
    permission_classes = [AllowAny]

    @extend_schema(
        responses={
            200: OpenApiResponse(
                response=HealthCheckResponseSerializer,
                description="Health check status"
            )
        },
        description="Health check endpoint to verify API is running"
    )
    def get(self, request):
        return Response({"status": "OK"})
