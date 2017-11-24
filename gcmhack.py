import checkin_pb2
import random
import requests

def getAndroidId():
	# most minimal checkin request possible
	cr = checkin_pb2.CheckinRequest()
	cr.androidId= 0
	cr.checkin.build.fingerprint = "google/razor/flo:5.0.1/LRX22C/1602158:user/release-keys"
	cr.checkin.build.hardware = "flo"
	cr.checkin.build.brand = "google"
	cr.checkin.build.radio = "FLO-04.04"
	cr.checkin.build.clientId = "android-google"
	cr.checkin.build.sdkVersion = 21
	cr.checkin.lastCheckinMs = 0
	cr.locale = "en"
	cr.macAddress.append("".join(random.choice("ABCDEF0123456789") for _ in range(12)))
	cr.meid = "".join(random.choice("0123456789") for _ in range(15))
	cr.timeZone = "Europe/London"
	cr.version = 3
	cr.otaCert.append("--no-output--")
	cr.macAddressType.append("wifi")
	cr.fragment = 0
	cr.userSerialNumber = 0

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





