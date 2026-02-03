#!/usr/bin/env python3
"""
sync_to_opensearch.py - Sync energy sensor data from Cassandra to OpenSearch

This script demonstrates the ETL pattern for energy sector data:
1. Extract from Cassandra (operational database)
2. Transform for search optimization (add geo_point, denormalize)
3. Load into OpenSearch (search & visualization layer)

Usage:
    # watsonx.data managed OpenSearch (recommended): set env vars, then run
    export OPENSEARCH_URL="https://<your-watsonx-opensearch-endpoint>:9200"
    export OPENSEARCH_USERNAME="your-username"
    export OPENSEARCH_PASSWORD="your-password"
    python3 scripts/sync_to_opensearch.py

    # Docker OpenSearch: no env vars needed (defaults to localhost:9200)
    python3 scripts/sync_to_opensearch.py

Requirements:
    - Python 3.8+
    - cassandra-driver
    - opensearch-py
    - Cassandra running with energy_ks keyspace
    - OpenSearch: watsonx.data managed (set OPENSEARCH_* env vars) or local (e.g. Docker on localhost:9200)
"""

from cassandra.cluster import Cluster
from opensearchpy import OpenSearch, helpers
from datetime import datetime
import os
import sys
from urllib.parse import urlparse

# =============================================================================
# CONFIGURATION - Cassandra (edit or use env); OpenSearch from env vars
# =============================================================================

CASSANDRA_HOST = os.environ.get('CASSANDRA_HOST', '<your-ec2-private-ip>')
CASSANDRA_KEYSPACE = os.environ.get('CASSANDRA_KEYSPACE', 'energy_ks')
CASSANDRA_TABLE = os.environ.get('CASSANDRA_TABLE', 'sensor_readings_by_asset')

# OpenSearch: use env vars for watsonx.data managed (default), or fallback to local Docker
OPENSEARCH_URL = os.environ.get('OPENSEARCH_URL')  # watsonx.data managed OpenSearch endpoint
OPENSEARCH_USERNAME = os.environ.get('OPENSEARCH_USERNAME')
OPENSEARCH_PASSWORD = os.environ.get('OPENSEARCH_PASSWORD')
OPENSEARCH_INDEX = os.environ.get('OPENSEARCH_INDEX', 'energy-sensor-readings')

BATCH_SIZE = int(os.environ.get('OPENSEARCH_SYNC_BATCH_SIZE', '100000'))

# =============================================================================
# CONNECTION FUNCTIONS
# =============================================================================

def connect_cassandra():
    """Connect to Cassandra cluster"""
    try:
        cluster = Cluster([CASSANDRA_HOST])
        session = cluster.connect(CASSANDRA_KEYSPACE)
        print(f"✓ Connected to Cassandra at {CASSANDRA_HOST}")
        return cluster, session
    except Exception as e:
        print(f"✗ Failed to connect to Cassandra: {e}")
        print(f"  Make sure CASSANDRA_HOST is set correctly (current: {CASSANDRA_HOST})")
        sys.exit(1)


def _opensearch_config():
    """Build OpenSearch client config from OPENSEARCH_URL or OPENSEARCH_HOST/PORT env vars."""
    if OPENSEARCH_URL:
        parsed = urlparse(OPENSEARCH_URL)
        host = parsed.hostname or 'localhost'
        port = parsed.port or (443 if parsed.scheme == 'https' else 9200)
        use_ssl = parsed.scheme == 'https'
    else:
        host = os.environ.get('OPENSEARCH_HOST', 'localhost')
        port = int(os.environ.get('OPENSEARCH_PORT', '9200'))
        use_ssl = False
    hosts = [{'host': host, 'port': port}]
    kwargs = {
        'hosts': hosts,
        'http_compress': True,
        'use_ssl': use_ssl,
        'verify_certs': use_ssl,
        'timeout': 60,
    }
    if OPENSEARCH_USERNAME and OPENSEARCH_PASSWORD:
        kwargs['http_auth'] = (OPENSEARCH_USERNAME, OPENSEARCH_PASSWORD)
    return kwargs


def connect_opensearch():
    """Connect to OpenSearch cluster (watsonx.data managed or Docker)."""
    try:
        client = OpenSearch(**_opensearch_config())
        info = client.info()
        print(f"✓ Connected to OpenSearch {info['version']['number']}")
        return client
    except Exception as e:
        print(f"✗ Failed to connect to OpenSearch: {e}")
        if OPENSEARCH_URL:
            print(f"  Check OPENSEARCH_URL, OPENSEARCH_USERNAME, OPENSEARCH_PASSWORD")
        else:
            print(f"  For Docker: ensure OpenSearch is running and SSH tunnel is active")
            print(f"  SSH tunnel: ssh -L 9200:localhost:9200 ec2-user@<your-ec2-ip>")
        sys.exit(1)


