"""
Populate coordinates for truck stops in the database
Run this to add sample truck stops with pre-configured coordinates
"""
import os
import django

# Setup Django
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
django.setup()

from route_planner.models import TruckStop

def populate_coordinates():
    """Create sample truck stops with coordinates"""
    
    print("=" * 60)
    print("POPULATING TRUCK STOP COORDINATES")
    print("=" * 60)
    
    # Sample data with coordinates already included
    sample_stops = [
        {
            'truckstop_name': 'Pilot Travel Center Dallas',
            'address': '1234 Interstate Dr',
            'city': 'Dallas',
            'state': 'TX',
            'rack_id': 1001,
            'retail_price': 3.299,
            'latitude': 32.7767,
            'longitude': -96.7970
        },
        {
            'truckstop_name': "Love's Travel Stop Houston",
            'address': '5678 Highway 45',
            'city': 'Houston',
            'state': 'TX',
            'rack_id': 1002,
            'retail_price': 3.199,
            'latitude': 29.7604,
            'longitude': -95.3698
        },
        {
            'truckstop_name': 'Flying J Oklahoma City',
            'address': '9101 Route 66',
            'city': 'Oklahoma City',
            'state': 'OK',
            'rack_id': 1003,
            'retail_price': 3.399,
            'latitude': 35.4676,
            'longitude': -97.5164
        },
        {
            'truckstop_name': 'TA Travel Center Amarillo',
            'address': '1213 I-40 Exit 200',
            'city': 'Amarillo',
            'state': 'TX',
            'rack_id': 1004,
            'retail_price': 3.249,
            'latitude': 35.2220,
            'longitude': -101.8313
        },
        {
            'truckstop_name': 'Petro Stopping Center Fort Worth',
            'address': '1415 US-287',
            'city': 'Fort Worth',
            'state': 'TX',
            'rack_id': 1005,
            'retail_price': 3.349,
            'latitude': 32.7555,
            'longitude': -97.3308
        },
        {
            'truckstop_name': "Pilot Travel Center San Antonio",
            'address': '1617 I-35 N',
            'city': 'San Antonio',
            'state': 'TX',
            'rack_id': 1006,
            'retail_price': 3.279,
            'latitude': 29.4241,
            'longitude': -98.4936
        },
        {
            'truckstop_name': "Love's Travel Stop Texarkana",
            'address': '1819 Highway 59',
            'city': 'Texarkana',
            'state': 'TX',
            'rack_id': 1007,
            'retail_price': 3.229,
            'latitude': 33.4251,
            'longitude': -94.0477
        },
        {
            'truckstop_name': 'Shell Gas Station Austin',
            'address': '2021 Main St',
            'city': 'Austin',
            'state': 'TX',
            'rack_id': 1008,
            'retail_price': 3.449,
            'latitude': 30.2672,
            'longitude': -97.7431
        },
        {
            'truckstop_name': 'Chevron El Paso',
            'address': '2223 Oak Ave',
            'city': 'El Paso',
            'state': 'TX',
            'rack_id': 1009,
            'retail_price': 3.379,
            'latitude': 31.7619,
            'longitude': -106.4850
        },
        {
            'truckstop_name': 'Valero Lubbock',
            'address': '2425 Cedar Rd',
            'city': 'Lubbock',
            'state': 'TX',
            'rack_id': 1010,
            'retail_price': 3.319,
            'latitude': 33.5779,
            'longitude': -101.8552
        },
        {
            'truckstop_name': 'Flying J Memphis',
            'address': '3100 Airways Blvd',
            'city': 'Memphis',
            'state': 'TN',
            'rack_id': 1011,
            'retail_price': 3.259,
            'latitude': 35.0447,
            'longitude': -89.9773
        },
        {
            'truckstop_name': 'TA Travel Center Little Rock',
            'address': '4500 Interstate 40',
            'city': 'Little Rock',
            'state': 'AR',
            'rack_id': 1012,
            'retail_price': 3.289,
            'latitude': 34.7465,
            'longitude': -92.2896
        },
        {
            'truckstop_name': "Love's Travel Stop Shreveport",
            'address': '5200 Highway 20',
            'city': 'Shreveport',
            'state': 'LA',
            'rack_id': 1013,
            'retail_price': 3.179,
            'latitude': 32.5252,
            'longitude': -93.7502
        },
        {
            'truckstop_name': 'Pilot Travel Center Beaumont',
            'address': '6100 I-10 E',
            'city': 'Beaumont',
            'state': 'TX',
            'rack_id': 1014,
            'retail_price': 3.189,
            'latitude': 30.0802,
            'longitude': -94.1266
        },
        {
            'truckstop_name': 'Petro Stopping Center Waco',
            'address': '7800 I-35 S',
            'city': 'Waco',
            'state': 'TX',
            'rack_id': 1015,
            'retail_price': 3.269,
            'latitude': 31.5493,
            'longitude': -97.1467
        }
    ]
    
    created_count = 0
    updated_count = 0
    skipped_count = 0
    
    for stop_data in sample_stops:
        # Check if already exists by name and city
        existing = TruckStop.objects.filter(
            truckstop_name=stop_data['truckstop_name'],
            city=stop_data['city'],
            state=stop_data['state']
        ).first()
        
        if existing:
            # Update coordinates if they don't exist
            if not existing.latitude or not existing.longitude:
                existing.latitude = stop_data['latitude']
                existing.longitude = stop_data['longitude']
                existing.save()
                print(f"✓ Updated: {stop_data['truckstop_name']} - {stop_data['city']}, {stop_data['state']}")
                print(f"  Coordinates: ({stop_data['latitude']}, {stop_data['longitude']})")
                updated_count += 1
            else:
                print(f"⏭  Skipped: {stop_data['truckstop_name']} (already has coordinates)")
                skipped_count += 1
        else:
            # Create new truck stop
            TruckStop.objects.create(**stop_data)
            print(f"✓ Created: {stop_data['truckstop_name']} - {stop_data['city']}, {stop_data['state']}")
            print(f"  Address: {stop_data['address']}")
            print(f"  Coordinates: ({stop_data['latitude']}, {stop_data['longitude']})")
            print(f"  Price: ${stop_data['retail_price']}/gallon")
            created_count += 1
    
    print("\n" + "=" * 60)
    print("POPULATION COMPLETE!")
    print("=" * 60)
    print(f"✓ Created: {created_count} new truck stops")
    print(f"✓ Updated: {updated_count} existing truck stops")
    print(f"⏭ Skipped: {skipped_count} (already had coordinates)")
    print(f"Total in database: {TruckStop.objects.count()}")
    
    # Check how many have coordinates now
    with_coords = TruckStop.objects.filter(
        latitude__isnull=False,
        longitude__isnull=False
    ).count()
    print(f"With coordinates: {with_coords}")
    print("=" * 60)
    
    if with_coords > 0:
        print("\n✅ SUCCESS! Database is ready.")
        print("\nTest the API now:")
        print("  python test_api.py")
        print("\nOr test with curl:")
        print('  curl -X POST http://localhost:8000/api/fuel-route/ -H "Content-Type: application/json" -d "{\\"start\\": \\"Dallas, TX\\", \\"destination\\": \\"Houston, TX\\"}"')
    else:
        print("\n⚠️  No coordinates found. Something went wrong.")

if __name__ == '__main__':
    try:
        populate_coordinates()
    except Exception as e:
        print(f"\n❌ ERROR: {str(e)}")
        import traceback
        traceback.print_exc()
