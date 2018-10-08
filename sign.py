#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rsa
import json
import base64
privkey = None
with open('private.pem', 'r') as f:
    privkey = rsa.PrivateKey._load_pkcs1_pem(f.read().encode())
GPUID = input('input the GPU ID:\n')
maxLoad = input('input max load:\n')

originMessage = json.dumps({'gpu': GPUID, 'maxload': maxLoad})
sigMessage = rsa.sign(originMessage.encode(), privkey, 'SHA-1')
sigStr = base64.b64encode(sigMessage).decode()
with open('device.license', 'w') as outFile:
    outFile.write('{0};{1}'.format(originMessage, sigStr))
