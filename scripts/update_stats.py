import json
import os

from google.analytics.data_v1beta import BetaAnalyticsDataClient
from google.analytics.data_v1beta.types import (
    RunReportRequest,
    DateRange,
    Dimension,
    Metric,
)

PROPERTY_ID = "543461935"

client = BetaAnalyticsDataClient()

# Total views in last 30 days
request = RunReportRequest(
    property=f"properties/{PROPERTY_ID}",
    dimensions=[Dimension(name="date")],
    metrics=[Metric(name="screenPageViews")],
    date_ranges=[DateRange(start_date="2026-06-25", end_date="today")],
)

response = client.run_report(request)

views = 0

for row in response.rows:
    views += int(row.metric_values[0].value)

request = RunReportRequest(
    property=f"properties/{PROPERTY_ID}",
    dimensions=[Dimension(name="country")],
    metrics=[Metric(name="screenPageViews")],
    date_ranges=[DateRange(start_date="2026-06-25", end_date="today")],
)

response = client.run_report(request)
topCountry = response.rows[0].dimension_values[0].value


stats = {
    "views": views,
    "topCountry" : topCountry
}

path = "api/stats.json"

if os.path.exists(path):
    with open(path, "r") as f:
        old_stats = json.load(f)

    if old_stats == stats:
        print("Statistics unchanged.")
        exit(0)

with open(path, "w") as f:
    json.dump(stats, f, indent=2)

print(stats)