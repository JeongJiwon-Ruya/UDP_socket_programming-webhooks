import socket
import os
import sys
import hashlib

def check_md5_hash(path):
    f = open(path, 'rb')
    data = f.read()
    md5_hash = hashlib.md5(data).hexdigest()
    return md5_hash

def checksum(data):

    data_d = data.decode()[1:]
    checksum_input = data_d[36:40]
    data_payload = data_d[40:]
    head = data_d[:36]
    data_ = head + "0000" + data_payload
    data_ = data_.encode()

    tsum = ""
    for j in range(0,len(data),2):
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
    if checksum != checksum_input:
        print("Not matched")
        sys.exit()
    else:
        print("checksum matched")
        print(checksum)


rec_argv = sys.argv
if len(rec_argv) > 3:
    print("over input")
    sys.exit()
ip_addr = rec_argv[1]
port_num = rec_argv[2]

try:
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    s.setblocking(0)
    s.settimeout(10)

except socket.error:
    print("failed to create socket")
    sys.exit()

zero = "0"
one = "1"
nak = "NAK"

msg_to_send = input("receive socket created\nenter your student number:\n")
s.sendto(msg_to_send.encode(), (ip_addr, int(port_num))) 
msg_cmd, addr = s.recvfrom(4096)##
print(msg_cmd.decode())
msg_fileExist, addr = s.recvfrom(4096)###
print(msg_fileExist.decode())

newfile = "copy_"+msg_to_send.split()[0]

write_file = open(os.getcwd()+"/"+newfile,'wb')
msg_size, addr = s.recvfrom(4096)####
# checksum(msg_size)
# msg_size = int((msg_size.decode())[41:])
msg_size = int(msg_size.decode())

i = 1
pastRecv = ""
test_2 = False # for ERROR 2

while i <= msg_size:
    try:
        chunk_file, addr = s.recvfrom(4096)


        print("#############################")
        print("Received frame number:", i)
        # checksum(chunk_file)

        recvACK = chunk_file.decode()[0:1]
        if pastRecv != chunk_file :
            write_file.write(chunk_file[1:])
        else :
            i -=1
            print(" Send ACK only ")
 
        if i == 8 and test_2:
            test_2 = False
            s.sendto(one.encode(), (ip_addr, 8008))
        elif recvACK == zero :
            print("receive index :", recvACK)
            s.sendto(one.encode(), (ip_addr, int(port_num)))
            print("sending index :", one)
        elif recvACK == one :
            print("receive index :", recvACK)
            s.sendto(zero.encode(), (ip_addr, int(port_num)))
            print("sending index :", zero)
        
        print("#############################\n")
        i += 1
        pastRecv = chunk_file

    except socket.timeout:
        print("====+++SEND NAK+++====\n")
        s.sendto(nak.encode(), (ip_addr, int(port_num)))

write_file.close()

# Do not modify the code (below)
rec_md5_hash, addr = s.recvfrom(4096)
		
if rec_md5_hash.decode('utf8') == check_md5_hash(newfile): # 
    print("True")
else:
    print("False")
