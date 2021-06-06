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
    s.setblocking(0)
    s.settimeout(10)
    print("server socket created.")
except socket.error:
    print("failed to create socket")
    sys.exit()

def check_md5(path):
    f = open(path, 'rb')
    data = f.read()
    md5_hash = hashlib.md5(data).hexdigest()
    return md5_hash

def checksum(data):
    data_length = sys.getsizeof(data)
    headers = ""

    sourceIp = "192.168.0.4"
    destinIp = "192.160.0.2"
    sIPA = ""
    dIPA = ""
    for i in range(4):
        sIPA += format(int(sourceIp.split('.')[i]), 'x').zfill(2)
        dIPA += format(int(destinIp.split('.')[i]), 'x').zfill(2)
    zeros = format(0, 'x').zfill(2)
    protocol = format(17, 'x')
    UDP_Length = format((8+data_length), 'x').zfill(4)
    s_Port = format(8000, 'x').zfill(4)
    d_Port = format(53109, 'x').zfill(4)
    Length = UDP_Length
    before_checksum = format(0, 'x').zfill(4)

    headers += sIPA
    headers += dIPA
    headers += zeros
    headers += protocol
    headers += UDP_Length
    headers += s_Port
    headers += d_Port
    headers += Length
    headers += before_checksum

    data_ = headers+data.decode()
    data_ = data_.encode()

    tsum = ""
    for j in range(0,len(data_),2):
        x = format(data_[j],'x')
        if len(data_)%2 == 0:
            y = format(data_[j+1],'x')
        else:
            y = format(0,'x')
        z = x+y
        if tsum == "":
            tsum = format(int(z,16), 'x')
        else :
            tsum = format(int(tsum,16) + int(z,16), 'x')
        if len(tsum) > 4 :
            tsum = format(int(tsum[0], 16) + int(tsum[1:], 16), 'x')

    before = (bin(int(tsum,16))[2:]).zfill(16)
    after = ""
    for k in range(len(before)):
        if before[k] == "0":
            after = after+"1"
        else :
            after = after+ "0"
    checksum = format(int(after,2), 'x').zfill(4)
         
    headers_ = ""    
    headers_ += sIPA
    headers_ += dIPA
    headers_ += zeros
    headers_ += protocol
    headers_ += UDP_Length
    headers_ += s_Port
    headers_ += d_Port
    headers_ += Length
    headers_ += checksum

    return headers_

zero = "0"
one = "1"
nak = "NAK"
rACK = ""

def sender_send(file_name = "speech_script.txt"):
    s.sendto("valid list command.".encode(), client_addr)##
    
    if not os.path.isfile(file_name):
        sys.exit()
    s.sendto("file exists!".encode(), client_addr)###
    
    read_file = open(file_name, 'rb')
    file_size = os.path.getsize(file_name)
    print("File Size :",file_size)
    check = math.ceil(file_size/981)
    # checksum_bytes = checksum(str(check).encode())
    # check_count = checksum_bytes + str(check)
    s.sendto(str(check).encode(), client_addr)####
    

    test_1 = False #  for ERROR 1

    i = 1
    while i <= check:
        chunk_file = read_file.read(981)
        # checksum_bytes = checksum(chunk_file)
        sendfile = chunk_file.decode('utf-8')
        
        if i == 1 :
            sACK = zero
        elif rACK == zero:
            sACK = zero
        elif rACK == one:
            sACK = one 

        sendfile = sACK + sendfile
            
        while True:
            # sendfile = sACK + checksum_bytes + sendfile
            if i == 5 and test_1:
                test_1 = False
                s.sendto(sendfile.encode('utf-8'), (client_ip,5002))
            else :
                s.sendto(sendfile.encode('utf-8'), client_addr)
            print("### final checksum ###")
            print("packet number ", i)
            print("sending index :", sACK)
            try:
                rACK, _ = s.recvfrom(4096)
                rACK = rACK.decode()
                if rACK == nak:
                    continue

                elif rACK != sACK :
                    sACK = rACK
                    print("receive index :", rACK)
                    print("data sending now:")
                    print("######################\n")
                    i += 1
                    break
            except socket.timeout:
                print("Lost ACK, Send same data again.\n")
                continue
            # print((checksum_bytes)[35:41])
            

        time.sleep(0.1)

    md5_hash = check_md5(file_name)
    s.sendto(md5_hash.encode('utf-8'), client_addr)

if __name__ == "__main__":
    try:
        data, (client_ip, client_port) = s.recvfrom(4096)
        client_addr = (client_ip,client_port)
    except ConnectionResetError:
        print("error. port number not matching.")
        sys.exit()

    text = data.decode('utf8')
    handler = text.split()

    if handler[0] == '201602070':
        sender_send("speech_script.txt")
