# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
import dataiku

client = dataiku.api_client()

# Set the path you want to audit
TARGET_PATH = "/Sandbox" 

print(f"--- Auditing all projects under: {TARGET_PATH} ---\n")

projects = client.list_projects()
found_any = False

for p_summary in projects:
    project = client.get_project(p_summary['projectKey'])
    
    # Get the folder location of the project
    metadata = project.get_metadata()
    folder_path = metadata.get('folder', '/')
    
    # Check if the project's folder matches or is a sub-folder of TARGET_PATH
    if folder_path.startswith(TARGET_PATH):
        found_any = True
        perms = project.get_permissions()
        
        # Get groups with explicit access
        groups = [p['group'] for p in perms.get('permissions', [])]
        
        print(f"PROJECT: {p_summary['name']} ({p_summary['projectKey']})")
        print(f"  - Folder Path: {folder_path}")
        print(f"  - Groups with Access: {', '.join(groups) if groups else 'None'}")
        
        # Check for the 'Discoverable' setting
        if perms.get('readerGroup'):
             print(f"  - WARNING: This project is DISCOVERABLE by: {perms['readerGroup']}")
        
        print("-" * 40)

if not found_any:
    print(f"No projects found in path: {TARGET_PATH}. Ensure the path starts with a slash and matches exactly!")

# -------------------------------------------------------------------------------- NOTEBOOK-CELL: CODE
import dataiku
client = dataiku.api_client()

projects = client.list_projects()
for p in projects:
    # We look for the display name you see in the UI
    if "pagerduty-sre-fetch-events" in p['name'].lower():
        project_obj = client.get_project(p['projectKey'])
        meta = project_obj.get_metadata()
        print(f"Match Found!")
        print(f"Project Name: {p['name']}")
        print(f"Project Key:  {p['projectKey']}")
        print(f"EXACT PATH:   '{meta.get('folder')}'") # Use this for TARGET_PATH

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
import dataiku

config = dataiku.recipe_config()
output_ds_name = config.get('outputs', {}).get('main', {}).get('items', [{}])[0].get('ref')

ds = dataiku.Dataset(output_ds_name)
ds_path = ds.get_location_info()["info"]["path"]

project_key = dataiku.default_project_key()
hive_table_name = f"{project_key}_{output_ds_name}"

print(output_ds_name)
print(ds_path)
print(hive_table_name)