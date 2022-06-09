# import_epics.py
import requests
from requests.auth import HTTPBasicAuth
import json
import csv

## Jira specifics
# Jira URL
JIRA_URL = 'https://www.jira.com/rest/api/latest'
# Jira user credentials (incl. API token)
JIRA_ACCOUNT = ('mail id ', 'jira token')
# Jira project ID (short)
JIRA_PROJECT = 'project ID'
# Jira Query (JQL)
JQL = 'project=%s+AND+resolution=Unresolved+ORDER+BY+createdDate+ASC&maxResults=20' % JIRA_PROJECT
# +AND+issueType=Epic

# *False* if Jira  is using self-signed certificates, otherwise *True*
VERIFY_SSL_CERTIFICATE = True


# GET request
def jira_get_request(endpoint):
    print("endpoint :" + endpoint)
    response = requests.get(
        JIRA_URL + endpoint,
        auth=HTTPBasicAuth(*JIRA_ACCOUNT),
        verify=VERIFY_SSL_CERTIFICATE,
        headers={'Content-Type': 'application/json'}
    )
    print(response)
    if response.status_code != 200:
        raise Exception("Unable to read data from %s!" % JIRA_PROJECT)

    return response.json()

##############################################################################


# Get Jira data
jira_issues = jira_get_request('/search?jql=' + JQL)
print(jira_issues)
with open('data.json', 'w') as file:
    json.dump(jira_issues, file)


with open('data.json') as json_file:
    data = json.load(json_file)

data_file = open('data.csv', 'w', newline='',encoding="utf8")
csv_writer = csv.writer(data_file)
count = 0
jira_data = data['issues']
for item in jira_data:
    if count == 0:
        # Writing headers of CSV file
        header = item.keys()
        csv_writer.writerow(header)
        count += 1

    # Writing data of CSV file
    csv_writer.writerow(item.values())

data_file.close()
