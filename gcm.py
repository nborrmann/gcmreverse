import socket
from bitstring import BitStream
import mcs_pb2
import ssl
import json

# attempt at logging into gcm server. need androidId and securityToken, 
# which can be pulled from a getToken request in a mitm proxy (fiddler)

# currently returns code 4 which means "CLOSE"

with open('credentials.txt', 'r') as f:
	data = json.loads(f.read())
	android_id = data['android_id']
	security_token = data['security_token']


HOST = "mtalk.google.com"
PORT = 5228


lr = mcs_pb2.LoginRequest()
lr.adaptive_heartbeat = False
lr.auth_service = 2
lr.auth_token = str(security_token)
lr.id = "android-11"
lr.domain = "mcs.android.com"
lr.device_id = "android-" + hex(android_id)[2:]
lr.network_type = 1
lr.resource = str(android_id)
lr.user = str(android_id)
lr.use_rmq2 = True
lr.account_id = android_id
lr.received_persistent_id.append("")  # possible source of error

s = lr.setting.add()
s.name = "new_vc"
s.value = "1"

x = lr.SerializeToString()
print(x)


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s = ssl.wrap_socket(s)
s.connect((HOST, PORT))

s.send(x)
while True:
    data = s.recv(1)
    print(data)
    if not data:
    	break
s.close()


















