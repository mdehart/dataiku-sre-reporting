# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
import requests
from datetime import datetime

def get_support_escalations():
    ids, API_KEY = ["P2OE4T3", "PWVQZNH"], "u+xqRscqCG91yXoHxL3g"
    
    params = {
        "escalation_policy_ids[]": ids,
        "statuses[]": ["triggered", "acknowledged", "resolved"],
        "limit": 15,
        "sort_by": "created_at:desc"
    }
    
    res = requests.get("https://api.pagerduty.com/incidents", 
                       headers={"Authorization": f"Token token={API_KEY}", 
                                "Accept": "application/vnd.pagerduty+json;version=2"}, 
                       params=params)

    incidents = res.json().get('incidents', [])
    
    #Force Sort (start), remove as needed 
    incidents.sort(key=lambda x: x['created_at'], reverse=True)
    #Force Sort (end)
    
    print(f"{'#'*30}\n{'LATEST ESCALATIONS':^30}\n{'#'*30}\n")

    for i, inc in enumerate(incidents, 1):
        dt = datetime.strptime(inc['created_at'], "%Y-%m-%dT%H:%M:%SZ").strftime("%b %d, %H:%M")
        print(f"{i}. [{inc['status'].upper()}] #{inc['incident_number']} | {dt}")
        print(f"   Summary: {inc['title'][:70]}...")
        print(f"   Link:    {inc['html_url']}\n" + "-"*50)

get_support_escalations()

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
#test script for support_low_incidents P2OE4T3
import dataiku
import pandas as pd
import requests
from datetime import datetime

# init
API_KEY = "u+xqRscqCG91yXoHxL3g"
POLICY_ID = "P2OE4T3"
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
output_dataset = dataiku.Dataset("support_low_incidents")
output_dataset.write_with_schema(df)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
#test script for support_high_incidents PWVQZNH
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
output_dataset = dataiku.Dataset("support_high_incidents")
output_dataset.write_with_schema(df)

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
# Recipe outputs
support_low_incidents_p2oe4t3 = dataiku.Dataset("support_low_incidents_P2OE4T3")
support_low_incidents_p2oe4t3.write_with_schema(pandas_dataframe)