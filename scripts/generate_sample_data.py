#!/usr/bin/env python3
"""
generate_sample_data.py - Generate sample energy sensor data for OpenSearch demo

This script creates realistic energy sector data across multiple days,
including various asset types and sensor readings.

Usage:
    pip3 install opensearch-py
    python3 scripts/generate_sample_data.py

Requirements:
    - Python 3.8+
    - opensearch-py
    - OpenSearch running on localhost:9200
"""

from opensearchpy import OpenSearch, helpers
from datetime import datetime, timedelta
import random
import uuid

# Configuration
OPENSEARCH_HOST = 'localhost'
OPENSEARCH_PORT = 9200
INDEX_NAME = 'energy-sensor-readings'

# Data generation settings
DAYS_OF_DATA = 7  # Generate 7 days of historical data
READINGS_PER_DAY = 1000  # Number of readings per day

# Asset types and their characteristics
ASSET_TYPES = {
    'wind_turbine': {
        'count': 50,
        'power_range': (0, 3000),  # kW
        'temp_range': (20, 80),
        'efficiency_range': (75, 98),
    },
    'solar_panel': {
        'count': 100,
        'power_range': (0, 500),  # kW
        'temp_range': (25, 70),
        'efficiency_range': (80, 95),
    },
    'substation': {
        'count': 20,
        'power_range': (1000, 50000),  # kW
        'temp_range': (30, 90),
        'efficiency_range': (95, 99),
    },
    'transmission_line': {
        'count': 30,
        'power_range': (5000, 100000),  # kW
        'temp_range': (15, 60),
        'efficiency_range': (97, 99.5),
    }
}

FACILITIES = [
    'North Wind Farm',
    'South Wind Farm', 
    'East Solar Array',
    'West Solar Array',
    'Central Substation',
    'Coastal Power Plant',
    'Mountain Wind Complex',
    'Desert Solar Farm',
    'River Hydroelectric',
    'Industrial Grid Hub'
]

ALERT_LEVELS = ['normal', 'normal', 'normal', 'normal', 'warning', 'critical']  # Weighted
OPERATIONAL_STATUS = ['online', 'online', 'online', 'online', 'maintenance', 'offline']


def connect_opensearch():
    """Connect to OpenSearch cluster"""
    client = OpenSearch(
        hosts=[{'host': OPENSEARCH_HOST, 'port': OPENSEARCH_PORT}],
        http_compress=True,
        use_ssl=False,
        verify_certs=False
    )
    info = client.info()
    print(f"✓ Connected to OpenSearch {info['version']['number']}")
    return client


def create_index_if_not_exists(client):
    """Create the index with proper mappings if it doesn't exist"""
    if client.indices.exists(index=INDEX_NAME):
        print(f"✓ Index '{INDEX_NAME}' already exists")
        return
    
    mappings = {
        "settings": {
            "number_of_shards": 3,
            "number_of_replicas": 1,
            "index.refresh_interval": "5s"
        },
        "mappings": {
            "properties": {
                "asset_id": {"type": "keyword"},
                "asset_name": {
                    "type": "text",
                    "fields": {"keyword": {"type": "keyword"}}
                },
                "asset_type": {"type": "keyword"},
                "facility_id": {"type": "keyword"},
                "facility_name": {
                    "type": "text",
                    "fields": {"keyword": {"type": "keyword"}}
                },
                "region": {"type": "keyword"},
                "reading_timestamp": {"type": "date"},
                "reading_id": {"type": "keyword"},
                "power_output": {"type": "float"},
                "voltage": {"type": "float"},
                "current": {"type": "float"},
                "temperature": {"type": "float"},
                "vibration_level": {"type": "float"},
                "frequency": {"type": "float"},
                "power_factor": {"type": "float"},
                "ambient_temperature": {"type": "float"},
                "wind_speed": {"type": "float"},
                "solar_irradiance": {"type": "float"},
                "operational_status": {"type": "keyword"},
                "alert_level": {"type": "keyword"},
                "efficiency": {"type": "float"},
                "capacity_factor": {"type": "float"},
                "location": {"type": "geo_point"}
            }
        }
    }
    
    client.indices.create(index=INDEX_NAME, body=mappings)
    print(f"✓ Created index '{INDEX_NAME}'")


