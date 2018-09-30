import rsa
import base64
pubKey = None

licenseContent = None
with open('device.license') as license:
    licenseContent = license.read()

with open('jia_rsa.pub', 'r') as pub:
    pubKey = pub.read()
origin, sig = licenseContent.split(';')
sig = base64.b64decode(sig.encode('UTF-8'))
print(rsa.verify(origin, sig, pubKey))
