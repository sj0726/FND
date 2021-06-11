import requests
import json
from datetime import datetime
import os

path = "/mdfsvc/FND" # os.getcwd() <- doesn't work with crontab

execfile("{}/symbols.py".format(path))
execfile("{}/codes.py".format(path))

def jformat(obj):
    # return a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    return text

def jprint(obj):
    # print a formatted string of the Python JSON object
    text = json.dumps(obj, sort_keys=True, indent=4)
    print(text)

start = datetime.now()

weekday = datetime.today().isoweekday()
if weekday == 7:
    weekday = 0

f = open("{}/CMEAPIOutputs.txt".format(path), "w")
log = open("{}/log/apiLog_{}.txt".format(path, weekday), "w")
 
log.write("Service Start: {}\n".format(start))
count = 0
notFound = 0
failed = 0

key = {
    'grant_type':'client_credentials',
    'client_id':'api_gemizip_v2',
    'client_secret':'ENW2MIW54X7RMYEEL6RYXBQJEPSAEIGRQWVFCZQ=',
}

def getAccessToken():
    r = requests.post('https://auth.cmegroup.com/as/token.oauth2', data=key)
    token = r.json()["access_token"]
    api_call_headers = {'Authorization': 'Bearer ' + token}
    return api_call_headers

apiHeaders = getAccessToken()

for i in range(len(symbols)):
    try:
        link = 'https://api.refdata.cmegroup.com/v2/instruments?globexSymbol={}'.format(symbols[i])
        count += 1
        
        numRequests = 1
        while numRequests <= 3:
            if numRequests == 3:
                raise Exception("All requests failed for {}.".format(symbols[i]))
            try:
                products = requests.get(link, headers=(apiHeaders))
                if products.status_code == 200:
                    log.write("\n{} > GET Request for {} Successful!".format(datetime.now(), symbols[i]))
                    break
                elif products.status_code == 403:
                    log.write("\n{} > {}. Obtaining new access token...".format(datetime.now(), products.json()["message"]))
                    apiHeaders = getAccessToken()
                    numRequests += 1
                else:
                    log.write("\n{} > Error: {} (Status Code {})".format(datetime.now(), products.content.replace("\n", ""), products.status_code))
                    numRequests += 1
            except Exception, e:
                log.write("\n{} > Request failed for {}. Retrying... ({})".format(datetime.now(), symbols[i], str(e)))
                numRequests += 1
        
        temp = products.json()["_embedded"]["instruments"]
        found = False

        for y in range(len(temp)):
            if (temp[y]["globexSymbol"] == symbols[i]):
                found = True
                currTime = str(datetime.now().strftime("%Y%m%d%H%M%S%f"))
                
                fnd = str(temp[y]["firstNoticeDate"]).replace("-", "")
                print("{}'s FND: {}".format(temp[y]["globexSymbol"], str(temp[y]["firstNoticeDate"])))
                if (fnd == "None"):
                    fnd = "        "
                
                ltd = str(temp[y]["lastTradeDate"]).replace("-", "")
                if (ltd == "None"):
                    ltd = "        "
                
                globexSymb = codes[i] # temp[y]["globexSymbol"]
                globexSymb += (16 - len(globexSymb)) * " "

                messageSeq = str(count - notFound - failed)
                messageSeq += (10 - len(messageSeq)) * " "

                ltd += (16 - len(ltd)) * " "
                fnd += (16 - len(fnd)) * " "
                
                res = "T80E01  {}{}{}{}{}".format(currTime, globexSymb, messageSeq, ltd, fnd)
                res += (186 - len(res)) * " "

                f.write(res + "\n")

        if not found:
            notFound += 1
            log.write(" (Symbol Missing)")

    except Exception, e:
       log.write("\n{} > {}".format(datetime.now(), str(e)))
       failed += 1

f.close()

end = datetime.now()

log.write("\n\nService End: {}\n".format(end))
log.write("\nRun Time: {}".format(end - start))
log.write("\nTotal Requests: {}".format(count))
log.write("\nMissing Symbols: {}".format(notFound))
log.write("\nFailed Requests: {}".format(failed))
log.write("\nFetched Data: {}".format(count - notFound - failed))

log.write("\n\n---------------------------------------------------------------------------------------------------------------------------------------------------\n\n")

log.close()