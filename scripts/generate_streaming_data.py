#!/usr/bin/env python3
"""
generate_streaming_data.py - Generate continuous streaming data for alert testing

This script sends new sensor readings every few seconds to trigger all 3 alerts:
  1. High Temperature (>= 85°C)
  2. Low Efficiency (<= 60%)
  3. High Vibration (>= 7)

Usage:
    # watsonx.data managed OpenSearch: set OPENSEARCH_URL, OPENSEARCH_USERNAME, OPENSEARCH_PASSWORD
    # Docker OpenSearch: python3 scripts/generate_streaming_data.py (no env vars needed)

Requirements:
    - Python 3.8+
    - opensearch-py
    - OpenSearch: watsonx.data managed (set OPENSEARCH_* env vars) or local (e.g. Docker on localhost:9200)
"""

from opensearchpy import OpenSearch
from datetime import datetime
import os
import random
import uuid
import time
from urllib.parse import urlparse

# Configuration - from environment (managed) or localhost (Docker)
OPENSEARCH_URL = os.environ.get('OPENSEARCH_URL')
OPENSEARCH_USERNAME = os.environ.get('OPENSEARCH_USERNAME')
OPENSEARCH_PASSWORD = os.environ.get('OPENSEARCH_PASSWORD')
INDEX_NAME = os.environ.get('OPENSEARCH_INDEX', 'energy-sensor-readings')

# How often to send data (seconds)
INTERVAL = 5

ASSET_TYPES = ['wind_turbine', 'solar_panel', 'substation', 'transmission_line']
FACILITIES = [
    'North Wind Farm', 'South Wind Farm', 'East Solar Array',
    'West Solar Array', 'Central Substation', 'Coastal Power Plant'
]


def _opensearch_config():
    """Build OpenSearch client config from OPENSEARCH_URL or OPENSEARCH_HOST/PORT."""
    if OPENSEARCH_URL:
        parsed = urlparse(OPENSEARCH_URL)
        host = parsed.hostname or 'localhost'
        port = parsed.port or (443 if parsed.scheme == 'https' else 9200)
        use_ssl = parsed.scheme == 'https'
    else:
        host = os.environ.get('OPENSEARCH_HOST', 'localhost')
        port = int(os.environ.get('OPENSEARCH_PORT', '9200'))
        use_ssl = False
    kwargs = {
        'hosts': [{'host': host, 'port': port}],
        'http_compress': True,
        'use_ssl': use_ssl,
        'verify_certs': use_ssl,
    }
    if OPENSEARCH_USERNAME and OPENSEARCH_PASSWORD:
        kwargs['http_auth'] = (OPENSEARCH_USERNAME, OPENSEARCH_PASSWORD)
    return kwargs


def connect_opensearch():
    """Connect to OpenSearch (watsonx.data managed or Docker)."""
    client = OpenSearch(**_opensearch_config())
    info = client.info()
    print(f"✓ Connected to OpenSearch {info['version']['number']}")
    return client


def generate_reading(alert_type=None):
    """
    Generate a single sensor reading.
    
    alert_type can be:
      - 'high_temp': Temperature >= 85°C (triggers Alert 1)
      - 'low_efficiency': Efficiency <= 60% (triggers Alert 2)
      - 'high_vibration': Vibration >= 7 (triggers Alert 3)
      - None: Normal reading
    """
    asset_type = random.choice(ASSET_TYPES)
    facility = random.choice(FACILITIES)
    asset_num = random.randint(1, 50)
    
    # Default normal values
    temperature = random.uniform(30, 70)
    efficiency = random.uniform(75, 95)
    vibration_level = random.uniform(1, 5)
    alert_level = 'normal'
    
    # Override based on alert type
    if alert_type == 'high_temp':
        temperature = random.uniform(86, 105)  # >= 85°C triggers alert
        alert_level = 'critical' if temperature > 95 else 'warning'
    
    elif alert_type == 'low_efficiency':
        efficiency = random.uniform(40, 58)  # <= 60% triggers alert
        alert_level = 'warning'
    
    elif alert_type == 'high_vibration':
        vibration_level = random.uniform(7.2, 9.5)  # >= 7 triggers alert
        alert_level = 'critical' if vibration_level > 8 else 'warning'
    
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
        'vibration_level': round(vibration_level, 2),
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
    print("  Generating data to trigger ALL 3 alerts:")
    print("    🔥 Alert 1: High Temperature (>= 85°C)")
    print("    📉 Alert 2: Low Efficiency (<= 60%)")
    print("    📳 Alert 3: High Vibration (>= 7)")
    print("  Press Ctrl+C to stop")
    print("=" * 60 + "\n")
    
    client = connect_opensearch()
    
    count = 0
    alert_counts = {'high_temp': 0, 'low_efficiency': 0, 'high_vibration': 0, 'normal': 0}
    
    # Cycle through alert types to trigger all 3 alerts
    alert_cycle = ['high_temp', 'low_efficiency', 'high_vibration', 'normal', 'normal']
    
    try:
        while True:
            # Rotate through alert types
            alert_type = alert_cycle[count % len(alert_cycle)]
            
            reading = generate_reading(alert_type=alert_type)
            
            # Index the document
            client.index(
                index=INDEX_NAME,
                body=reading,
                refresh=True  # Make it immediately searchable
            )
            
            count += 1
            alert_counts[alert_type] += 1
            
            # Format output based on alert type
            if alert_type == 'high_temp':
                status = f"🔥 Temp: {reading['temperature']}°C"
            elif alert_type == 'low_efficiency':
                status = f"📉 Eff: {reading['efficiency']}%"
            elif alert_type == 'high_vibration':
                status = f"📳 Vib: {reading['vibration_level']}"
            else:
                status = f"✓ Normal"
            
            print(f"[{datetime.now().strftime('%H:%M:%S')}] #{count}: "
                  f"{reading['asset_name'][:25]:25} | {status:20} | {reading['alert_level']}")
            
            # Show summary every 10 readings
            if count % 10 == 0:
                print(f"\n  📊 Alert Summary:")
                print(f"     🔥 High Temp:    {alert_counts['high_temp']} readings")
                print(f"     📉 Low Eff:      {alert_counts['low_efficiency']} readings")
                print(f"     📳 High Vib:     {alert_counts['high_vibration']} readings")
                print(f"     ✓  Normal:       {alert_counts['normal']} readings")
                print(f"  All 3 alerts should be triggering!\n")
            
            time.sleep(INTERVAL)
            
    except KeyboardInterrupt:
        print(f"\n\n" + "=" * 60)
        print(f"  ✓ Stopped. Total readings sent: {count}")
        print(f"     🔥 High Temp:    {alert_counts['high_temp']}")
        print(f"     📉 Low Eff:      {alert_counts['low_efficiency']}")
        print(f"     📳 High Vib:     {alert_counts['high_vibration']}")
        print(f"     ✓  Normal:       {alert_counts['normal']}")
        print("=" * 60)


if __name__ == "__main__":
    main()

