# Advanced OpenSearch Dashboards for Energy Sector

**Interactive Controls, Complex Visualizations & Real-Time Monitoring**

---

## Overview

This guide covers advanced dashboard techniques for energy sector operations, building on your `energy-sensor-readings` index. You'll learn to create:

- **Interactive Controls** — Filter data with dropdowns and sliders
- **Metric Panels** — Display KPIs with large, prominent numbers
- **Dual-Axis Charts** — Overlay multiple metrics on one visualization
- **Percentage Calculations** — Show delay rates, efficiency percentages
- **Stacked Visualizations** — Break down data by categories over time
- **Markdown Panels** — Add context and instructions to dashboards
- **Maps & Geo Visualizations** — Plot assets on interactive maps with heatmaps

---

## Prerequisites

Before building advanced dashboards, ensure you have:

1. **OpenSearch running** with the `energy-sensor-readings` index
2. **Index pattern created** for `energy-sensor-readings` with `reading_timestamp` as time field
3. **Sample data loaded** (run `python3 scripts/generate_sample_data.py`)

---

## Part 1: Dashboard Controls

Controls let users filter dashboard data interactively—just like the filter controls shown in modern analytics dashboards.

### Create Controls Panel

1. **Menu** → **Visualize** → **Create visualization**
2. Select **Controls**
3. Configure control elements:

#### Control 1: Region Dropdown

| Setting | Value |
|---------|-------|
| Control Type | `Options list` |
| Control Label | `Region` |
| Index Pattern | `energy-sensor-readings` |
| Field | `region` |
| Parent Control | (none) |
| Multiselect | ✓ Enabled |

Click **Add** to add another control.

#### Control 2: Asset Type Dropdown

| Setting | Value |
|---------|-------|
| Control Type | `Options list` |
| Control Label | `Asset Type` |
| Index Pattern | `energy-sensor-readings` |
| Field | `asset_type` |
| Parent Control | (none) |
| Multiselect | ✓ Enabled |

Click **Add** to add another control.

#### Control 3: Facility Dropdown

| Setting | Value |
|---------|-------|
| Control Type | `Options list` |
| Control Label | `Facility` |
| Index Pattern | `energy-sensor-readings` |
| Field | `facility_name.keyword` |
| Parent Control | (none) |
| Multiselect | ✓ Enabled |

Click **Add** to add another control.

#### Control 4: Temperature Range Slider

| Setting | Value |
|---------|-------|
| Control Type | `Range slider` |
| Control Label | `Temperature (°C)` |
| Index Pattern | `energy-sensor-readings` |
| Field | `temperature` |
| Parent Control | (none) |
| Size | `5` |

> **Note**: The Range Slider automatically detects min/max values from your data. The slider will show the full range of temperature values in your index.

4. Click **Apply changes**
5. **Save** → Name: `Energy - Controls Panel`

### Using Controls in Dashboard

When added to a dashboard, controls appear at the top. Users can:
- Select one or multiple regions
- Filter by asset type (wind_turbine, solar_panel, etc.)
- Choose specific facilities
- Drag the temperature slider to filter by range

All other visualizations on the dashboard automatically filter based on these selections.

---

## Part 2: Metric Visualizations (KPI Panels)

Large metric displays for key performance indicators.

### Metric 1: Total Power Generation

1. **Menu** → **Visualize** → **Create visualization**
2. Select **Metric**
3. Select index: `energy-sensor-readings`
4. Configure:

| Section | Setting |
|---------|---------|
| **Metrics** | Aggregation: `Sum`, Field: `power_output` |
| **Options** | Font Size: `60pt` |

5. **Save** → Name: `Energy - Total Power Generation`

---

### Metric 2: Average Efficiency

1. Create new **Metric** visualization
2. Configure:

| Section | Setting |
|---------|---------|
| **Metrics** | Aggregation: `Average`, Field: `efficiency` |
| **Options** | Font Size: `60pt` |

3. **Save** → Name: `Energy - Average Efficiency`

---

