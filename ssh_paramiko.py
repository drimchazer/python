import paramiko
import time
from getpass import getpass

ip = '192.168.21.236'
username = 'admin15'
password = 'password'

SESSION = paramiko.SSHClient()
SESSION.set_missing_host_key_policy(paramiko.AutoAddPolicy())
SESSION.connect(ip,port=22,
		username = username,
		password = password,
		look_for_keys = False,
		allow_agent = False)

DEVICE_ACCESS = SESSION.invoke_shell()
DEVICE_ACCESS.send(b'term len 0\n')
DEVICE_ACCESS.send(b'show ip int br\n')
time.sleep(2)
output = DEVICE_ACCESS.recv(65000)
print(output.decode('ascii'))

SESSION.close