# =============================================================================
# DATA FUNCTIONS
# =============================================================================

def fetch_sensor_readings(session, batch_size):
    """
    Fetch sensor readings from Cassandra.
    
    In production, you'd typically:
    - Filter by time range for incremental loads
    - Use token-aware pagination for large datasets
    """
    query = f"SELECT * FROM {CASSANDRA_TABLE} LIMIT {batch_size}"
    print(f"  Fetching up to {batch_size:,} readings from Cassandra...")
    return session.execute(query)


def transform_for_opensearch(row):
    """
    Transform a Cassandra row into an OpenSearch document.
    
    Key transformations:
    - Convert UUIDs to strings (OpenSearch doesn't support UUID type)
    - Create geo_point from lat/lon for map visualizations
    - Format timestamp for OpenSearch date type
    """
    return {
        '_index': OPENSEARCH_INDEX,
        '_id': str(row.reading_id),
        '_source': {
            # Identifiers
            'asset_id': str(row.asset_id),
            'asset_name': row.asset_name,
            'asset_type': row.asset_type,
            'facility_id': str(row.facility_id),
            'facility_name': row.facility_name,
            'region': row.region,
            'reading_id': str(row.reading_id),
            
            # Timestamp
            'reading_timestamp': row.reading_timestamp.isoformat() if row.reading_timestamp else None,
            
            # Sensor measurements
            'power_output': row.power_output,
            'voltage': row.voltage,
            'current': row.current,
            'temperature': row.temperature,
            'vibration_level': row.vibration_level,
            'frequency': row.frequency,
            'power_factor': row.power_factor,
            
            # Environmental data
            'ambient_temperature': row.ambient_temperature,
            'wind_speed': row.wind_speed,
            'solar_irradiance': row.solar_irradiance,
            
            # Status
            'operational_status': row.operational_status,
            'alert_level': row.alert_level,
            'efficiency': row.efficiency,
            'capacity_factor': row.capacity_factor,
            
            # Geo-location (for maps)
            'location': {
                'lat': row.latitude,
                'lon': row.longitude
            } if hasattr(row, 'latitude') and row.latitude and row.longitude else None
        }
    }


def load_to_opensearch(client, rows):
    """
    Bulk load documents into OpenSearch.
    
    Uses the bulk API for efficiency - much faster than individual inserts.
    """
    def generate_actions():
        count = 0
        for row in rows:
            yield transform_for_opensearch(row)
            count += 1
            if count % 10000 == 0:
                print(f"    Processed {count:,} documents...")
        print(f"    Total processed: {count:,} documents")
    
    print("  Loading into OpenSearch...")
    success, failed = helpers.bulk(
        client,
        generate_actions(),
        chunk_size=1000,
        request_timeout=60
    )
    return success, failed


# =============================================================================
# MAIN
# =============================================================================

def main():
    print("\n" + "=" * 60)
    print("  Energy Sensor Data → OpenSearch Sync")
    print("=" * 60 + "\n")
    
    # Check configuration
    if CASSANDRA_HOST == '<your-ec2-private-ip>':
        print("✗ ERROR: Please update CASSANDRA_HOST in this script")
        print("  Edit the script and set your EC2 private IP address")
        sys.exit(1)
    
    # Connect to data sources
    print("Step 1: Connecting to data sources")
    cassandra_cluster, cassandra_session = connect_cassandra()
    opensearch_client = connect_opensearch()
    
    # Extract
    print("\nStep 2: Extracting from Cassandra")
    rows = fetch_sensor_readings(cassandra_session, batch_size=BATCH_SIZE)
    
    # Transform & Load
    print("\nStep 3: Transforming and Loading to OpenSearch")
    success, failed = load_to_opensearch(opensearch_client, rows)
    
    # Summary
    print("\n" + "=" * 60)
    print(f"  ✓ Sync Complete!")
    print(f"    Documents indexed: {success:,}")
    print(f"    Failed: {failed}")
    print("=" * 60)
    
    # Verify
    print("\nStep 4: Verifying in OpenSearch")
    count = opensearch_client.count(index=OPENSEARCH_INDEX)['count']
    print(f"  Total documents in index: {count:,}")
    
    print("\n✓ Done! Open OpenSearch Dashboards to view data")
    print("  (Managed: use your Dashboards URL; Docker: http://localhost:5601)")
    print("  Set time filter to 'Last 7 days' to see the data\n")
    
    # Cleanup
    cassandra_cluster.shutdown()


if __name__ == "__main__":
    main()

