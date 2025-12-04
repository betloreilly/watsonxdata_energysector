#!/usr/bin/env python3
"""
generate_streaming_data.py - Generate continuous streaming data for alert testing

This script sends new sensor readings every few seconds so you can test
OpenSearch alerts in real-time.

Usage:
    pip3 install opensearch-py
    python3 scripts/generate_streaming_data.py

Requirements:
    - Python 3.8+
    - opensearch-py
    - OpenSearch running on localhost:9200
"""

from opensearchpy import OpenSearch
from datetime import datetime
import random
import uuid
import time

# Configuration
OPENSEARCH_HOST = 'localhost'
OPENSEARCH_PORT = 9200
INDEX_NAME = 'energy-sensor-readings'

# How often to send data (seconds)
INTERVAL = 5

# Set to True to generate some high temperature readings for alert testing
GENERATE_ALERTS = True

ASSET_TYPES = ['wind_turbine', 'solar_panel', 'substation', 'transmission_line']
FACILITIES = [
    'North Wind Farm', 'South Wind Farm', 'East Solar Array',
    'West Solar Array', 'Central Substation', 'Coastal Power Plant'
]


def connect_opensearch():
    """Connect to OpenSearch"""
    client = OpenSearch(
        hosts=[{'host': OPENSEARCH_HOST, 'port': OPENSEARCH_PORT}],
        http_compress=True,
        use_ssl=False,
        verify_certs=False
    )
    info = client.info()
    print(f"✓ Connected to OpenSearch {info['version']['number']}")
    return client


def generate_reading(force_high_temp=False):
    """Generate a single sensor reading"""
    asset_type = random.choice(ASSET_TYPES)
    facility = random.choice(FACILITIES)
    asset_num = random.randint(1, 50)
    
    # Normal temperature range
    if force_high_temp:
        # Generate HIGH temperature for alert testing (above 85°C)
        temperature = random.uniform(86, 105)
        alert_level = 'critical' if temperature > 95 else 'warning'
        efficiency = random.uniform(40, 65)
    else:
        temperature = random.uniform(25, 75)
        alert_level = 'normal'
        efficiency = random.uniform(75, 98)
    
    return {
        'asset_id': str(uuid.uuid4()),
        'asset_name': f"{asset_type.replace('_', ' ').title()}-{facility[:3].upper()}-{asset_num:03d}",
        'asset_type': asset_type,
        'facility_id': str(uuid.uuid4()),
        'facility_name': facility,
        'reading_timestamp': datetime.now().isoformat(),
        'reading_id': str(uuid.uuid4()),
        
        'power_output': round(random.uniform(100, 5000), 2),
        'voltage': round(random.uniform(380, 420), 2),
        'current': round(random.uniform(100, 500), 2),
        'frequency': round(random.uniform(49.8, 50.2), 2),
        'power_factor': round(random.uniform(0.85, 0.99), 3),
        
        'temperature': round(temperature, 1),
        'vibration_level': round(random.uniform(0.5, 8.0), 2),
        'efficiency': round(efficiency, 1),
        'capacity_factor': round(random.uniform(0.2, 0.95), 2),
        
        'ambient_temperature': round(random.uniform(10, 35), 1),
        'wind_speed': round(random.uniform(0, 25), 1),
        'solar_irradiance': round(random.uniform(0, 1000), 1),
        
        'operational_status': 'online',
        'alert_level': alert_level,
        
        'location': {
            'lat': round(random.uniform(30, 45), 4),
            'lon': round(random.uniform(-120, -75), 4)
        }
    }


def main():
    print("\n" + "=" * 60)
    print("  Streaming Data Generator for Alert Testing")
    print("=" * 60)
    print(f"  Sending data every {INTERVAL} seconds")
    print(f"  Generate high temps for alerts: {GENERATE_ALERTS}")
    print("  Press Ctrl+C to stop")
    print("=" * 60 + "\n")
    
    client = connect_opensearch()
    
    count = 0
    high_temp_count = 0
    
    try:
        while True:
            # Every 3rd reading, generate a high temperature if GENERATE_ALERTS is True
            force_high_temp = GENERATE_ALERTS and (count % 3 == 0)
            
            reading = generate_reading(force_high_temp=force_high_temp)
            
            # Index the document
            client.index(
                index=INDEX_NAME,
                body=reading,
                refresh=True  # Make it immediately searchable
            )
            
            count += 1
            temp_str = f"🔥 {reading['temperature']}°C" if force_high_temp else f"✓ {reading['temperature']}°C"
            
            if force_high_temp:
                high_temp_count += 1
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] Sent reading #{count}: "
                  f"{reading['asset_name']} | Temp: {temp_str} | Alert: {reading['alert_level']}")
            
            if high_temp_count > 0 and high_temp_count % 5 == 0:
                print(f"\n  📊 High temp readings sent: {high_temp_count} (should trigger alert!)\n")
            
            time.sleep(INTERVAL)
            
    except KeyboardInterrupt:
        print(f"\n\n✓ Stopped. Total readings sent: {count}")
        print(f"  High temperature readings: {high_temp_count}")


if __name__ == "__main__":
    main()

