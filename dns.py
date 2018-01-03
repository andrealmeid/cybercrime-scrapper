import requests
import hashlib


def getDomain(url):
    return url.split("//")[-1].split("/")[0]


def func(url):
    req1 = requests.get(url, stream=True)
    ip = req1.raw._fp.fp.raw._sock.getpeername()[0]
    print(ip)
    a = req1.url

    req2 = requests.get("http://" + ip)

    b = req2.url

    print(a, b)
    print(getDomain(a), getDomain(b))
    print(getDomain(a) == getDomain(b))

    if getDomain(a) != getDomain(b):
        print(hashlib.md5(str.encode(req1.text)) == hashlib.md5(str.encode(req2.text)))


func("http://youtube.com")
func("http://stackoverflow.com")
func("http://appleid-lost-iphone.eu/")
