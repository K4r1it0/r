import requests
from bs4 import BeautifulSoup
import re
import time
url =""
ips=set()
c=0
def getd(url):
	session = requests.Session()
	paramsPost = {"query":"http.favicon.hash:784872924 {}".format(url)}
	headers = {"Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9","Connection":"close","User-Agent":"Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.88 Safari/537.36","Referer":"https://www.shodan.io/search?query=http.favicon.hash%3A784872924+-ip%3A77.68.82.43+-ip%3A142.93.118.223+-ip%3A162.208.0.242+-ip%3A70.182.190.49+-ip%3A52.33.195.99+-ip%3A91.250.103.181+-BLKBOX","Sec-Fetch-Site":"same-origin","Sec-Fetch-Dest":"document","Accept-Encoding":"gzip, deflate","Sec-Fetch-Mode":"navigate","Cache-Control":"max-age=0","Upgrade-Insecure-Requests":"1","Sec-Fetch-User":"?1","Accept-Language":"en-US,en;q=0.9,ar;q=0.8","Content-Type":"application/x-www-form-urlencoded"}
	cookies = {"_LOCALE_":"en","_ga":"GA1.2.836267779.1610769571","polito":"\"<>!\"","__cfduid":"<>","session":"<>="}
	response = session.post("https://www.shodan.io/search", data=paramsPost, headers=headers, cookies=cookies)
	return response


while c < 100:
	res = getd(url).text
	if "Invalid search query" in res:
		print("Results")
		for i in ips:
			print(i)
		break
	else:
		s= re.findall(r'/host/\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}',res)
		for i in s:
			if not i.replace('/host/',"") in ips:
				url +=" -ip:{}".format(i.replace('/host/',""))
				ips.add(i.replace('/host/',""))
		c+=1
		print(len(ips),"Total IPS Length")
		time.sleep(10)
