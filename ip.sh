function usage(){
	echo "Usage: ./ip.sh --target https://target.com -f queueTime -m"
	echo "-f --fingerprint: A valid string from target response"
	echo "-m --manual: for manual mood"	
	echo "-e --enumerate: for hosts enumeration mood"
}
if [ "$#" -eq  "0" ]
   then
     usage
     exit
 fi
while [ "$1" != "" ]; do
    case $1 in
        -t | --target )         shift
                                target=$1
                                ;;
        -f | --fingerprint )         shift
                                fingerprint=$1
                                ;;
        -m | --manual )    manual=1
		                        ;;
        -e | --enumerate )    enumeration=1
                                ;;
        -h | --help )           usage
                                exit
                                ;;
        * )                     usage
                                exit 1
    esac
    shift
done

host=$(echo ${target} | sed 's/https\?:\/\///g')

export PYTHONWARNINGS="ignore:Unverified HTTPS request"

function fingerprint(){
	my_string=$(curl $1 -LsI --insecure | grep -m1 Set-Cookie)
IFS=' ' read -ra my_array <<< "$my_string"
for i in "${my_array[@]}"
do
	if [[ $i =~ "=" ]]
	then
   		echo $i | sed 's/=.*$//g'
   		break
	fi
done	
}
f=$(fingerprint ${target})
function checker(){
	request=$(curl $1 -H "host: $2" -LsI --insecure | grep -m1 Set-Cookie)
IFS=' ' read -ra string <<< "$request"
for i in "${string[@]}"
do
	if [[ $i =~ "=" ]]
	then
   		echo $i | sed 's/=.*$//g'
   		break
	fi
done	
}


function favicon(){
hash=$(python -c "import mmh3;import requests;r=requests.get('$1'+'/favicon.ico',verify=False,allow_redirects=True);print mmh3.hash(r.content.encode('base64'))")
echo ${hash}
}
result=$(shodan search http.favicon.hash:$(favicon ${target}) --fields ip_str 2> /dev/null)
function auto(){

	IFS="" ; echo ${result} | while read ip;do if [[ $ip == *":"* ]];then :;else if echo $(checker ${target} ${host}) | grep -q ${f};then echo "Possible Real Ip : $ip" | grep -v "104\.";fi;fi;done

}


function manual()
{
	IFS="" ; echo ${result} | while read ip;do if [[ $ip == *":"* ]];then :;else if curl -sL --insecure ${target}/test -H "host: ${host}" | grep -q $1;then echo "Possible Real Ip : $ip" | grep -v "104\.";fi;fi;done

}

function enum(){

	IFS="" ; echo ${result} | while read ip;do if [[ $ip == *":"* ]];then :;else echo $ip;fi;done
}

if curl -LIs ${target}/favicon.ico | grep -q "image/" ;then :;else echo "No Favicon Found";exit;fi
if [[ ${enumeration} == 1 ]];then enum;exit;else :;fi
if [[ ${manual} == 1 ]];then manual ${fingerprint};else auto;fi


