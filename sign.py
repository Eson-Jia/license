import rsa
import json
privkey = None
with open('jia_rsa', 'r') as f:
    privkey = rsa.PrivateKey.load_pkcs1(f.read().encode())
GPUID = input('input the GPU ID:\n')
maxLoad = input('input max load:\n')

message = json.dumps({'gpu': GPUID, 'maxload': maxLoad})
crypto_message = rsa.sign(message.encode(), privkey, 'SHA-1')

with open('device.licence', 'w') as outFile:
    outFile.write('{0}:{1}'.format(message,crypto_message))