### Metric 3: Total Asset Count

1. Create new **Metric** visualization
2. Configure:

| Section | Setting |
|---------|---------|
| **Metrics** | Aggregation: `Unique Count`, Field: `asset_id` |
| **Options** | Font Size: `60pt` |

3. **Save** → Name: `Energy - Total Assets`

---

### Metric 4: Critical Alerts Count

1. Create new **Metric** visualization
2. Configure:

| Section | Setting |
|---------|---------|
| **Metrics** | Aggregation: `Count` |
| **Buckets** | (none - we'll use filter) |

3. Click the **+ Add filter** link in the query bar
4. Add filter: `alert_level` is `critical`
5. **Save** → Name: `Energy - Critical Alerts`

---

### Metric 5: Warning Alerts Count

1. Create new **Metric** visualization
2. Add filter: `alert_level` is `warning`
3. **Save** → Name: `Energy - Warning Alerts`

---

## Part 3: Dual-Axis Charts (Combined Metrics)

Show power output trend with efficiency overlay—two metrics on one chart.

### Power Output & Efficiency Trend

1. **Menu** → **Visualize** → **Create visualization**
2. Select **Area**
3. Select index: `energy-sensor-readings`

**Step A: Configure Data Tab**

| Section | Setting |
|---------|---------|
| **Metrics** | Y-axis 1: Aggregation: `Sum`, Field: `power_output`, Custom Label: `Power Output (MW)` |
| **Metrics** | Add Y-axis → Aggregation: `Average`, Field: `efficiency`, Custom Label: `Avg Efficiency (%)` |
| **Buckets** | X-axis: Aggregation: `Date Histogram`, Field: `reading_timestamp`, Interval: `Hourly` |

**Step B: Configure Metrics & Axes Tab**

4. Click the **Metrics & Axes** tab (next to "Data" tab)

5. In the **Y-axes** section, click to expand the axis settings:

   | Setting | Value for Power Output |
   |---------|------------------------|
   | Position | `Left` |
   | Mode | `Normal` |
   | Scale type | `Linear` |
   | Title | `Power Output (MW)` |

6. Click the **+** button in Y-axes to add a second axis, configure:

   | Setting | Value for Efficiency |
   |---------|---------------------|
   | Position | `Right` |
   | Mode | `Normal` |
   | Scale type | `Linear` |
   | Title | `Avg Efficiency (%)` |

7. For the efficiency metric, change **Line mode** to `Straight` (at the top of Metrics & Axes tab)

8. Click **▶ Apply changes** to preview

9. **Save** → Name: `Energy - Power & Efficiency Trend`

> **Result**: You'll see an area chart for Power Output with a line overlay for Efficiency, each with its own Y-axis scale.

---

### Temperature & Vibration Monitoring

1. Create new **Area** visualization
2. Configure:

| Section | Setting |
|---------|---------|
| **Metrics** | Y-axis 1: `Average` of `temperature`, Custom Label: `Avg Temperature (°C)` |
| **Metrics** | Y-axis 2: `Average` of `vibration_level`, Custom Label: `Avg Vibration` |
| **Buckets** | X-axis: `Date Histogram` on `reading_timestamp`, Interval: `Hourly` |

3. Set Temperature to Left axis, Vibration to Right axis
4. Change Vibration to Line chart type
5. **Save** → Name: `Energy - Temperature & Vibration Trend`

---

## Part 4: Alert Distribution & Percentages

### Alert Level Distribution (Donut Chart)

1. **Menu** → **Visualize** → **Create visualization**
2. Select **Pie**
3. Select index: `energy-sensor-readings`
4. Configure:

| Section | Setting |
|---------|---------|
| **Metrics** | Slice Size: `Count` |
| **Buckets** | Split Slices: `Terms`, Field: `alert_level`, Order by: `Count`, Size: `5` |

5. Go to **Options** tab:
   - Check **Donut** to create ring chart
   - Check **Show Labels**

6. **Save** → Name: `Energy - Alert Distribution`

---

### Operational Status Breakdown

1. Create new **Pie** visualization (Donut)
2. Configure:

| Section | Setting |
|---------|---------|
| **Metrics** | Slice Size: `Count` |
| **Buckets** | Split Slices: `Terms`, Field: `operational_status` |

3. Enable Donut mode
4. **Save** → Name: `Energy - Operational Status`

---

### Alert Percentage Over Time

Shows what percentage of readings are alerts vs normal over time.

1. **Menu** → **Visualize** → **Create visualization**
2. Select **Area**
3. Select index: `energy-sensor-readings`
4. Configure:

| Section | Setting |
|---------|---------|
| **Metrics** | Y-axis: `Count` |
| **Buckets** | X-axis: `Date Histogram` on `reading_timestamp`, Interval: `Daily` |
| **Buckets** | Add → Split Series: `Terms`, Field: `alert_level` |

5. Go to **Metrics & Axes** tab:
   - Mode: `Stacked`
   - Scale: `Percentage` (shows as 100% stacked)

6. **Save** → Name: `Energy - Alert Percentage Trend`

---

## Part 5: Stacked Bar Charts

### Power Output by Asset Type (Stacked)

1. **Menu** → **Visualize** → **Create visualization**
2. Select **Vertical Bar**
3. Configure:

| Section | Setting |
|---------|---------|
| **Metrics** | Y-axis: `Sum`, Field: `power_output` |
| **Buckets** | X-axis: `Date Histogram` on `reading_timestamp`, Interval: `Daily` |
| **Buckets** | Add → Split Series: `Terms`, Field: `asset_type` |

4. Go to **Metrics & Axes** tab:
   - Mode: `Stacked`

5. **Save** → Name: `Energy - Power by Asset Type (Stacked)`

---

### Efficiency Buckets Distribution

Shows distribution of efficiency values across different ranges.

1. Create new **Vertical Bar** visualization
2. Configure:

| Section | Setting |
|---------|---------|
| **Metrics** | Y-axis: `Count` |
| **Buckets** | X-axis: `Range`, Field: `efficiency` |

3. Define ranges:
   - 0 - 50 (Poor)
   - 50 - 70 (Below Average)
   - 70 - 85 (Good)
   - 85 - 95 (Excellent)
   - 95 - 100 (Optimal)

4. **Save** → Name: `Energy - Efficiency Buckets`

---

### Temperature Buckets by Alert Level

1. Create new **Vertical Bar** visualization
2. Configure:

| Section | Setting |
|---------|---------|
| **Metrics** | Y-axis: `Count` |
| **Buckets** | X-axis: `Histogram`, Field: `temperature`, Interval: `10` |
| **Buckets** | Split Series: `Terms`, Field: `alert_level` |

3. Set mode to `Stacked`
4. **Save** → Name: `Energy - Temperature by Alert Level`

---

## Part 6: Horizontal Bar Charts

### Top 10 Facilities by Power Output

1. **Menu** → **Visualize** → **Create visualization**
2. Select **Horizontal Bar**
3. Configure:

| Section | Setting |
|---------|---------|
| **Metrics** | Y-axis: `Sum`, Field: `power_output` |
| **Buckets** | X-axis: `Terms`, Field: `facility_name.keyword`, Size: `10`, Order: `Descending` |

4. **Save** → Name: `Energy - Top Facilities`

---

### Assets with Highest Vibration

1. Create new **Horizontal Bar** visualization
2. Configure:

| Section | Setting |
|---------|---------|
| **Metrics** | Y-axis: `Max`, Field: `vibration_level` |
| **Buckets** | X-axis: `Terms`, Field: `asset_name.keyword`, Size: `10`, Order: `Descending` |

3. Add filter: `vibration_level` is greater than `5`
4. **Save** → Name: `Energy - High Vibration Assets`

---

### Alert Count by Facility (True/False Style)

Shows which facilities have alerts vs no alerts.

1. Create new **Horizontal Bar** visualization
2. Configure:

| Section | Setting |
|---------|---------|
| **Metrics** | Y-axis: `Count` |
| **Buckets** | X-axis: `Terms`, Field: `alert_level`, Size: `3` |

3. **Save** → Name: `Energy - Alerts True/False`

---

## Part 7: Data Tables

### Detailed Asset Performance Table

1. **Menu** → **Visualize** → **Create visualization**
2. Select **Data Table**
3. Configure:

| Section | Setting |
|---------|---------|
| **Metrics** | Add metrics: |
|  | - `Sum` of `power_output` (label: Total Power) |
|  | - `Average` of `efficiency` (label: Avg Efficiency) |
|  | - `Average` of `temperature` (label: Avg Temp) |
|  | - `Max` of `vibration_level` (label: Max Vibration) |
|  | - `Count` (label: Readings) |
| **Buckets** | Split Rows: `Terms`, Field: `asset_name.keyword`, Size: `20` |

4. **Save** → Name: `Energy - Asset Performance Table`

---

### Maintenance Priority Table

1. Create new **Data Table** visualization
2. Add filter:
   ```
   (temperature > 80) OR (vibration_level > 6) OR (efficiency < 60)
   ```
3. Configure:

| Section | Setting |
|---------|---------|
| **Metrics** | `Max` of `temperature`, `Max` of `vibration_level`, `Min` of `efficiency`, `Count` |
| **Buckets** | Split Rows: `Terms`, Field: `asset_name.keyword`, Size: `15` |
| **Buckets** | Add Sub-Row: `Terms`, Field: `facility_name.keyword`, Size: `1` |

4. **Save** → Name: `Energy - Maintenance Priority List`

---

## Part 8: Markdown Panels

Add context, instructions, and documentation directly in dashboards.

### Create Markdown Panel

1. **Menu** → **Visualize** → **Create visualization**
2. Select **Markdown**
3. Enter markdown content:

```markdown
## Energy Sector Monitoring Dashboard

This dashboard provides real-time visibility into your energy infrastructure.

### How to Use This Dashboard

1. **Select Filters** - Use the controls at the top to filter by region, asset type, or facility
2. **Time Range** - Adjust the time picker (top right) to view different periods
3. **Drill Down** - Click any chart element to filter the entire dashboard

### Alert Levels

| Level | Description | Action Required |
|-------|-------------|-----------------|
| 🟢 Normal | All systems operating within parameters | None |
| 🟡 Warning | Metrics approaching thresholds | Monitor closely |
| 🔴 Critical | Immediate attention required | Dispatch team |

### Key Metrics

- **Power Output** - Total MW generated across all assets
- **Efficiency** - Percentage of optimal performance
- **Temperature** - Equipment operating temperature
- **Vibration** - Mechanical vibration levels (high = potential failure)

For more information, check our [OpenSearch Documentation](../OPENSEARCH_DASHBOARDS.md).
```

4. **Save** → Name: `Energy - Dashboard Instructions`

---

### Quick Stats Panel

```markdown
## Quick Reference

### Temperature Thresholds
- **Normal**: < 70°C
- **Elevated**: 70-85°C
- **Critical**: > 85°C

### Vibration Levels
- **Normal**: < 4 mm/s
- **Warning**: 4-7 mm/s
- **Critical**: > 7 mm/s

### Efficiency Targets
- **Optimal**: > 90%
- **Acceptable**: 70-90%
- **Poor**: < 70%
```

Save as: `Energy - Quick Stats Reference`

---

## Part 9: Maps Visualization

Visualize your energy assets geographically using the `location` geo_point field.

### Prerequisites for Maps

Ensure your index has geo_point data:

```json
// Check if location field has data
GET energy-sensor-readings/_search
{
  "size": 5,
  "query": {
    "exists": { "field": "location" }
  },
  "_source": ["asset_name", "location", "facility_name", "region"]
}
```

If location data is missing, the sample data generator creates coordinates for each facility.

---

### Map 1: Asset Location Map (Coordinate Map)

Shows all energy assets on an interactive map with clustering.

1. **Menu** → **Visualize** → **Create visualization**
2. Select **Coordinate Map**
3. Select index: `energy-sensor-readings`
4. Configure:

| Section | Setting |
|---------|---------|
| **Metrics** | Value: `Count` |
| **Buckets** | Geo Coordinates: Aggregation: `Geohash`, Field: `location`, Precision: `5` |

5. Go to **Options** tab:

| Setting | Value |
|---------|-------|
| Map type | `Scaled Circle Markers` |
| Show Tooltip | ✓ Enabled |

6. **Save** → Name: `Energy - Asset Locations Map`

---

### Map 2: Power Output by Region (Choropleth-Style)

Heat map showing power generation intensity by location.

1. **Menu** → **Visualize** → **Create visualization**
2. Select **Coordinate Map**
3. Select index: `energy-sensor-readings`
4. Configure:

| Section | Setting |
|---------|---------|
| **Metrics** | Value: Aggregation: `Sum`, Field: `power_output` |
| **Buckets** | Geo Coordinates: Aggregation: `Geohash`, Field: `location`, Precision: `4` |

5. Go to **Options** tab:

| Setting | Value |
|---------|-------|
| Map type | `Heatmap` |
| Show Tooltip | ✓ Enabled |
| Heatmap Intensity | `0.5` (adjust as needed) |

6. **Save** → Name: `Energy - Power Output Heatmap`

---

### Map 3: Alert Locations Map

Highlight assets with active alerts on the map.

1. **Menu** → **Visualize** → **Create visualization**
2. Select **Coordinate Map**
3. Select index: `energy-sensor-readings`
4. **Add filter** in query bar:
   - `alert_level` is `warning` OR `alert_level` is `critical`

5. Configure:

| Section | Setting |
|---------|---------|
| **Metrics** | Value: `Count` |
| **Buckets** | Geo Coordinates: Aggregation: `Geohash`, Field: `location`, Precision: `6` |

6. Go to **Options** tab:

| Setting | Value |
|---------|-------|
| Map type | `Scaled Circle Markers` |
| Color | Red or Orange |
| Show Tooltip | ✓ Enabled |

7. **Save** → Name: `Energy - Alert Locations`

---

### Map 4: Temperature Distribution Map

Visualize equipment temperature across geographic locations.

1. Create new **Coordinate Map** visualization
2. Configure:

| Section | Setting |
|---------|---------|
| **Metrics** | Value: Aggregation: `Average`, Field: `temperature` |
| **Buckets** | Geo Coordinates: Aggregation: `Geohash`, Field: `location`, Precision: `5` |

3. Options:
   - Map type: `Heatmap`
   - Color range: Blue (cool) to Red (hot)

4. **Save** → Name: `Energy - Temperature Distribution Map`

---

### Map 5: Efficiency by Location

Shows average efficiency across facilities geographically.

1. Create new **Coordinate Map** visualization
2. Configure:

| Section | Setting |
|---------|---------|
| **Metrics** | Value: Aggregation: `Average`, Field: `efficiency` |
| **Buckets** | Geo Coordinates: Aggregation: `Geohash`, Field: `location`, Precision: `5` |

3. Options:
   - Map type: `Scaled Circle Markers`
   - Size reflects efficiency value

4. **Save** → Name: `Energy - Efficiency by Location`

---

### Using Maps Plugin (Advanced)

For more advanced mapping, use the **Maps Plugin**:

1. **Menu** → **OpenSearch Plugins** → **Maps**
2. Click **Create map**

#### Add Document Layer

1. Click **Add layer** → **Documents**
2. Configure:

| Setting | Value |
|---------|-------|
| Data source | `energy-sensor-readings` |
| Geo field | `location` |
| Style by | `alert_level` (categorical) |

3. Set colors:
   - `normal` → Green
   - `warning` → Yellow
   - `critical` → Red

#### Add Cluster Layer

For dense data, use clustering:

1. Click **Add layer** → **Cluster**
2. Configure:

| Setting | Value |
|---------|-------|
| Data source | `energy-sensor-readings` |
| Geo field | `location` |
| Cluster by | `Count` or `Sum of power_output` |

---

### Map Tooltips Configuration

Enhance map tooltips to show relevant asset information:

When creating coordinate maps, the tooltip automatically shows the metric value. For richer tooltips:

1. In visualization settings, enable **Show Tooltip**
2. The tooltip will display:
   - Metric value (count, sum, average)
   - Geohash bucket location
   - Number of documents in cluster

For detailed asset information, use the Maps Plugin which supports custom tooltips.

---

### Sample Facility Coordinates

The sample data generator uses these approximate coordinates for facilities:

| Facility | Region | Latitude | Longitude |
|----------|--------|----------|-----------|
| Wind Farm North-1 | North | 41.8781 | -87.6298 |
| Wind Farm North-2 | North | 42.3601 | -71.0589 |
| Solar Farm East-1 | East | 40.7128 | -74.0060 |
| Solar Farm East-2 | East | 39.9526 | -75.1652 |
| Substation Central-1 | Central | 39.7392 | -104.9903 |
| Substation Central-2 | Central | 38.6270 | -90.1994 |
| Wind Farm South-1 | South | 29.7604 | -95.3698 |
| Wind Farm South-2 | South | 33.4484 | -112.0740 |
| Solar Farm West-1 | West | 34.0522 | -118.2437 |
| Transmission Hub-1 | Central | 41.2565 | -95.9345 |

---

### Maps Quick Reference

| # | Visualization Name | Type | What It Shows |
|---|-------------------|------|---------------|
| 1 | Energy - Asset Locations Map | Coordinate Map | All assets clustered by location |
| 2 | Energy - Power Output Heatmap | Heatmap | Power generation intensity |
| 3 | Energy - Alert Locations | Coordinate Map | Warning/critical alert locations |
| 4 | Energy - Temperature Distribution Map | Heatmap | Equipment temperature by area |
| 5 | Energy - Efficiency by Location | Coordinate Map | Efficiency performance by location |

---

## Part 10: Complete Advanced Dashboard Assembly

### Energy Operations Control Center (Advanced)

Create a comprehensive dashboard with all advanced visualizations:

1. **Menu** → **Dashboard** → **Create dashboard**
2. Click **Add** and add panels in this order:

**Row 1 - Controls & Instructions:**
| Panel | Width |
|-------|-------|
| Energy - Controls Panel | 8/12 |
| Energy - Dashboard Instructions | 4/12 |

**Row 2 - Key Metrics:**
| Panel | Width |
|-------|-------|
| Energy - Total Power Generation | 2/12 |
| Energy - Average Efficiency | 2/12 |
| Energy - Total Assets | 2/12 |
| Energy - Critical Alerts | 3/12 |
| Energy - Warning Alerts | 3/12 |

**Row 3 - Trend Analysis:**
| Panel | Width |
|-------|-------|
| Energy - Power & Efficiency Trend | 8/12 |
| Energy - Alert Distribution | 4/12 |

**Row 4 - Status Breakdown:**
| Panel | Width |
|-------|-------|
| Energy - Operational Status | 4/12 |
| Energy - Alert Percentage Trend | 8/12 |

**Row 5 - Detailed Analysis:**
| Panel | Width |
|-------|-------|
| Energy - Power by Asset Type (Stacked) | 6/12 |
| Energy - Temperature by Alert Level | 6/12 |

**Row 6 - Rankings:**
| Panel | Width |
|-------|-------|
| Energy - Top Facilities | 4/12 |
| Energy - High Vibration Assets | 4/12 |
| Energy - Efficiency Buckets | 4/12 |

**Row 7 - Tables:**
| Panel | Width |
|-------|-------|
| Energy - Asset Performance Table | 6/12 |
| Energy - Maintenance Priority List | 6/12 |

**Row 8 - Geographic View:**
| Panel | Width |
|-------|-------|
| Energy - Asset Locations Map | 6/12 |
| Energy - Alert Locations | 6/12 |

3. Set time filter: **Last 7 days**
4. **Save** → Name: `Energy Operations Control Center (Advanced)`

---

## Part 11: Dashboard Interactions

### Click-to-Filter

When users click on chart elements:
- Click a pie slice → filters entire dashboard to that value
- Click a bar → filters to that category
- Click a time period → zooms to that time range

### Drill-Down Configuration

To enable drill-down on a visualization:

1. Edit the visualization
2. Go to **Options** panel
3. Enable **Click on legend**
4. Set action to **Filter**

### Time Comparison

Compare current period vs previous:

1. In date histogram visualizations, add a **Filter Ratio** metric
2. Configure:
   - Numerator: Current query
   - Denominator: Previous period (shift by time range)

---

## Part 12: Performance Optimization

### Dashboard Load Time

For large datasets, optimize:

1. **Reduce bucket sizes** - Use `Size: 10` instead of `Size: 100`
2. **Use date math** - Limit time ranges (`now-7d` instead of all time)
3. **Avoid expensive aggregations** - Cardinality on high-cardinality fields is slow
4. **Pre-aggregate in index** - Create rollup indices for historical data

### Refresh Intervals

Set appropriate auto-refresh:

| Dashboard Type | Refresh Interval |
|----------------|------------------|
| Real-time Ops | 10-30 seconds |
| Shift Overview | 1-5 minutes |
| Daily Summary | 15-60 minutes |
| Historical | Manual only |

Configure: Click time picker → **Auto-refresh** → Select interval

---

## Quick Reference: All Advanced Visualizations

| # | Visualization Name | Type | Key Feature |
|---|-------------------|------|-------------|
| 1 | Energy - Controls Panel | Controls | Interactive filtering |
| 2 | Energy - Total Power Generation | Metric | Large KPI display |
| 3 | Energy - Average Efficiency | Metric | Large KPI display |
| 4 | Energy - Total Assets | Metric | Unique count |
| 5 | Energy - Critical Alerts | Metric | Filtered count |
| 6 | Energy - Warning Alerts | Metric | Filtered count |
| 7 | Energy - Power & Efficiency Trend | Area/Line | Dual-axis chart |
| 8 | Energy - Temperature & Vibration Trend | Area/Line | Dual-axis chart |
| 9 | Energy - Alert Distribution | Pie (Donut) | Ring chart |
| 10 | Energy - Operational Status | Pie (Donut) | Ring chart |
| 11 | Energy - Alert Percentage Trend | Area | 100% stacked |
| 12 | Energy - Power by Asset Type (Stacked) | Vertical Bar | Stacked categories |
| 13 | Energy - Efficiency Buckets | Vertical Bar | Range buckets |
| 14 | Energy - Temperature by Alert Level | Vertical Bar | Stacked by alert |
| 15 | Energy - Top Facilities | Horizontal Bar | Top N ranking |
| 16 | Energy - High Vibration Assets | Horizontal Bar | Filtered top N |
| 17 | Energy - Alerts True/False | Horizontal Bar | Boolean-style |
| 18 | Energy - Asset Performance Table | Data Table | Multi-metric |
| 19 | Energy - Maintenance Priority List | Data Table | Filtered + nested |
| 20 | Energy - Dashboard Instructions | Markdown | Help text |
| 21 | Energy - Quick Stats Reference | Markdown | Reference guide |
| 22 | Energy - Asset Locations Map | Coordinate Map | All assets on map |
| 23 | Energy - Power Output Heatmap | Heatmap | Power intensity by location |
| 24 | Energy - Alert Locations | Coordinate Map | Warning/critical alerts on map |
| 25 | Energy - Temperature Distribution Map | Heatmap | Temperature by geographic area |
| 26 | Energy - Efficiency by Location | Coordinate Map | Efficiency performance on map |

---

## Sample Dashboard Layout

```
┌─────────────────────────────────────────────────────────────────────────────┐
│  [Region ▼] [Asset Type ▼] [Facility ▼]    Temperature: [====●========]    │
│  [Apply changes]  [Cancel]  [Clear]                                         │
├──────────────────────────────────────────────────┬──────────────────────────┤
│                                                  │ ## Energy Monitoring     │
│                                                  │                          │
│                                                  │ Use controls to filter   │
│                                                  │ Click charts to drill    │
├──────────┬──────────┬──────────┬─────────┬──────┴──────────────────────────┤
│          │          │          │         │                                  │
│ 847 MW   │  89.3%   │   127    │   3     │              12                  │
│ Total    │ Avg Eff  │ Assets   │Critical │           Warnings               │
│ Power    │          │          │ Alerts  │                                  │
├──────────┴──────────┴──────────┴─────────┴──────────────────────────────────┤
│                                                        ┌───────────────────┐│
│  ████                                                  │    ◉ Normal 78%   ││
│  ██████████                    ───efficiency───        │    ◉ Warning 15%  ││
│  █████████████████       ──────────────────────        │    ◉ Critical 7%  ││
│  ██████████████████████████                            └───────────────────┘│
│  Power Output & Efficiency Over Time                    Alert Distribution  │
├─────────────────────────────────────────┬───────────────────────────────────┤
│    ┌─────────────┐                      │ 100%|████████████████████████████ │
│    │  Running    │                      │  80%|████████████████████████████ │
│    │    82%      │                      │  60%|████████████████████████████ │
│    │             │                      │  40%|████████████████████████████ │
│    │  Offline 8% │                      │  20%|████████████████████████████ │
│    │  Maint 10%  │                      │   0%|████████████████████████████ │
│    └─────────────┘                      │      Mon Tue Wed Thu Fri Sat Sun  │
│    Operational Status                   │      Alert Percentage Over Time   │
├─────────────────────────────────────────┴───────────────────────────────────┤
│                                                                              │
│  Asset        │ Total Power │ Avg Eff │ Avg Temp │ Max Vib │ Readings      │
│  ─────────────┼─────────────┼─────────┼──────────┼─────────┼───────────    │
│  Turbine-N7   │   124.5 MW  │  91.2%  │   45°C   │   3.2   │    847        │
│  Turbine-N8   │   118.3 MW  │  88.7%  │   48°C   │   4.1   │    832        │
│  Solar-E12    │    87.2 MW  │  94.1%  │   52°C   │   1.2   │    921        │
│                                                                              │
├─────────────────────────────────────────┬───────────────────────────────────┤
│                                         │                                    │
│     ┌────────────────────────────┐      │     ┌────────────────────────┐    │
│     │  🗺️  Asset Locations       │      │     │  🗺️  Alert Locations   │    │
│     │                            │      │     │                        │    │
│     │    ●  ●     ●              │      │     │         🔴             │    │
│     │       ●  ●                 │      │     │    🟡      🔴          │    │
│     │  ●        ●    ●           │      │     │       🟡               │    │
│     │     ●  ●     ●             │      │     │                        │    │
│     └────────────────────────────┘      │     └────────────────────────┘    │
│                                         │                                    │
└─────────────────────────────────────────┴────────────────────────────────────┘
```

---

## Next Steps

1. **Create the visualizations** following the instructions above
2. **Assemble the dashboard** using the layout guide
3. **Set up alerts** (see [OpenSearch Dashboards Guide](OPENSEARCH_DASHBOARDS.md#part-5-setting-up-intelligent-alerts))
4. **Enable auto-refresh** for real-time monitoring
5. **Share with team** using Dashboard → Share menu

---

## Resources

- [OpenSearch Dashboards Documentation](https://opensearch.org/docs/latest/dashboards/)
- [Visualization Types Reference](https://opensearch.org/docs/latest/dashboards/visualize/viz-index/)
- [Dashboard Controls](https://opensearch.org/docs/latest/dashboards/visualize/controls/)
- [Main Energy Sector OpenSearch Guide](OPENSEARCH_DASHBOARDS.md)

