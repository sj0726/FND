import requests
import json

symbols = ["6AH2"]

key = {
    'grant_type':'client_credentials',
    'client_id':'api_gemizip_v2',
    'client_secret':'ENW2MIW54X7RMYEEL6RYXBQJEPSAEIGRQWVFCZQ=',
}

def jprint(obj):
    # print a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

def getAccessToken():
    r = requests.post('https://auth.cmegroup.com/as/token.oauth2', data=key)
    token = r.json()["access_token"]
    api_call_headers = {'Authorization': 'Bearer ' + token}
    return api_call_headers

apiHeaders = getAccessToken()
link = 'https://api.refdata.cmegroup.com/v2/instruments?globexSymbol={}'.format(symbols[0])

products = requests.get(link, headers=(apiHeaders))

x = products.json()

jprint(x)