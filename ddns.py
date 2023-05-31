import http.client
import urllib.request
import logging
import json

#Reading in json of api request variables in Dict
apiFile = open('apiData.json')
apiDict = json.load(apiFile)

#Following will need custom information
authEmail = apiDict['authEmail']
authKey = apiDict['authKey']
zoneID = apiDict['zoneID']
record = apiDict['record']
recordID = apiDict['recordID']

#Setup for logging
logs = ""
logging.basicConfig(filename='ddns.log',filemode = 'a+', format='%(asctime)s, %(levelname)s %(message)s',datefmt='%H:%M:%S', level=logging.DEBUG)

#Retrieval of current physical IP and comparison to previous
#Prevents lots of unneeded api calls.
externalIP = urllib.request.urlopen('https://ident.me').read().decode('utf8')
ipFile = open("ip.txt", "a+")
oldIP = ipFile.read()
logs = "Current IP is " + externalIP

#Api Call
if externalIP == oldIP:
	logs = logs + "| IP has not changed."
else:
	try:
		conn = http.client.HTTPSConnection("api.cloudflare.com")
		payload = "{\n  \"content\": \"" + externalIP + "\",\n  \"name\": \"" + record + "\",\n  \"proxied\": true,\n  \"type\": \"A\"}"
		headers = {'Content-Type': "application/json",'X-Auth-Email': authEmail,'X-Auth-Key': authKey}
		conn.request("PUT", "/client/v4/zones/" + zoneID + "/dns_records/" + recordID, payload, headers)
		res = conn.getresponse()
		data = res.read()
		if str(data).__contains__("\"success\":false"):
			logs = logs + "| API call returned error| " + str(data)
		else:
			logs = logs + "| IP has changed and DNS set"
			ipFile.write(externalIP)	
	except:
		logs = logs + "| Error with api call."

#Writing to log
logging.info(logs)
