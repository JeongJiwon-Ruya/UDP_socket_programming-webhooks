import socket
import os
import sys
import hashlib
import math
import time

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    port_num = 5001
    s.bind(('', int(port_num)))
    print("server socket created.")
except socket.error:
    print("failed to create socket")
    sys.exit()

def check_md5(path):
    f = open(path, 'rb')
    data = f.read()
    md5_hash = hashlib.md5(data).hexdigest()
    return md5_hash

def sender_send(file_name):
    s.sendto("valid list command.".encode(), client_addr)##
    
    if not os.path.isfile(file_name):
        sys.exit()
    s.sendto("file exists!".encode(), client_addr)###
    
    read_file = open(file_name, 'rb')
    file_size = os.path.getsize(file_name)
    check = math.ceil(file_size/4096)
    s.sendto(str(check).encode(), client_addr)####
    
    while check != 0:
        chunk_file = read_file.read(4096)
        s.sendto(chunk_file, client_addr)
        check -= 1
        print("packet number ", check)
        time.sleep(0.02)
    

    md5_hash = check_md5(file_name)
    s.sendto(md5_hash.encode('utf-8'), client_addr)

if __name__ == "__main__":
    try:
        data, client_addr = s.recvfrom(4096)
    except ConnectionResetError:
        print("error. port number not matching.")
        sys.exit()

    text = data.decode('utf8')
    handler = text.split()

    if handler[0] == 'receive':
        sender_send(handler[1])
    elif handler[0] == 'exit':
        sys.exit()
