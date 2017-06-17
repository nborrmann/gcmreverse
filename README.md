# gcmreverse

Verification process:

### 1. InstanceID.getToken:

Google Cloud Messaging/Firebase Cloud Messaging: https://developers.google.com/android/reference/com/google/android/gms/iid/InstanceID

happens in:
```
com/jodelapp/jodelandroidv3/usecases/verification/GetInstanceIdTokenImpl.java
com/jodelapp/jodelandroidv3/data/gcm/RegistrationIntentService.java
```

needs a senderId, which is 425112442765 (grep for that in the code)

i'll post the requests i saw in mitm to that api in the repo

I was able to get a token using this request, however it is different from the one I saw in the mitm.
```
curl "https://android.clients.google.com/c2dm/register3" -H "Authorization: AidLogin $androidID:$securityToken" --data "app=com.tellm.android.app&sender=425112442765&device=$androidId&cert=a4a8d4d7b09736a0f65596a868cc6fd6209 20fb0&app_ver=1001800&gcm_ver=11055448&X-appid=$randomString&X-scope=*&X-app_ver_name=4.48.0" -k
```
Maybe because I omitted the ``X-sig`` header? Maybe this is some kind of signing which gives a token but it is not actually valid?
I'll try to modify the token in the request and see what happens.

Update: I have managed to verify that the above request returns an actual working token by intercepting and modifying requests in fiddler.


### 2. sendPushToken

token from gcm is sent to jodel servers using this endpoint:
```python
def send_push_token(self, client_id, push_token, **kwargs):
    return self._send_request("PUT", "/v2/users/pushToken", payload={"client_id": client_id, "push_token": push_token}, **kwargs)
```
I have verified that this is same token that the app gets in the previous step.

### 3. receive verification_code via GCM and post it to jodel api

no progress here. I don't see the gcm traffic in fiddler mitm, and I havent managed to receive gcm messages myself.

```python
def verify_push(self, server_time, verification_code, **kwargs):
    return self._send_request("POST", "/v3/user/verification/push", payload={"server_time": server_time, "verification_code": verification_code}, **kwargs)
```

Possible path forward:
1. install a signature spoofed ROM: https://github.com/microg/android_packages_apps_GmsCore/wiki/Signature-Spoofing
2. install microG fake gapps
3. check if jodel verification works (if yes, we know that it is fully reversible by just looking at the open source gmscore app) **Update: Verification works**.

We need to find out how to receive GCM messages from the server and we are pretty much done.


## Other interesting things:
```
# grep -Pri 425112442765 jodel-4.48.0/i
jodel-4.48.0/apktool/res/values/strings.xml:    <string name="default_web_client_id">425112442765-rh5u1d604qrmgjmv0sj31d4eohnhartg.apps.googleusercontent.com</string>
jodel-4.48.0/apktool/res/values/strings.xml:    <string name="gcm_defaultSenderId">425112442765</string>
jodel-4.48.0/apktool/res/values/strings.xml:    <string name="gcm_senderId">425112442765</string>
jodel-4.48.0/apktool/res/values/strings.xml:    <string name="google_app_id">1:425112442765:android:2f4503e0808c2362</string>
```

OSS implementation of google play services:
https://github.com/microg/android_packages_apps_GmsCore

Particularly interesting:
https://github.com/microg/android_packages_apps_GmsCore/blob/master/play-services-core/src/main/java/org/microg/gms/gcm/RegisterRequest.java















