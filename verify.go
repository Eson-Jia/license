package main

import (
	"crypto"
	"crypto/rsa"
	"crypto/sha1"
	"crypto/x509"
	"encoding/base64"
	"encoding/json"
	"encoding/pem"
	"flag"
	"fmt"
	"io"
	"io/ioutil"
	"strings"
)

var publicKey = []byte(`
-----BEGIN PUBLIC KEY-----
MIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEA3ro6QTpuKsX+z+Y4iHke
UXr0LdAEcHFhuIeYv3YKtLuLGAdGtwR3ZwEKrcSYwQ5FOER0Rbj8gX3q19vZeXex
+svz+CnbjZqc3c3lrycGLd4hGjV8ACreOfsUoXHJ/yfbf7sSczs8aqhYhdkLRUn5
zT0NwrmAVKaCFpQdzxD9OiWFFb/46seKelOdpTKD3D4voD7vypSQ9CHdyftgdJ6k
ucyZDu98qwYgTV8bAwMB0q5DRNGhISOsbhgGd57c84helrdSyCOfk/ZT89xzFyyY
b5+Dk8Et5A1f2rR3kvtpqDCuJQbeeHs4bA/kkLOKzlRXKeYuSYInRBnaacJQo2Ta
BwIDAQAB
-----END PUBLIC KEY-----
`)
var filePath = flag.String("input", "device.license", "license file path")

func main() {
	block, _ := pem.Decode(publicKey)
	if block == nil {
		fmt.Println("解析公钥失败")
		return
	}

	pubInterface, err := x509.ParsePKIXPublicKey(block.Bytes)
	if err != nil {
		fmt.Println("解析公钥失败", err)
		return
	}
	pub := pubInterface.(*rsa.PublicKey)
	b, err := ioutil.ReadFile(*filePath)
	if err != nil {
		fmt.Println("读取配置文件失败", err)
		return
	}
	content := string(b)
	results := strings.Split(content, ";")
	config, siged := results[0], results[1]
	data, err := base64.StdEncoding.DecodeString(siged)
	t := sha1.New()
	io.WriteString(t, config)
	if err := rsa.VerifyPKCS1v15(pub, crypto.SHA1, t.Sum(nil), data); err != nil {
		fmt.Println("验证未通过")
		return
	}
	var configStruct struct {
		Maxload int    `json:"maxload"`
		GPU     string `json:"gpu"`
	}
	if err := json.Unmarshal([]byte(config), &configStruct); err != nil {
		fmt.Println("反序列化json失败", err)
		return
	}
	fmt.Println("验证通过，", "最大负载：", configStruct.Maxload, "GPU编号：", configStruct.GPU)
}
