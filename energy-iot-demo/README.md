# Energy IoT Demo - Maven Project

This is the Maven project for the Energy Sector IoT demo.

## Quick Build

```bash
cd energy-iot-demo
mvn clean package
```

**Result**: `target/energy-iot-demo-1.0.0.jar`

## Complete Documentation

**See the main README** in the parent directory:

```bash
cd ..
cat README.md
```

The main README contains:
- Complete installation instructions
- How to build this JAR
- How to load data
- How to run Spark jobs
- How to query results
- Troubleshooting

## Configuration

**IMPORTANT**: Before building, you MUST configure Cassandra connection settings.

See the main README's **Step 3: Build the Demo Application** for detailed instructions on:
1. Verifying your Cassandra datacenter name
2. Updating connection settings (host and datacenter)

Quick reference - update these in `src/main/java/com/ibm/wxd/datalabs/demo/cass_spark_iceberg/utils/CassUtil.java`:

```java
// Lines 21 and 23
private static final String CASSANDRA_HOST = "your-ec2-private-ip";  // NOT 127.0.0.1
private static final String CASSANDRA_DATACENTER = "datacenter1";  // Verify with nodetool status
```

⚠️ **These settings are compiled into the JAR**. If you need to change them, you must rebuild.

## Project Structure

```
src/main/java/com/ibm/wxd/datalabs/demo/cass_spark_iceberg/
├── LoadEnergyReadings.java      # Data loader
├── CassandraToIceberg.java      # Spark ETL job
├── dto/
│   ├── Asset.java               # Asset data model
│   └── SensorReading.java       # Sensor reading model
└── utils/
    ├── CassUtil.java            # Cassandra utilities
    ├── EnergyDataHelper.java    # Data generation
    └── SparkUtil.java           # Spark utilities
```

---

**For complete instructions, see `../README.md`**
