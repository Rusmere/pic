import requests

url = "https://api.short.io/domains/"

import json
payload = json.dumps({"hideReferer":False,"httpsLinks":False,"hostname":"srurl.ml","linkType":"random"})
headers = {
    'accept': "application/json",
    'content-type': "application/json",
    'authorization': "pk_Wt66gzs4F8gaEHzE"
    }

response = requests.request("POST", url, data=payload, headers=headers)

print(response.text)
