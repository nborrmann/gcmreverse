import checkin_pb2
import random
import requests

cr = checkin_pb2.CheckinRequest()

cr.imei = "109269993813709" # "".join(random.choice("0123456789") for _ in range(15))
cr.androidId= 0
#cr.digest = ""

cr.checkin.build.fingerprint = "google/razor/flo:5.0.1/LRX22C/1602158:user/release-keys"
cr.checkin.build.hardware = "flo"
cr.checkin.build.brand = "google"
cr.checkin.build.radio = "FLO-04.04"
#cr.checkin.build.bootloader = "FLO-04.04"
cr.checkin.build.clientId = "android-google"
#cr.checkin.build.time = "android-google"
#cr.checkin.build.packageVersionCode  = "android-google"
#cr.checkin.build.device  = "android-google"
#cr.checkin.build.sdkVersion = "android-google"
#cr.checkin.build.model = "android-google"
#cr.checkin.build.manufacturer = "android-google"
#cr.checkin.build.product = "android-google"
#cr.checkin.build.otaInstalled = "android-google"

cr.checkin.lastCheckinMs = 0
#cr.checkin.event = 0
#cr.checkin.stat
#cr.checkin.requestedGroup
#cr.checkin.cellOperator
#cr.checkin.simOperator
#cr.checkin.roaming
#cr.checkin.userNumber

#cr.desiredBuild
cr.locale = "en"
cr.loggingId = random.getrandbits(63)
#cr.marketCheckin
cr.macAddress.append("".join(random.choice("ABCDEF0123456789") for _ in range(12)))
cr.meid = "".join(random.choice("0123456789") for _ in range(14))
cr.accountCookie.append("")
cr.timeZone = "GMT"
cr.version = 3
cr.otaCert.append("--no-output--") # 71Q6Rn2DDZl1zPDVaaeEHItd
#cr.serial 
cr.esn = "".join(random.choice("ABCDEF0123456789") for _ in range(8))
#cr.deviceConfiguration
cr.macAddressType.append("wifi")
cr.fragment = 0
#cr.username
cr.userSerialNumber = 0

data = cr.SerializeToString()
headers = {"Content-type": "application/x-protobuffer",
           "Accept-Encoding": "gzip",
           "User-Agent": "Android-Checkin/2.0 (vbox86p JLS36G); gzip"}

print(len(data), data)

r = requests.post("https://android.clients.google.com/checkin", headers=headers, data=data)

print(r.status_code)

if r.status_code == 200:
	cresp = checkin_pb2.CheckinResponse()
	cresp.ParseFromString(r.content)
	print("statsOk", cresp.statsOk)
	print("intent", cresp.intent)
	print("timeMs", cresp.timeMs)
	print("digest", cresp.digest)
	print("marketOk", cresp.marketOk)
	print("androidId", cresp.androidId)
	print("securityToken", cresp.securityToken)
	print("settingsDiff", cresp.settingsDiff)
	print("deleteSetting", cresp.deleteSetting)
	print("versionInfo", cresp.versionInfo)
	print("deviceDataVersionInfo", cresp.deviceDataVersionInfo)
else:
	print(r.text)








