# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
import dataiku
import pandas as pd
import requests

# init
API_KEY = "u+xqRscqCG91yXoHxL3g"
POLICY_ID = "PWVQZNH"
headers = {
    "Accept": "application/vnd.pagerduty+json;version=2",
    "Authorization": f"Token token={API_KEY}"
}

# params
params = {
    "escalation_policy_ids[]": [POLICY_ID],
    "statuses[]": ["triggered", "acknowledged", "resolved"],
    "limit": 50,
    "sort_by": "created_at:desc"
}

# get call
res = requests.get("https://api.pagerduty.com/incidents", headers=headers, params=params)
incidents = res.json().get('incidents', [])

# table format conversion
rows = []
for inc in incidents:
    rows.append({
        "incident_number": inc.get('incident_number'),
        "status": inc.get('status'),
        "created_at": inc.get('created_at'),
        "title": inc.get('title'),
        "url": inc.get('html_url')
    })

# write 
df = pd.DataFrame(rows)
# output_dataset = dataiku.Dataset("support_high_incidents")
# output_dataset.write_with_schema(df)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Recipe outputs
support_high_incidents_pwvqznh = dataiku.Dataset("support_high_incidents_PWVQZNH")
support_high_incidents_pwvqznh.write_with_schema(pandas_dataframe)