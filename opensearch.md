# OpenSearch for Energy Sector: Real-Time Visibility & Intelligent Search

**From Data Overload to Actionable Insights**

---

## Table of Contents

- [A Day in the Life: The Challenge & How OpenSearch Solves It](#a-day-in-the-life-the-challenge--how-opensearch-solves-it)
- [Why OpenSearch for Energy Operations?](#why-opensearch-for-energy-operations)
- [Part 1: Setting Up OpenSearch](#part-1-setting-up-opensearch)
  - [Option A: watsonx.data managed OpenSearch (recommended)](#option-a-watsonxdata-managed-opensearch-recommended)
  - [Option B: Docker Compose](#option-b-docker-compose)
- [Part 2: Loading Energy Sensor Data](#part-2-loading-energy-sensor-data)
- [Part 3: Building Operational Dashboards](#part-3-building-operational-dashboards)
- [Part 4: Search Queries](#part-4-search-queries)
- [Part 5: Setting Up Intelligent Alerts](#part-5-setting-up-intelligent-alerts)
- [The Complete Picture](#the-complete-picture)
- [Resources](#resources)
- [Appendix: Index Mapping](#appendix-index-mapping)
- [Appendix: Sync Script](#appendix-sync-script)

---

## A Day in the Life: The Challenge & How OpenSearch Solves It

### The Challenge

It's 2:47 AM at PowerGrid Energy's control center. An operator notices a sudden dip in power output from the North Wind Farm cluster. They need answers fast:

- *Which specific turbines are affected?*
- *Is this a weather event or equipment failure?*
- *Are there similar patterns from other facilities?*

With **8,500 sensors** generating **51,000 readings per minute**, the data exists. But finding the needle in this haystack of 73 million daily readings? That's where traditional databases struggle.

### The Solution: OpenSearch in Action

**6:00 AM — The Control Room**

Maria starts her shift. Her OpenSearch dashboard shows everything at a glance:

```
┌─────────────────────────────────────────────────────────────────┐
│  Morning Shift Dashboard                                         │
├─────────────────────┬───────────────────┬───────────────────────┤
│  TOTAL GENERATION   │  FLEET HEALTH     │  ACTIVE ALERTS        │
│     4,247 MW        │     94.2%         │     3 warnings        │
├─────────────────────┴───────────────────┴───────────────────────┤
│  POWER BY REGION                                                │
│  ████████████████████ North: 1,842 MW                           │
│  ██████████████ South: 1,203 MW                                 │
│  ██████████ Central: 847 MW                                     │
└─────────────────────────────────────────────────────────────────┘
```

She clicks a warning indicator for Wind Farm North-7. OpenSearch instantly returns:

> **3 turbines showing elevated vibration** (7.2-7.8 mm/s vs normal 3-4 mm/s)
> - Turbine-N7-023, N7-024, N7-025
>
> **Similar historical pattern found**: December 2023, same turbines—ice accumulation on blades.

Finding patterns across months of data in milliseconds, that's what makes OpenSearch invaluable.

**10:30 AM — In the Field**

Carlos receives an alert on his tablet:

> **Maintenance Alert**: Solar-Facility-East-12, Panel Array B3
> Efficiency dropped 23% over 72 hours
> Probable cause: Soiling (no rain in 8 days)

He searches for similar issues:

```
"efficiency drop" AND region:East AND asset_type:solar_panel AND last_7_days
```

OpenSearch returns 17 similar cases, sorted by severity—now he can plan an optimized route for the maintenance crew.

---

## Why OpenSearch for Energy Operations?

### The Gap in Your Current Architecture

You've built a solid foundation. **Cassandra** handles the firehose of sensor data, 51,000 writes per minute, no problem. **Iceberg** archives years of history for your data scientists to train ML models. **watsonx.data** lets analysts run complex SQL across both.

But here's the thing: *these tools are optimized for storage and analytics, not real-time operations*.

Your control room operators need something different, instant search across millions of records, live dashboards that update every second, and alerts that fire the moment something goes wrong. That's a different kind of workload, and it calls for a purpose-built solution.

**That's where OpenSearch comes in.**

### What OpenSearch Brings

OpenSearch is a **search and analytics engine** purpose-built for real-time operations:

| What You Need | How OpenSearch Delivers |
|---------------|------------------------|
| *"Find all turbine failures in the last hour"* | **Sub-second search** across billions of records |
| *"Show me live power output by region"* | **Real-time dashboards** updating every second |
| *"Which assets are near the incoming storm?"* | **Geo-spatial queries** with interactive maps |
| *"Search maintenance logs for gearbox issues"* | **Full-text search** across all your data |
| *"Alert me before equipment fails"* | **Intelligent alerting** with custom thresholds |
| *"What happened last time we saw this pattern?"* | **Pattern discovery** across historical data |

### The Bottom Line

OpenSearch is built on a **proven open-source foundation** with a thriving community driving continuous innovation. It scales seamlessly from development environments to petabytes in production. Most importantly, it turns your existing data into **actionable intelligence**: catching a failing turbine 30 minutes earlier, dispatching maintenance crews more efficiently, or giving executives instant visibility into fleet performance.

The ROI? One prevented unplanned outage can save hundreds of thousands of dollars. OpenSearch helps you find the signal in the noise before it becomes a problem.

---

### Today's Architecture

#### Can OpenSearch be Added to watsonx.data?

Current State (December 2025) : **Direct integration is not yet available.** watsonx.data does not currently have a native OpenSearch connector.

#### The Good News :  IBM joined the **OpenSearch Software Foundation as a Premier Member** . 

This signals commitment to future integration:

- Native OpenSearch connector in watsonx.data
- Federated queries spanning Iceberg, Cassandra, Other databases and OpenSearch
- Unified data governance across both platforms

Until native integration arrives, OpenSearch runs alongside your existing stack:

```
                    ┌─────────────────────────────────┐
                    │      Sensor Devices (8,500)     │
                    │   Wind • Solar • Substations    │
                    └───────────────┬─────────────────┘
                                    │
                    ┌───────────────▼─────────────────┐
                    │         Cassandra (HCD)          │
                    │    Operational Data (hours)      │
                    │    • 51,000 writes/minute        │
                    │    • Real-time status queries    │
                    └───────────────┬─────────────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
┌─────────────────────┐ ┌─────────────────────┐ ┌─────────────────────┐
│   Iceberg (MinIO)   │ │     OpenSearch      │ │   watsonx.data      │
│                     │ │                     │ │                     │
│ Historical Archive  │ │ Search & Dashboards │ │ Federated Analytics │
│ • Years of data     │ │ • Real-time viz     │ │ • Complex SQL       │
│ • ML training       │ │ • Full-text search  │ │ • Query both DBs    │
│ • Compliance        │ │ • Alerting          │ │ • AI/ML prep        │
└─────────────────────┘ └─────────────────────┘ └─────────────────────┘

         │                        │                      │
         │                        │                      │
         ▼                        ▼                      ▼
    Data Science            Operations Center        Business Analytics
    & ML Models             & Field Teams            & Reporting
```

**Each system has its role:**

| System | Primary Users | Key Value |
|--------|--------------|-----------|
| **Cassandra** | Applications, real-time pipelines | Fastest writes, operational queries |
| **Iceberg** | Data scientists, compliance | Historical depth, ML-ready format |
| **OpenSearch** | Operators, field engineers | Search, dashboards, alerts |
| **watsonx.data** | Analysts, executives | Complex SQL across all sources |

---

## Part 1: Setting Up OpenSearch

You can use **IBM watsonx.data managed OpenSearch** (recommended) or run **OpenSearch with Docker** yourself.

---

### Option A: watsonx.data managed OpenSearch (recommended)

Use **IBM watsonx.data managed OpenSearch**. No local install or Docker required.

1. **Provision OpenSearch** via watsonx.data and note:
   - **OpenSearch API URL** (endpoint and port, e.g. `https://<your-watsonx-opensearch-endpoint>:9200`)
   - **OpenSearch Dashboards URL** (from your watsonx.data / OpenSearch console)
   - **Username** and **password** (if authentication is enabled)

2. **Set environment variables** so the sync and data scripts use your instance:

```bash
export OPENSEARCH_URL="https://<your-watsonx-opensearch-endpoint>:9200"
export OPENSEARCH_USERNAME="your-username"
export OPENSEARCH_PASSWORD="your-password"
```

Use the same variables when running `sync_to_opensearch.py`, `generate_sample_data.py`, and `generate_streaming_data.py`. For **Create the Index** and **Verify** steps in Part 2, use your API URL (and auth) instead of `http://localhost:9200` in `curl` commands.

**Access:** Open your **watsonx.data OpenSearch Dashboards URL** in a browser (no SSH tunnel needed).

---

### Option B: Docker Compose

If you prefer to run OpenSearch yourself (e.g. on EC2 or your laptop), use Docker Compose.

1. **Create the OpenSearch directory:**

```bash
mkdir -p ~/opensearch && cd ~/opensearch
```

2. **Create `docker-compose.yml`** by copying the **Sample Docker Compose file for development** from the official OpenSearch documentation:

   **[OpenSearch Docker Compose for Development](https://docs.opensearch.org/latest/install-and-configure/install-opensearch/docker/#sample-docker-compose-file-for-development)**

   This configuration includes:
   - Two OpenSearch nodes in a cluster
   - OpenSearch Dashboards
   - Security disabled for development simplicity
   - Proper memory and ulimit settings

3. **Set required kernel parameter** (OpenSearch requires this):

```bash
sudo sysctl -w vm.max_map_count=262144

# Make it permanent (survives reboot)
echo "vm.max_map_count=262144" | sudo tee -a /etc/sysctl.conf
```

4. **Start the services:**

```bash
cd ~/opensearch
docker compose up -d

# Wait for startup (30-60 seconds)
sleep 30

# Verify health
curl "http://localhost:9200/_cluster/health?pretty"
```

> **Note**: The sample Docker Compose file disables security for development. For production deployments, enable the security plugin and configure TLS.

**Configure SSH tunnel (when OpenSearch runs on EC2):** Add OpenSearch ports to your SSH tunnel. Open a **new terminal** on your Mac and run:

```bash
ssh -i your-key.pem -N \
  -L 9200:localhost:9200 \
  -L 5601:localhost:5601 \
  ec2-user@your-ec2-public-ip
```

> **Note**: The `-N` flag keeps the tunnel open without starting a shell. Keep this terminal running while you access OpenSearch.

**Access points (Docker):**
- **OpenSearch Dashboards**: http://localhost:5601
- **OpenSearch API**: http://localhost:9200

With Docker, you do **not** need to set `OPENSEARCH_URL`; the scripts default to `localhost:9200`.

---

## Part 2: Loading Energy Sensor Data

### Data Flow

```
┌────────────────┐                        ┌────────────────┐                        ┌────────────────┐
│                │    Python ETL Script   │                │                        │                │
│   Cassandra    │  ────────────────────► │   OpenSearch   │  ────────────────────► │   Dashboards   │
│    (source)    │   sync_to_opensearch   │    (search)    │                        │  (visualize)   │
│                │                        │                │                        │                │
└────────────────┘                        └────────────────┘                        └────────────────┘
```

---

### Step 1: Create the Index

**watsonx.data managed OpenSearch:** Replace the URL with your `OPENSEARCH_URL` and add `-u "$OPENSEARCH_USERNAME:$OPENSEARCH_PASSWORD"` if you use auth.

**Docker:** Use `http://localhost:9200` (with SSH tunnel if OpenSearch is on EC2).

```bash
curl -X PUT "http://localhost:9200/energy-sensor-readings" \
  -H 'Content-Type: application/json' \
  -d @scripts/opensearch_index_mapping.json
```

> **Note**: See [Appendix: Index Mapping](#appendix-index-mapping) for the full schema.

---

### Step 2: Run the Sync Script

**watsonx.data managed OpenSearch:** Set `OPENSEARCH_URL`, `OPENSEARCH_USERNAME`, and `OPENSEARCH_PASSWORD` in your environment (or in a `.env` file), then run the script. No code changes needed.

**Docker:** Ensure OpenSearch is running (and SSH tunnel active if remote). Do **not** set `OPENSEARCH_URL`; the script defaults to `localhost:9200` with no auth.

```bash
# Optional: set env vars for watsonx.data managed OpenSearch (recommended)
# export OPENSEARCH_URL="https://<your-watsonx-opensearch-endpoint>:9200"
# export OPENSEARCH_USERNAME="your-username"
# export OPENSEARCH_PASSWORD="your-password"

pip3 install cassandra-driver opensearch-py && python3 scripts/sync_to_opensearch.py
```

> **Note**: Set `CASSANDRA_HOST` (or `CASSANDRA_HOST` env var) for your Cassandra instance. See [Appendix: Sync Script](#appendix-sync-script) for details.

---

### Step 3: Generate Sample Data (Optional)

If you don't have Cassandra data yet, generate sample data for dashboards. Uses the same OpenSearch connection as the sync script (env vars for managed, or localhost for Docker).

```bash
python3 scripts/generate_sample_data.py
```

---

### Step 4: Verify Document Count

Use your OpenSearch API URL (and auth if managed). Example for Docker:

```bash
curl -s "http://localhost:9200/energy-sensor-readings/_count" | python3 -c "import sys,json; print(f'Documents: {json.load(sys.stdin)[\"count\"]:,}')"
```

---

### Step 5: Open Dashboards

**watsonx.data managed:** Open your watsonx.data OpenSearch Dashboards URL in your browser.  
**Docker:** Navigate to **http://localhost:5601** (with SSH tunnel if OpenSearch is on EC2).

Set time filter to **Last 7 days** to see the data.

---

## Part 3: Building Operational Dashboards

Now the exciting part—turning data into visual insights that drive decisions.

![Dashboards](images/dashboard.png)

### Step 1: Create Index Pattern

Before creating visualizations, tell Dashboards about your data:

1. Click the **Menu** (hamburger icon) in the top left
2. Go to **Management** → **Dashboards Management** → **Index patterns**
3. Click **Create index pattern**
4. Enter `energy-sensor-readings` as the pattern
5. Click **Next step**
6. Select `reading_timestamp` as the time field
7. Click **Create index pattern**

### Step 2: Build Visualizations

> **Important**: Use the **Visualize Library** (not Observability Explorer) to create reusable visualizations that can be saved separately.

1. Click **Menu** → **OpenSearch Dashboards** → **Visualize**
2. Click **Create visualization**
3. Choose your visualization type
4. Select index: `energy-sensor-readings`
5. Configure and **Save with a unique name**

![Building Visualizations](images/visual.gif)

---

#### Visualization 1: Power Generation Trend (Vertical Bar)

1. **Menu** → **Visualize** → **Create visualization**
2. Select **Vertical Bar**
3. Select index: `energy-sensor-readings`
4. Configure:

| Section | Setting |
|---------|---------|
| **Metrics** | Y-axis → Aggregation: `Sum`, Field: `power_output` |
| **Buckets** | X-axis → Aggregation: `Date Histogram`, Field: `reading_timestamp`, Interval: `Daily` |
| **Buckets** | Add → Split Series → Aggregation: `Terms`, Field: `asset_type` |

5. Click **Apply changes**
6. **Save** → Name: `Energy - Power Generation Trend`

---

#### Visualization 2: Fleet Health Overview (Pie Chart)

1. **Menu** → **Visualize** → **Create visualization**
2. Select **Pie**
3. Select index: `energy-sensor-readings`
4. Configure:

| Section | Setting |
|---------|---------|
| **Metrics** | Slice Size → Aggregation: `Count` |
| **Buckets** | Split Slices → Aggregation: `Terms`, Field: `alert_level` |

5. Click **Apply changes**
6. **Save** → Name: `Energy - Fleet Health Overview`

---

#### Visualization 3: Average Temperature by Asset Type (Horizontal Bar)

1. **Menu** → **Visualize** → **Create visualization**
2. Select **Horizontal Bar**
3. Select index: `energy-sensor-readings`
4. Configure:

| Section | Setting |
|---------|---------|
| **Metrics** | Y-axis → Aggregation: `Average`, Field: `temperature` |
| **Buckets** | X-axis → Aggregation: `Terms`, Field: `asset_type` |

5. Click **Apply changes**
6. **Save** → Name: `Energy - Avg Temperature by Asset`

---

#### Visualization 4: Power Output by Facility (Vertical Bar)

1. **Menu** → **Visualize** → **Create visualization**
2. Select **Vertical Bar**
3. Select index: `energy-sensor-readings`
4. Configure:

| Section | Setting |
|---------|---------|
| **Metrics** | Y-axis → Aggregation: `Sum`, Field: `power_output` |
| **Buckets** | X-axis → Aggregation: `Terms`, Field: `facility_name`, Size: `10` |

5. Click **Apply changes**
6. **Save** → Name: `Energy - Power by Facility`

---

#### Visualization 5: Top Assets by Power Output (Horizontal Bar)

1. **Menu** → **Visualize** → **Create visualization**
2. Select **Horizontal Bar**
3. Select index: `energy-sensor-readings`
4. Configure:

| Section | Setting |
|---------|---------|
| **Metrics** | Y-axis → Aggregation: `Sum`, Field: `power_output` |
| **Buckets** | X-axis → Aggregation: `Terms`, Field: `asset_name`, Size: `10` |
| **Buckets** | (same row) Order By: `metric: Sum of power_output`, Order: `Descending` |

5. Click **Apply changes**
6. **Save** → Name: `Energy - Top Assets`

---

#### Visualization 6: Efficiency Distribution (Vertical Bar)

1. **Menu** → **Visualize** → **Create visualization**
2. Select **Vertical Bar**
3. Select index: `energy-sensor-readings`
4. Configure:

| Section | Setting |
|---------|---------|
| **Metrics** | Y-axis → Aggregation: `Count` |
| **Buckets** | X-axis → Aggregation: `Histogram`, Field: `efficiency`, Interval: `5` |

5. Click **Apply changes**
6. **Save** → Name: `Energy - Efficiency Distribution`

---

### Quick Reference: All Visualizations

| # | Name | Type | Metric | Bucket |
|---|------|------|--------|--------|
| 1 | Energy - Power Generation Trend | Vertical Bar | Sum of `power_output` | Date Histogram (Daily) on `reading_timestamp` + Split by `asset_type` |
| 2 | Energy - Fleet Health Overview | Pie | Count | Terms on `alert_level` |
| 3 | Energy - Avg Temperature by Asset | Horizontal Bar | Average of `temperature` | Terms on `asset_type` |
| 4 | Energy - Power by Facility | Vertical Bar | Sum of `power_output` | Terms on `facility_name` (top 10) |
| 5 | Energy - Top Assets | Horizontal Bar | Sum of `power_output` | Terms on `asset_name` (top 10) |
| 6 | Energy - Efficiency Distribution | Vertical Bar | Count | Histogram on `efficiency` (interval 5) |

---

### Step 3: Assemble the Dashboard

1. **Menu** → **OpenSearch Dashboards** → **Dashboard**
2. Click **Create dashboard**
3. Click **Add**
4. Select each visualization you created:
   - Energy - Power Generation Trend
   - Energy - Fleet Health Overview
   - Energy - Avg Temperature by Asset
   - Energy - Power by Facility
   - Energy - Top Assets
   - Energy - Efficiency Distribution
5. Drag and resize panels to arrange the layout
6. Set time filter (top right): **Last 24 hours**
7. Click **Save** → Name: `Energy Operations Control Center`

---

## Part 4: Search Queries

Run these queries in **Dev Tools** (Menu → Management → Dev Tools).

---

### Query 1: Find All Alerts (Warning and Critical)

**What it does**: Returns all readings with warning or critical alert levels from the last 24 hours.

```json
GET energy-sensor-readings/_search
{
  "query": {
    "bool": {
      "must": [
        { "range": { "reading_timestamp": { "gte": "now-24h" } } }
      ],
      "should": [
        { "term": { "alert_level": "critical" } },
        { "term": { "alert_level": "warning" } }
      ],
      "minimum_should_match": 1
    }
  },
  "sort": [{ "reading_timestamp": "desc" }],
  "size": 100
}
```

---

### Query 2: High Temperature Assets

**What it does**: Finds all assets with temperature above 80°C in the last 7 days.

```json
GET energy-sensor-readings/_search
{
  "query": {
    "bool": {
      "must": [
        { "range": { "temperature": { "gte": 80 } } },
        { "range": { "reading_timestamp": { "gte": "now-7d" } } }
      ]
    }
  },
  "sort": [{ "temperature": "desc" }],
  "size": 50
}
```

---

### Query 3: High Vibration Assets

**What it does**: Finds all assets with vibration level above 6 (potential mechanical issues).

```json
GET energy-sensor-readings/_search
{
  "query": {
    "bool": {
      "must": [
        { "range": { "vibration_level": { "gte": 6 } } },
        { "range": { "reading_timestamp": { "gte": "now-7d" } } }
      ]
    }
  },
  "sort": [{ "vibration_level": "desc" }],
  "size": 50
}
```

---

### Query 4: Low Efficiency Assets

**What it does**: Finds all assets with efficiency below 70% (underperforming).

```json
GET energy-sensor-readings/_search
{
  "query": {
    "bool": {
      "must": [
        { "range": { "efficiency": { "lte": 70 } } },
        { "range": { "reading_timestamp": { "gte": "now-7d" } } }
      ]
    }
  },
  "sort": [{ "efficiency": "asc" }],
  "size": 50
}
```

---

### Query 5: Performance by Asset Type

**What it does**: Shows total power output, average efficiency, and average temperature grouped by asset type.

```json
GET energy-sensor-readings/_search
{
  "size": 0,
  "query": {
    "range": { "reading_timestamp": { "gte": "now-7d" } }
  },
  "aggs": {
    "by_asset_type": {
      "terms": { "field": "asset_type" },
      "aggs": {
        "total_power": { "sum": { "field": "power_output" } },
        "avg_efficiency": { "avg": { "field": "efficiency" } },
        "avg_temperature": { "avg": { "field": "temperature" } },
        "reading_count": { "value_count": { "field": "reading_id" } }
      }
    }
  }
}
```

---

### Query 6: Performance by Facility

**What it does**: Shows total power output and average efficiency grouped by facility name.

```json
GET energy-sensor-readings/_search
{
  "size": 0,
  "query": {
    "range": { "reading_timestamp": { "gte": "now-7d" } }
  },
  "aggs": {
    "by_facility": {
      "terms": { "field": "facility_name.keyword", "size": 20 },
      "aggs": {
        "total_power": { "sum": { "field": "power_output" } },
        "avg_efficiency": { "avg": { "field": "efficiency" } },
        "avg_temperature": { "avg": { "field": "temperature" } }
      }
    }
  }
}
```

---

### Query 7: Maintenance Priority List

**What it does**: Finds assets that need maintenance attention - high temperature, high vibration, or low efficiency - grouped by asset name with their worst readings.

```json
GET energy-sensor-readings/_search
{
  "size": 0,
  "query": {
    "bool": {
      "must": [
        { "range": { "reading_timestamp": { "gte": "now-24h" } } }
      ],
      "should": [
        { "range": { "temperature": { "gte": 75 } } },
        { "range": { "vibration_level": { "gte": 6 } } },
        { "range": { "efficiency": { "lte": 70 } } }
      ],
      "minimum_should_match": 1
    }
  },
  "aggs": {
    "problem_assets": {
      "terms": { 
        "field": "asset_name.keyword", 
        "size": 20,
        "order": { "max_temp": "desc" }
      },
      "aggs": {
        "max_temp": { "max": { "field": "temperature" } },
        "max_vibration": { "max": { "field": "vibration_level" } },
        "min_efficiency": { "min": { "field": "efficiency" } },
        "facility": { "terms": { "field": "facility_name.keyword", "size": 1 } }
      }
    }
  }
}
```

---

### Query 8: Daily Power Generation Trend

**What it does**: Shows total power output per day for the last 7 days, grouped by asset type.

```json
GET energy-sensor-readings/_search
{
  "size": 0,
  "query": {
    "range": { "reading_timestamp": { "gte": "now-7d" } }
  },
  "aggs": {
    "daily_power": {
      "date_histogram": {
        "field": "reading_timestamp",
        "calendar_interval": "day"
      },
      "aggs": {
        "total_power": { "sum": { "field": "power_output" } },
        "by_asset_type": {
          "terms": { "field": "asset_type" },
          "aggs": {
            "power": { "sum": { "field": "power_output" } }
          }
        }
      }
    }
  }
}
```

---

### Query Summary Table

| # | Query | What It Finds |
|---|-------|---------------|
| 1 | Find All Alerts | Warning and critical alert readings |
| 2 | High Temperature | Assets with temp > 80°C |
| 3 | High Vibration | Assets with vibration > 6 |
| 4 | Low Efficiency | Assets with efficiency < 70% |
| 5 | By Asset Type | Performance grouped by wind_turbine, solar_panel, etc. |
| 6 | By Facility | Performance grouped by facility name |
| 7 | Maintenance Priority | Assets needing attention, sorted by severity |
| 8 | Daily Trend | Power output trend over time |

---

## Part 5: Setting Up Intelligent Alerts

Don't wait for problems—let OpenSearch notify you proactively.

![Alerts](images/alerting.png)

### Alert 1: High Temperature Warning

1. Go to **Menu** → **OpenSearch Plugins** → **Alerting**
2. Click **Create monitor**

**Step 1: Monitor Details**

| Setting | Value |
|---------|-------|
| Monitor name | `High Equipment Temperature` |
| Monitor type | `Per query monitor` |
| Monitor defining method | `Visual editor` |
| Frequency | `By interval`, Every `1` Minutes |

**Step 2: Data Source**

| Setting | Value |
|---------|-------|
| Index | `energy-sensor-readings` |
| Time field | `reading_timestamp` |

**Step 3: Query (Visual Editor)**

1. Click **Add filter**
2. Configure first filter:
   - Field: `temperature`
   - Operator: `is greater than`
   - Value: `85`
3. Set time range: `Last 5 minutes`

**Step 4: Create Trigger**

1. Click **Add trigger**
2. Configure:

| Setting | Value |
|---------|-------|
| Trigger name | `High Temp Alert` |
| Severity level | `1 (Highest)` |
| Trigger condition | `IS ABOVE 0` |

**Step 5: Add Action (Optional)**

1. Click **Add action**
2. Select destination (Slack, Email, etc.)
3. Message template:

```
HIGH TEMPERATURE ALERT

Assets reporting temperatures above 85°C detected.
Check the Energy Operations Dashboard for details.
```

4. Click **Create**

---

### Alert 2: Low Efficiency Warning

1. Go to **Alerting** → **Create monitor**

**Monitor Settings:**

| Setting | Value |
|---------|-------|
| Monitor name | `Low Efficiency Alert` |
| Monitor type | `Per query monitor` |
| Monitor defining method | `Visual editor` |
| Frequency | Every `5` Minutes |
| Index | `energy-sensor-readings` |
| Time field | `reading_timestamp` |

**Query Filter:**
- Field: `efficiency`
- Operator: `is less than`
- Value: `60`

**Trigger:**
- Trigger condition: `IS ABOVE 0`
- Severity: `2 (High)`

---

### Alert 3: High Vibration Warning

1. Go to **Alerting** → **Create monitor**

**Monitor Settings:**

| Setting | Value |
|---------|-------|
| Monitor name | `High Vibration Alert` |
| Monitor type | `Per query monitor` |
| Monitor defining method | `Visual editor` |
| Frequency | Every `1` Minutes |
| Index | `energy-sensor-readings` |
| Time field | `reading_timestamp` |

**Query Filter:**
- Field: `vibration_level`
- Operator: `is greater than`
- Value: `7`

**Trigger:**
- Trigger condition: `IS ABOVE 0`
- Severity: `1 (Highest)`

---

### Testing Alerts

To test alerts, run the streaming data generator:

```bash
# Install dependencies (if not already installed)
pip3 install opensearch-py

# Run the streaming data generator
python3 scripts/generate_streaming_data.py
```

This script sends new data every 5 seconds with some high temperature readings to trigger alerts.

---

## Resources

**Related Guides:**
- **[Advanced Dashboards Guide](advanced_dashboard.md)** — Controls, maps, metrics panels, dual-axis charts

**External Documentation:**
- **OpenSearch Documentation**: https://opensearch.org/docs/latest/
- **OpenSearch Dashboards Guide**: https://opensearch.org/docs/latest/dashboards/
- **Alerting Plugin**: https://opensearch.org/docs/latest/observing-your-data/alerting/
- **Anomaly Detection**: https://opensearch.org/docs/latest/observing-your-data/ad/
- **OpenSearch Community Forum**: https://forum.opensearch.org/

---

## Appendix: Index Mapping

<details>
<summary><b>Full index schema for energy-sensor-readings</b></summary>

```json
{
  "settings": {
    "number_of_shards": 3,
    "number_of_replicas": 1,
    "index.refresh_interval": "5s"
  },
  "mappings": {
    "properties": {
      "asset_id": { "type": "keyword" },
      "asset_name": { 
        "type": "text",
        "fields": { "keyword": { "type": "keyword" } }
      },
      "asset_type": { "type": "keyword" },
      "facility_id": { "type": "keyword" },
      "facility_name": { 
        "type": "text",
        "fields": { "keyword": { "type": "keyword" } }
      },
      "region": { "type": "keyword" },
      "reading_timestamp": { "type": "date" },
      "reading_id": { "type": "keyword" },
      "power_output": { "type": "float" },
      "voltage": { "type": "float" },
      "current": { "type": "float" },
      "temperature": { "type": "float" },
      "vibration_level": { "type": "float" },
      "frequency": { "type": "float" },
      "power_factor": { "type": "float" },
      "ambient_temperature": { "type": "float" },
      "wind_speed": { "type": "float" },
      "solar_irradiance": { "type": "float" },
      "operational_status": { "type": "keyword" },
      "alert_level": { "type": "keyword" },
      "efficiency": { "type": "float" },
      "capacity_factor": { "type": "float" },
      "location": { "type": "geo_point" }
    }
  }
}
```

**Field types explained:**
- `keyword`: Exact matching for filters (region, asset_type, alert_level)
- `text` + `keyword`: Full-text search + exact aggregations
- `geo_point`: Map visualizations and distance queries
- `float`: Numeric measurements

</details>

---

## Appendix: Sync Script

<details>
<summary><b>OpenSearch connection in sync_to_opensearch.py</b></summary>

The script reads OpenSearch connection from **environment variables** (no hardcoded credentials):

| Variable | Description | Example (watsonx.data) | Docker default |
|----------|-------------|-------------------|----------------|
| `OPENSEARCH_URL` | API endpoint | Your watsonx.data OpenSearch endpoint (e.g. `https://<endpoint>:9200`) | not set → use host/port |
| `OPENSEARCH_USERNAME` | Username (optional) | `admin` | not set |
| `OPENSEARCH_PASSWORD` | Password (optional) | your password | not set |
| `OPENSEARCH_HOST` | Host when URL not set | — | `localhost` |
| `OPENSEARCH_PORT` | Port when URL not set | — | `9200` |

**watsonx.data managed OpenSearch:** Set `OPENSEARCH_URL` and, if your instance uses auth, `OPENSEARCH_USERNAME` and `OPENSEARCH_PASSWORD`. The script uses HTTPS when the URL scheme is `https`.

**Docker:** Leave `OPENSEARCH_URL` unset; the script uses `localhost:9200` (or `OPENSEARCH_HOST` / `OPENSEARCH_PORT` if you set them).

</details>

<details>
<summary><b>Simplified sync flow (conceptual)</b></summary>

The script loads config from the environment, connects to Cassandra and OpenSearch, fetches rows from Cassandra, transforms them into documents, and bulk-indexes into OpenSearch. Full source: `scripts/sync_to_opensearch.py`.

</details>

---

## Next Step

Ready to build advanced dashboards with interactive controls, geographic maps, and dual-axis charts?

**Continue to: [Advanced Dashboards Guide](advanced_dashboard.md)** — Controls, maps, metrics panels, dual-axis charts

---

**Questions?** The combination of watsonx.data's analytical power with OpenSearch's visualization and search capabilities gives your energy operations complete visibility—from real-time monitoring to historical analysis to predictive insights.
