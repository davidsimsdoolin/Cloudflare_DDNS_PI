import http.client
import urllib.request
import logging
import json

#Following will need custom information
AuthEmail = "TBD"
AuthKey = "TBD"
ZoneID = "TBD"
Record = "TBD"
RecordID = "TBD"

#Setup for logging
logs = ""
logging.basicConfig(filename='cloudflare.log',filemode = 'a', format='%(asctime)s,%(msecs)d %(name)s %(levelname)s %(message)s',datefmt='%H:%M:%S', level=logging.DEBUG)

#Retrieval of current physicla IP and comparison to previous
#Prevents lots of unneeded api calls.
ExternalIP = urllib.request.urlopen('https://ident.me').read().decode('utf8')
read = open("ip.txt", "r")
OldIP = read.read()
logs = "Current IP is " + ExternalIP

#Api Call
if ExternalIP == OldIP:
	logs = logs + "| IP has not changed."
else:
	try:
		conn = http.client.HTTPSConnection("api.cloudflare.com")
		payload = "{\n  \"content\": \"" + ExternalIP + "\",\n  \"name\": \"" + Record + "\",\n  \"proxied\": true,\n  \"type\": \"A\"}"
		headers = {'Content-Type': "application/json",'X-Auth-Email': AuthEmail,'X-Auth-Key': AuthKey}
		conn.request("PUT", "/client/v4/zones/" + ZoneID + "/dns_records/" + RecordID, payload, headers)

		res = conn.getresponse()
		data = res.read()
		logs = logs + "|IP has changed and DNS set"
		write = open("ip.txt", "w")
		write.write(ExternalIP)	
	except:
		logs = logs + "|Error with api call."

#Writing to log
logging.info(logs)
