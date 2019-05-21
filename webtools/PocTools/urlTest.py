#!/usr/bin/python3
# coding: UTF-8
#https://github.com/iceshijie/PocTools/edit/master/urlTest.py
#url连通性测试

import requests

import sys
import ssl
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:66.0) Gecko/20100101 Firefox/66.0",
    "Connection": "keep-alive",
    "Content-Type": "text/xml"
}

def check(url):

    try:
        
        req = requests.post(url,headers=header,verify=False,timeout=5)
        if req.status_code == 200:
            #print("[-] OK",url)
            status = url + " [-] ok"
            return status

        else:
            status = url + " [-] " + str(req.status_code)
            #print("[-] ",req.status_code)
            return status
    except requests.exceptions.ConnectTimeout:
        #print("[-] connect timeout")
        status = url + "  [-] connect timeout"
        return status 
    except requests.exceptions.ConnectionError:
        #print("[-] connect error")
        status = url + "  [-] connect error"
        return status
def urlHttpSDecide(http):
    if http[0:5] == "https":
        return http
    elif http[0:4] =="http":
        return http
    else:
        http = "http://" + http
        return http
 

if __name__ == '__main__':
    with open('urls.txt', 'r') as f:
        for i in f:
            ip = i.strip()
            url = urlHttpSDecide(ip)
            #print(url)
            aa =  check(url)
            with open('jieguo.txt','a') as f:
                f.write(aa + '\n')
		
	
	
