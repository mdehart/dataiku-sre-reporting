import dataiku
import pandas as pd
import requests

# init
API_KEY = "u+xqRscqCG91yXoHxL3g"
POLICY_ID = "PWVQZNH"
url = "https://api.pagerduty.com/incidents"

# params
params = {
    "escalation_policy_ids[]": [POLICY_ID],
    "statuses[]": ["triggered", "acknowledged", "resolved"],
    "limit": 50,
    "sort_by": "created_at:desc"
}

# auth
headers = {
    "Accept": "application/vnd.pagerduty+json;version=2",
    "Authorization": f"Token token={API_KEY}"
}

res = requests.get(url, headers=headers, params=params).json()

# format into df
df = pd.DataFrame([{
    "incident_number": i.get('incident_number'),
    "status": i.get('status'),
    "created_at": i.get('created_at'),
    "title": i.get('title'),
    "url": i.get('html_url')
} for i in res.get('incidents', [])])

# output
dataiku.Dataset("support_high_incidents_PWVQZNH").write_with_schema(df)