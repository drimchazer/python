import getpass
import sys
import telnetlib

HOST = raw_input("Enter the host: ")
#HOST = '192.168.21.236'
user = raw_input("Enter your remote account: ")
password = getpass.getpass()
cmd = raw_input("Enter command :")

tn = telnetlib.Telnet(HOST)
tn.read_until("Username: ")
tn.write(user + "\n")
if password:
    tn.read_until("Password: ")
    tn.write(password + "\n")
    
tn.write("ter len 0\n")
tn.write(cmd + "\n")
tn.write("exit\n")

print tn.read_all()
