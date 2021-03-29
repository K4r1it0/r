import requests
import urllib3
from bs4 import BeautifulSoup
import signal
import re
import time
urllib3.disable_warnings()
username=""
password=""
query = input("Query: ")#"ssl:oktaprise"


def session(username,password):
	global headers
	headers = {
	    'Content-Type': 'application/x-www-form-urlencoded',
	    'User-Agent': 'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36',
	    'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9'}

	session = requests.session()
	csrfres = session.get("https://account.shodan.io/login",headers=headers).text
	csrf = BeautifulSoup(csrfres,'html.parser').find('input',{"name":"csrf_token"})['value']
	data = 'username={}&password={}&grant_type=password&continue=https%3A%2F%2Faccount.shodan.io%2F&csrf_token={}'.format(username,password,csrf)
	r = session.post('https://account.shodan.io/login', headers=headers, data=data)
	return session


def getlen(session):

	response = session.get("https://www.shodan.io/search/_summary?query={}".format(query),headers=headers).text
	length = BeautifulSoup(response,'html.parser').find('div',{"class":"bignumber"}).text
	return int(length)-1


def getd(query,url,session):
	paramsPost = {"query":"{} {}".format(query,url)}
	response = session.post("https://www.shodan.io/search", data=paramsPost, headers=headers)
	return response.text


session = session()
length = getlen(session(u,p))
reip = 0
c=0
ips=[]
url =""
counter = len(ips) 

for result in range(length):
	if reip < 3:
		res = getd(query,url,session)

		if "Invalid search query" in res:
			print("Invalid search query")
			break

		if "Daily search usage limit reached" in res:
			print("Daily search usage limit reached")
			for i in list(dict.fromkeys(ips)):
				print(i)
			break
		elif len(ips) == length:
			for i in list(dict.fromkeys(ips)):
				print(i)
			break
		else:
			s= re.findall(r'/host/\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',res)	
			for i in s:
				if not i.replace('/host/',"") in ips:
					url +=" -ip:{}".format(i.replace('/host/',""))
					ips.append(i.replace('/host/',""))
			c+=1
			if len(ips) == counter:
				reip +=1
				time.sleep(10)
			counter = len(ips)	
	else:
		for i in list(dict.fromkeys(ips)):
					print(i)
