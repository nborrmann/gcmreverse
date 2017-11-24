import checkin_pb2
import random
import requests

def getAndroidId():
	# most minimal checkin request possible
	cr = checkin_pb2.CheckinRequest()
	cr.checkin.build.sdkVersion = 18
	cr.version = 3
	cr.fragment = 0

	data = cr.SerializeToString()
	headers = {"Content-type": "application/x-protobuffer",
    	       "Accept-Encoding": "gzip",
        	   "User-Agent": "Android-Checkin/2.0 (vbox86p JLS36G); gzip"}
	r = requests.post("https://android.clients.google.com/checkin", headers=headers, data=data)

	if r.status_code == 200:
		cresp = checkin_pb2.CheckinResponse()
		cresp.ParseFromString(r.content)
		android_id = cresp.androidId
		security_token = cresp.securityToken
		return android_id, security_token
			
	else:
		print(r.text)

def getPushToken(android_id, security_token):
	headers = {"Authorization":"AidLogin {}:{}".format(android_id, security_token)}
	data = {'app': 'com.tellm.android.app',
			'sender': '425112442765',
			'device': str(android_id),
			'cert': 'a4a8d4d7b09736a0f65596a868cc6fd620920fb0',
			'app_ver': '1001800',
			'gcm_ver': '11055448',
#			'X-appid': '$randomString',
			'X-scope': 'GCM',
			'X-app_ver_name': '4.48.0'}

	r = requests.post("https://android.clients.google.com/c2dm/register3", data=data, headers=headers)
	print(r.status_code, r.text)


android_id, security_token = getAndroidId()
print(android_id, security_token)
getPushToken(android_id, security_token)





