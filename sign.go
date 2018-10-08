package main

import (
	"bytes"
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
	"os"
)

var gpu = flag.String("GPUID", "123123", "the gpu id")
var maxLoad = flag.Int("maxload", 10, "max load")
var keyPath = flag.String("key", "private.pem", "private key path")
var output = flag.String("out", "device.license", "output license file")

func main() {
	flag.Parse()
	//serialize json
	var configStruct = struct {
		MaxLoad int    `json:"maxload"`
		GPU     string `json:"gpu"`
	}{*maxLoad, *gpu}
	jsonStr, err := json.Marshal(configStruct)
	if err != nil {
		fmt.Println("json序列化失败")
	}
	// sha-1 hash
	t := sha1.New()
	io.WriteString(t, string(jsonStr))
	//sig
	privateKey, err := GetPrivateKey(keyPath)
	if err != nil {
		fmt.Println("获取秘钥", err)
	}
	siged, err := rsa.SignPKCS1v15(nil, privateKey, crypto.SHA1, t.Sum(nil))
	if err != nil {
		fmt.Println("签名失败", err)
		return
	}
	//base64 to string
	sigedStr := base64.StdEncoding.EncodeToString(siged)
	//format string
	var buf bytes.Buffer
	fmt.Fprintf(&buf, "%s;%s", jsonStr, sigedStr)
	//save to file
	ioutil.WriteFile(*output, buf.Bytes(), os.ModePerm)
}

func GetPrivateKey(keyPath *string) (*rsa.PrivateKey, error) {
	//get private key
	conetent, err := ioutil.ReadFile(*keyPath)
	if err != nil {
		fmt.Println("open key file failed")
		return nil, err
	}
	block, _ := pem.Decode(conetent)
	if block == nil {
		fmt.Println("解析私钥失败")
		return nil, fmt.Errorf("%s", "解析私钥失败")
	}
	privateKey, err := x509.ParsePKCS1PrivateKey(block.Bytes)
	if err != nil {
		fmt.Println("解析私钥失败", err)
		return nil, err
	}
	return privateKey, nil
}
