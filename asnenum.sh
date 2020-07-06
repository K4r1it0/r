if [ "$#" -eq  "0" ]
   then
     echo "Usage: ./asnenum.sh google.com"
     exit
 fi

proxy="AKAMAI|CLOUDFLARE"
IFS='|' read -r -a proxys <<< "$proxy"

function getDoamin(){

	printf "\e[1;32mRegistered ASN Domains\n\e[m"
	shodan search asn:AS$1 --fields domains,hostnams --separator " " | awk 'NF > 0' | sort -u 
}

function getIps(){

	printf "\e[1;32mRegistered ASN Hosts\n\e[m"
	 shodan search asn:AS$1 --fields ip_str,port --separator " " | awk '{print "http://"$1":"$2}' | egrep 'http://[0-9].*'
}

proxy="AKAMAI-AS"
result=$(whois -h whois.cymru.com $(dig a $1 +short))
if echo ${result} | grep -q -e ${proxys[0]} -e ${proxys[1]},;then 
	echo "Target is useing proxy"
	exit;
fi 
asn=$(echo ${result} | grep -o "AS Name.*" | awk '{print $3}')
echo ${result}
getIps ${asn}
getDoamin ${asn}
