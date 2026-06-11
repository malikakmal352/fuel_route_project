from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from drf_spectacular.utils import extend_schema

from route_planner.services import RouteService
from route_planner.api.serializers import RouteRequestSerializer, RouteResponseSerializer


@extend_schema(tags=['Fuel Route APIs'])
class FuelRoutePlannerAPIView(APIView):
    """
    Single comprehensive API endpoint for fuel route planning
    
    Uses OSRM (Open Source Routing Machine) - completely free, no API key required!
    """
    
    def _plan_route(self, start, destination):
        """Helper method to plan route and serialize response"""
        # Use OSRM service (free, no API key!)
        route_service = RouteService()
        route_plan = route_service.plan_route(start, destination)
        
        response_data = {
            'start_location': route_plan['start_location'],
            'end_location': route_plan['end_location'],
            'total_distance_miles': route_plan['total_distance_miles'],
            'total_distance_km': route_plan['total_distance_km'],
            'total_duration_hours': route_plan['total_duration_hours'],
            'total_fuel_gallons': route_plan['total_fuel_gallons'],
            'total_fuel_cost': route_plan['total_fuel_cost'],
            'route_geometry': route_plan['route_geometry']
        }
        
        return response_data

    @extend_schema(
        request=RouteRequestSerializer,
        responses={200: RouteResponseSerializer},
        parameters=[
            OpenApiParameter(
                name='start',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Starting location within USA (e.g., "Dallas, TX")',
                required=True
            ),
            OpenApiParameter(
                name='destination',
                type=OpenApiTypes.STR,
                location=OpenApiParameter.QUERY,
                description='Destination location within USA (e.g., "Houston, TX")',
                required=True
            ),
        ]
    )
    def get(self, request):
        """Handle GET requests for route planning"""
        serializer = RouteRequestSerializer(data=request.query_params)
        
        if not serializer.is_valid():
            return Response(
                {'error': 'Invalid input', 'details': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )
        
        start = serializer.validated_data['start']
        destination = serializer.validated_data['destination']
        
        try:
            response_data = self._plan_route(start, destination)
            return Response(response_data, status=status.HTTP_200_OK)
                
        except ValueError as e:
            return Response(
                {'error': str(e)},
                status=status.HTTP_400_BAD_REQUEST
            )
        except Exception as e:
            return Response(
                {'error': 'An error occurred while planning the route', 'details': str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )
    
