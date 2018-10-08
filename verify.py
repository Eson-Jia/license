#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import rsa
import base64
import json
pubKey = None

licenseContent = None
with open('device.license') as license:
    licenseContent = license.read()

with open('public.pem') as public:
    pubKey = rsa.PublicKey.load_pkcs1_openssl_pem(public.read())
origin, sig = licenseContent.split(';')

sig = base64.b64decode(sig.encode())
if rsa.verify(origin.encode(), sig, pubKey) == 'SHA-1':
    config = json.loads(origin)
    print('验证通过，GPU编号为：{0}，最大负载为：{1}'.format(config['gpu'], config['maxload']))
