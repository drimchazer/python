import paramiko
import time
from getpass import getpass

username = 'admin15'
password = 'password'

rtr_list = open ('devices.txt')
for rtr in rtr_list:
	print('### connecting to device ' + rtr.strip() + '###\n')
	SESSION = paramiko.SSHClient()
	SESSION.set_missing_host_key_policy(paramiko.AutoAddPolicy())
	SESSION.connect(rtr.strip(),port=22,
			username = username,
			password = password,
			look_for_keys = False,
			allow_agent = False)

	DEVICE_ACCESS = SESSION.invoke_shell()
	
	cmd = open('command.txt')
	for lines_cmd in cmd:
		DEVICE_ACCESS.send(lines_cmd)
		time.sleep(2)
	output = DEVICE_ACCESS.recv(65000)
	print(output.decode('ascii'))
	
	SESSION.close