def generate_reading(asset_type, asset_num, facility, timestamp):
    """Generate a single sensor reading"""
    config = ASSET_TYPES[asset_type]
    
    # Add some time-of-day variation for solar panels
    hour = timestamp.hour
    if asset_type == 'solar_panel':
        # Solar output varies with time of day
        if 6 <= hour <= 18:
            solar_factor = 1 - abs(hour - 12) / 12
        else:
            solar_factor = 0
        power_min, power_max = config['power_range']
        power_output = random.uniform(power_min, power_max) * solar_factor
    else:
        power_output = random.uniform(*config['power_range'])
    
    # Add some randomness to simulate real sensor data
    temperature = random.uniform(*config['temp_range'])
    efficiency = random.uniform(*config['efficiency_range'])
    
    # Occasionally create warning/critical conditions
    alert_level = random.choice(ALERT_LEVELS)
    if alert_level == 'warning':
        temperature += 15  # Higher temp for warnings
        efficiency -= 10
    elif alert_level == 'critical':
        temperature += 30
        efficiency -= 25
    
    return {
        '_index': INDEX_NAME,
        '_id': str(uuid.uuid4()),
        '_source': {
            'asset_id': str(uuid.uuid4()),
            'asset_name': f"{asset_type.replace('_', ' ').title()}-{facility[:3].upper()}-{asset_num:03d}",
            'asset_type': asset_type,
            'facility_id': str(uuid.uuid4()),
            'facility_name': facility,
            'reading_timestamp': timestamp.isoformat(),
            'reading_id': str(uuid.uuid4()),
            
            # Power metrics
            'power_output': round(power_output, 2),
            'voltage': round(random.uniform(380, 420), 2),
            'current': round(random.uniform(100, 500), 2),
            'frequency': round(random.uniform(49.8, 50.2), 2),
            'power_factor': round(random.uniform(0.85, 0.99), 3),
            
            # Equipment status
            'temperature': round(temperature, 1),
            'vibration_level': round(random.uniform(0.5, 8.0), 2),
            'efficiency': round(max(0, min(100, efficiency)), 1),
            'capacity_factor': round(random.uniform(0.2, 0.95), 2),
            
            # Environmental
            'ambient_temperature': round(random.uniform(10, 35), 1),
            'wind_speed': round(random.uniform(0, 25), 1),
            'solar_irradiance': round(random.uniform(0, 1000), 1),
            
            # Status
            'operational_status': random.choice(OPERATIONAL_STATUS),
            'alert_level': alert_level,
            
            # Location (random US coordinates)
            'location': {
                'lat': round(random.uniform(30, 45), 4),
                'lon': round(random.uniform(-120, -75), 4)
            }
        }
    }


def generate_documents():
    """Generate all sample documents"""
    print(f"\nGenerating {DAYS_OF_DATA} days of sample data...")
    
    end_date = datetime.now()
    start_date = end_date - timedelta(days=DAYS_OF_DATA)
    
    doc_count = 0
    
    for day_offset in range(DAYS_OF_DATA):
        current_date = start_date + timedelta(days=day_offset)
        print(f"  Generating data for {current_date.strftime('%Y-%m-%d')}...")
        
        for _ in range(READINGS_PER_DAY):
            # Random time during the day
            random_hour = random.randint(0, 23)
            random_minute = random.randint(0, 59)
            random_second = random.randint(0, 59)
            timestamp = current_date.replace(
                hour=random_hour, 
                minute=random_minute, 
                second=random_second
            )
            
            # Generate reading for a random asset
            asset_type = random.choice(list(ASSET_TYPES.keys()))
            asset_num = random.randint(1, ASSET_TYPES[asset_type]['count'])
            facility = random.choice(FACILITIES)
            
            yield generate_reading(asset_type, asset_num, facility, timestamp)
            doc_count += 1
    
    print(f"  Total documents generated: {doc_count:,}")


def load_to_opensearch(client):
    """Bulk load documents to OpenSearch"""
    print("\nLoading data into OpenSearch...")
    
    success, failed = helpers.bulk(
        client,
        generate_documents(),
        chunk_size=500,
        request_timeout=60
    )
    
    return success, failed


def main():
    print("\n" + "=" * 60)
    print("  Energy Sensor Data Generator for OpenSearch")
    print("=" * 60)
    
    # Connect
    client = connect_opensearch()
    
    # Create index
    create_index_if_not_exists(client)
    
    # Load data
    success, failed = load_to_opensearch(client)
    
    # Refresh index
    client.indices.refresh(index=INDEX_NAME)
    
    # Get final count
    count = client.count(index=INDEX_NAME)['count']
    
    print("\n" + "=" * 60)
    print(f"  ✓ Data generation complete!")
    print(f"    Documents indexed: {success:,}")
    print(f"    Failed: {failed}")
    print(f"    Total in index: {count:,}")
    print("=" * 60)
    print("\nNext steps:")
    print("  1. Open OpenSearch Dashboards: http://localhost:5601")
    print("  2. Set time filter to 'Last 7 days'")
    print("  3. Refresh your visualizations")
    print("=" * 60 + "\n")


if __name__ == "__main__":
    main()

