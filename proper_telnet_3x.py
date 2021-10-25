import getpass
import telnetlib

HOST = input("Enter your host :")
user = input("Enter your remote account: ")

password = getpass.getpass()

cmd = input("Enter your command :")

tn = telnetlib.Telnet(HOST)

tn.read_until(b"Username: ")
tn.write(user.encode('ascii') + b"\n")
if password:
    tn.read_until(b"Password: ")
    tn.write(password.encode('ascii') + b"\n")

tn.write(b"ter len 0\n")
tn.write(cmd.encode('ascii') + b"\n")
tn.write(b"exit\n")

print(tn.read_all().decode('ascii'))
