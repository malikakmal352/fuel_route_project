"""
Route planning and fuel optimization services using OSRM (no API key needed)
"""
import requests
from geopy.geocoders import Nominatim
from geopy.distance import geodesic
from route_planner.models import TruckStop
from decimal import Decimal


class RouteService:
    """Service for calculating routes and optimizing fuel stops using OSRM"""
    
    MAX_RANGE_MILES = 500  # Maximum range before refueling
    FUEL_EFFICIENCY_MPG = 10  # Miles per gallon
    BUFFER_MILES = 50  # Safety buffer before running out of fuel
    
    # OSRM public API - completely free, no API key required
    OSRM_BASE_URL = "http://router.project-osrm.org"
    
    def __init__(self):
        self.geocoder = Nominatim(user_agent="fuel_route_planner")
    
    def geocode_location(self, location_string):
        """
        Convert a location string to coordinates
        
        Args:
            location_string: Address or place name
            
        Returns:
            dict: {'latitude': float, 'longitude': float, 'display_name': str}
        """
        try:
            # Add USA to help with geocoding accuracy
            if "USA" not in location_string.upper() and "UNITED STATES" not in location_string.upper():
                location_string += ", USA"
            
            location = self.geocoder.geocode(location_string)
            if not location:
                raise ValueError(f"Could not geocode location: {location_string}")
            
            return {
                'latitude': location.latitude,
                'longitude': location.longitude,
                'display_name': location.address
            }
        except Exception as e:
            raise ValueError(f"Geocoding error for '{location_string}': {str(e)}")
    
    def get_route(self, start_coords, end_coords):
        """
        Get route from OSRM (Open Source Routing Machine)
        Completely free, no API key required!
        
        Args:
            start_coords: (longitude, latitude) tuple
            end_coords: (longitude, latitude) tuple
            
        Returns:
            dict: Route information including geometry and distance
        """
        try:
            # OSRM API endpoint
            url = f"{self.OSRM_BASE_URL}/route/v1/driving/{start_coords[0]},{start_coords[1]};{end_coords[0]},{end_coords[1]}"
            
            # Parameters
            params = {
                'overview': 'full',
                'geometries': 'geojson',
                'steps': 'false'
            }
            
            response = requests.get(url, params=params, timeout=30)
            response.raise_for_status()
            
            data = response.json()
            
            if data.get('code') != 'Ok':
                raise ValueError(f"OSRM API error: {data.get('message', 'Unknown error')}")
            
            route = data['routes'][0]
            
            # Convert to our expected format
            return {
                'geometry': route['geometry'],
                'distance_meters': route['distance'],
                'duration_seconds': route['duration']
            }
            
        except requests.exceptions.RequestException as e:
            raise ValueError(f"Could not calculate route: {str(e)}")
        except Exception as e:
            raise ValueError(f"Route calculation error: {str(e)}")
    
    def calculate_distance_miles(self, coord1, coord2):
        """
        Calculate distance between two coordinates in miles
        
        Args:
            coord1: (latitude, longitude) tuple
            coord2: (latitude, longitude) tuple
            
        Returns:
            float: Distance in miles
        """
        return geodesic(coord1, coord2).miles
    
    def find_optimal_fuel_stops(self, route_coords, total_distance_miles):
        """
        Find optimal fuel stops along the route based on price and distance
        Returns TruckStop model instances with additional attributes
        
        Args:
            route_coords: List of (longitude, latitude) tuples along the route
            total_distance_miles: Total route distance in miles
            
        Returns:
            list: TruckStop model instances with additional attributes
        """
        fuel_stops = []
        current_distance = 0
        last_fuel_latitude = route_coords[0][1]
        last_fuel_longitude = route_coords[0][0]
        
        # Get all truck stops with coordinates
        all_stops = TruckStop.objects.filter(
            latitude__isnull=False,
            longitude__isnull=False
        ).order_by('retail_price')
        
        if not all_stops.exists():
            return []
        
        # Calculate fuel stop intervals
        max_distance_between_stops = self.MAX_RANGE_MILES - self.BUFFER_MILES
        
        while current_distance < total_distance_miles:
            # Find stops within range along the route
            next_fuel_distance = min(
                current_distance + max_distance_between_stops,
                total_distance_miles
            )
            
            # Find target point on route
            target_point = self._find_point_at_distance(
                route_coords,
                (last_fuel_longitude, last_fuel_latitude),
                next_fuel_distance - current_distance
            )
            
            if not target_point:
                break
            
            # Find nearest affordable truck stop
            best_stop = self._find_nearest_stop_to_point(
                all_stops,
                target_point,
                max_search_radius_miles=100
            )
            
            if best_stop:
                distance_from_last = self.calculate_distance_miles(
                    (last_fuel_latitude, last_fuel_longitude),
                    (best_stop.latitude, best_stop.longitude)
                )
                
                current_distance += distance_from_last
                fuel_needed = distance_from_last / self.FUEL_EFFICIENCY_MPG
                fuel_cost = float(best_stop.retail_price) * fuel_needed
                
                # Add dynamic attributes to the model instance
                best_stop.distance_from_start = round(current_distance, 2)
                best_stop.fuel_needed = round(fuel_needed, 2)
                best_stop.cost = round(Decimal(str(fuel_cost)), 2)
                
                fuel_stops.append(best_stop)
                
                last_fuel_latitude = best_stop.latitude
                last_fuel_longitude = best_stop.longitude
            else:
                # No stop found, move to next segment
                current_distance = next_fuel_distance
                last_fuel_latitude = target_point[1]
                last_fuel_longitude = target_point[0]
        
        # Add final segment fuel calculation
        if fuel_stops and current_distance < total_distance_miles:
            final_distance = total_distance_miles - current_distance
            final_fuel = final_distance / self.FUEL_EFFICIENCY_MPG
            final_cost = float(fuel_stops[-1].retail_price) * final_fuel
            
            # Update last stop with additional fuel
            fuel_stops[-1].fuel_needed += round(final_fuel, 2)
            fuel_stops[-1].cost += round(Decimal(str(final_cost)), 2)
        
        return fuel_stops
    
    def _find_point_at_distance(self, route_coords, start_point, target_distance_miles):
        """Find a point along the route at approximately target_distance_miles from start_point"""
        accumulated_distance = 0
        
        for i in range(len(route_coords) - 1):
            point1 = (route_coords[i][1], route_coords[i][0])
            point2 = (route_coords[i + 1][1], route_coords[i + 1][0])
            segment_distance = self.calculate_distance_miles(point1, point2)
            
            if accumulated_distance + segment_distance >= target_distance_miles:
                # Target is in this segment
                return route_coords[i + 1]
            
            accumulated_distance += segment_distance
        
        # Return last point if we've gone through all segments
        return route_coords[-1] if route_coords else None
    
    def _find_nearest_stop_to_point(self, truck_stops, point, max_search_radius_miles=100):
        """Find the nearest truck stop to a given point, sorted by price"""
        point_lat_lon = (point[1], point[0])
        
        nearest_stop = None
        min_distance = float('inf')
        
        for stop in truck_stops:
            stop_lat_lon = (stop.latitude, stop.longitude)
            distance = self.calculate_distance_miles(point_lat_lon, stop_lat_lon)
            
            if distance < max_search_radius_miles and distance < min_distance:
                min_distance = distance
                nearest_stop = stop
        
        return nearest_stop
    
    def calculate_total_fuel_cost(self, fuel_stops):
        """Calculate total fuel cost from all stops - works with model instances"""
        return sum(Decimal(str(stop.cost)) for stop in fuel_stops)
    
    def calculate_total_fuel_gallons(self, total_distance_miles):
        """Calculate total fuel needed for the trip"""
        return total_distance_miles / self.FUEL_EFFICIENCY_MPG
    
    def plan_route(self, start_location, end_location):
        """
        Main method to plan a complete route with fuel stops using OSRM
        
        Args:
            start_location: Starting address or coordinates
            end_location: Ending address or coordinates
            
        Returns:
            dict: Complete route plan with fuel stops and costs
        """
        # Geocode locations
        start = self.geocode_location(start_location)
        end = self.geocode_location(end_location)
        
        # Get route from OSRM (FREE API - no key needed!)
        route_data = self.get_route(
            (start['longitude'], start['latitude']),
            (end['longitude'], end['latitude'])
        )
        
        # Extract route information
        geometry = route_data['geometry']
        distance_meters = route_data['distance_meters']
        duration_seconds = route_data['duration_seconds']
        
        # Convert to miles and hours
        total_distance_km = distance_meters / 1000
        total_distance_miles = total_distance_km * 0.621371
        total_duration_hours = duration_seconds / 3600
        
        # Get route coordinates for fuel stop finding
        route_coords = geometry['coordinates']
        
        # Find optimal fuel stops
        fuel_stops = self.find_optimal_fuel_stops(route_coords, total_distance_miles)
        
        # Calculate totals
        total_fuel_gallons = self.calculate_total_fuel_gallons(total_distance_miles)
        total_fuel_cost = self.calculate_total_fuel_cost(fuel_stops)
        
        # Create list of all stops with their cumulative distances in km
        all_stops_with_distances = []
        
        # Start point
        all_stops_with_distances.append({
            'cumulative_distance_km': 0,
            'type': 'start',
            'data': {
                'coordinates': [start['longitude'], start['latitude']],
                'latitude': start['latitude'],
                'longitude': start['longitude'],
                'address': start['display_name'],
                'retail_price': None
            }
        })
        
        # Add fuel stops with their cumulative distances
        for stop in fuel_stops:
            cumulative_km = stop.distance_from_start * 1.60934  # Convert miles to km
            all_stops_with_distances.append({
                'cumulative_distance_km': cumulative_km,
                'type': 'fuel_stop',
                'data': {
                    'coordinates': [stop.longitude, stop.latitude],
                    'latitude': stop.latitude,
                    'longitude': stop.longitude,
                    'address': stop.address,
                    'city': stop.city,
                    'state': stop.state,
                    'name': stop.truckstop_name,
                    'retail_price': float(stop.retail_price)
                }
            })
        
        # End point
        all_stops_with_distances.append({
            'cumulative_distance_km': total_distance_km,
            'type': 'end',
            'data': {
                'coordinates': [end['longitude'], end['latitude']],
                'latitude': end['latitude'],
                'longitude': end['longitude'],
                'address': end['display_name'],
                'retail_price': None
            }
        })
        
        # Sort by cumulative distance to ensure correct order
        all_stops_with_distances.sort(key=lambda x: x['cumulative_distance_km'])
        
        # Ensure the last point is always 'end' - remove any fuel stops beyond the end
        filtered_stops = []
        for stop in all_stops_with_distances:
            if stop['type'] == 'end' or stop['cumulative_distance_km'] <= total_distance_km:
                filtered_stops.append(stop)
        
        # Make sure end is the last element
        end_point = next((s for s in filtered_stops if s['type'] == 'end'), None)
        if end_point:
            filtered_stops = [s for s in filtered_stops if s['type'] != 'end']
            filtered_stops.append(end_point)
        
        all_stops_with_distances = filtered_stops
        
        # Calculate distance_to_next_stop_km and assign position labels after sorting
        key_points = []
        fuel_stop_counter = 1
        
        for i, stop_info in enumerate(all_stops_with_distances):
            point = stop_info['data'].copy()
            
            # Assign position label based on type
            if stop_info['type'] == 'start':
                point['position'] = 'start'
            elif stop_info['type'] == 'end':
                point['position'] = 'end'
            elif stop_info['type'] == 'fuel_stop':
                point['position'] = f'fuel_stop_{fuel_stop_counter}'
                fuel_stop_counter += 1
            
            # Calculate distance to next stop
            if i < len(all_stops_with_distances) - 1:
                distance_km = all_stops_with_distances[i + 1]['cumulative_distance_km'] - stop_info['cumulative_distance_km']
                distance_miles = distance_km * 0.621371  # Convert km to miles
                point['distance_to_next_stop_miles'] = round(distance_miles, 2)
            else:
                point['distance_to_next_stop_miles'] = None  # Last stop
            
            key_points.append(point)
        
        route_summary = {
            'type': 'LineString',
            'total_points': len(route_coords),
            'key_points': key_points
        }
        
        return {
            'start_location': start,
            'end_location': end,
            'total_distance_miles': round(total_distance_miles, 2),
            'total_distance_km': round(total_distance_km, 2),
            'total_duration_hours': round(total_duration_hours, 2),
            'total_fuel_gallons': round(total_fuel_gallons, 2),
            'total_fuel_cost': total_fuel_cost,
            'fuel_stops': fuel_stops,
            'route_geometry': route_summary
        }
