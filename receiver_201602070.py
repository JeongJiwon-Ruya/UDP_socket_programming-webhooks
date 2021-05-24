import socket
import os
import sys
import hashlib

def check_md5_hash(path):
    f = open(path, 'rb')
    data = f.read()
    md5_hash = hashlib.md5(data).hexdigest()
    return md5_hash

#file_name = input()
rec_argv = sys.argv
if len(rec_argv) > 3:
    print("over input")
    sys.exit()
ip_addr = rec_argv[1]
port_num = rec_argv[2]

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setblocking(0)
    s.settimeout(15)

except socket.error:
    print("failed to create socket")
    sys.exit()

#host = "localhost"#
#port = 8000#

msg_to_send = input("enter a command: \n1.receive [file_name]\n2.exit\n")
s.sendto(msg_to_send.encode(), (ip_addr, int(port_num))) 
msg_cmd, addr = s.recvfrom(4096)##
print(msg_cmd.decode())
msg_fileExist, addr = s.recvfrom(4096)###
print(msg_fileExist.decode())

newfile = "copy_"+msg_to_send.split()[1]

write_file = open(os.getcwd()+"/"+newfile,'wb')
msg_size, addr = s.recvfrom(4096)####
msg_size = int(msg_size.decode())

while msg_size != 0:
    chunk_file, addr = s.recvfrom(4096)
    write_file.write(chunk_file)
    print("Received packet number: ", msg_size)
    msg_size -= 1 

write_file.close()

# Do not modify the code (below)
rec_md5_hash, addr = s.recvfrom(4096)
		
if rec_md5_hash.decode('utf8') == check_md5_hash(newfile): # 
    print("True")
else:
    print("False")
