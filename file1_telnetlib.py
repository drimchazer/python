from telnetlib import Telnet

cmd = input('Enter the command: \n')

tn = Telnet('192.168.21.236', 23)   # connect to telnet port
tn.write(b'admin15\r\n')
tn.write(b'password\r\n')
tn.write(b'ter len 0\r\n')
tn.write(cmd.encode('ascii')+b'\n')
tn.write(b'exit\r\n')
print(tn.read_all().decode('ascii'))
