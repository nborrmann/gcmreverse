import socket
from bitstring import BitStream
import mcs_pb2
import ssl
import json
import varint

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
print(varint.encode(len(x)))


s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
s = ssl.wrap_socket(s)
s.connect((HOST, PORT))

s.send(bytes([41]))
s.send(bytes([2]))
s.send(varint.encode(len(x)))
s.send(x)
print("reading")

while True:
    responseTag = s.recv(1)
    if responseTag in [b'\x03', b'\x07', b'\x08']:
        length = varint.decode_stream(s)
        msg = s.recv(length)

    if responseTag == b'\x03':
        lresp = mcs_pb2.LoginResponse()
        lresp.ParseFromString(msg)
        print("RECV LOGIN RESP")
        print(lresp)
    elif responseTag == b'\x07':
        iqs = mcs_pb2.IqStanza()
        iqs.ParseFromString(msg)
        print("RECV IQ")
        print(iqs)
    elif responseTag == b'\x08':
        dms = mcs_pb2.DataMessageStanza()
        dms.ParseFromString(msg)
        print("RECV DATA MESSAGE")
        print(dms)
    else:
        print(responseTag)

s.close()
print("closed")
















