import rsa
import base64
pubKey = None

licenseContent = None
with open('device.license') as license:
    licenseContent = license.read()

with open('public.pem') as pub:
    pubKey = rsa.PublicKey.load_pkcs1(pub.read())
origin, sig = licenseContent.split(';')

sig = base64.b64decode(sig.encode())
print(rsa.verify(origin.encode(), sig, pubKey))
