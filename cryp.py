import rsa

# 生成密钥
(pubkey, privkey) = rsa.newkeys(1024)


# =================================
# 场景〇：密钥保存导入
# =================================
# 保存密钥
with open('public.pem','w+') as f:
    f.write(pubkey.save_pkcs1().decode())

with open('private.pem','w+') as f:
    f.write(privkey.save_pkcs1().decode())


# 导入密钥
with open('public.pem','r') as f:
    pubkey = rsa.PublicKey.load_pkcs1(f.read().encode())

with open('private.pem','r') as f:
    privkey = rsa.PrivateKey.load_pkcs1(f.read().encode())

    
# =================================
# 场景一：数据泄密问题
# 为了开拓市场，公司经理分派了一群业务员到世界各地考察商机。
# 业务员们都很精明强干，很快就各自发现了很好的商机。
# 时间就是金钱！他们必须马上用email向经理汇报。
# 这就麻烦来了：网络是及其不安全的！
# 各种数据被抓包、邮箱密码泄露...太可怕了！商业竞争对手的各种手段太可怕了！
# 如何让业务员的email安全地送到公司经理的手里？(即使数据被抓包、邮箱密码泄露...)
# 太不安全了，怎么办？
#  
# 没错！聪明的您一定想到了：加密。
# =================================

# 明文：业务员发现的商机
message = '这是商机：...'

# 业务员用公司经理事先给的公钥对明文加密，得到密文
crypto_email_text = rsa.encrypt(message.encode(), pubkey)

# 然后，业务员用email发送密文
# 。。。


# email在网络传输中 。。。（各种数据被抓包、邮箱密码泄露）
# 没办法，还是被有心人看到了这封email:
print(crypto_email_text) # 什么鬼？看不懂啊！


# 最后，公司经理也收到了业务员们发了的email。打开，也只看到一堆奇怪的字符！
# 没问题，公司经理用自己的私钥对收到的密文进行解密，就可得到明文
message = rsa.decrypt(crypto_email_text, privkey).decode()

# 然后，就可以看到重要的商机信息了
print(message)


# =================================
# 场景二：身份确认问题
# 为了开拓市场，公司经理分派了一群业务员到各地考察商机。
# 在这过程中，公司经理常常通过email向业务员下达重要指令
# 然而，网络是及其不安全的！譬如：数据包被修改、邮箱密码泄露...
# 商业竞争对手可以通过各种手段伪造/修改公司经理的重要指令！
# 
# 话说这天早上，业务员照常打开邮箱，发现公司经理的一封email：命令他马上回国。
# 不对啊。昨天说要在这边扩大业务，怎么今天就变了？
# 这封email是公司经理本人发的吗？
# 怎么办？
# 
# 没错！聪明的您一定也想到了：签名。
# =================================

# 明文：公司经理的指令
message = '这是重要指令：...'

# 公司经理私钥签名
crypto_email_text = rsa.sign(message.encode(), privkey, 'SHA-1')

# 业务员同时收到指令明文、密文，然后用公钥验证，进行身份确认
rsa.verify(message.encode(), crypto_email_text, pubkey)