import socket

ip_addr = "34.64.165.24"
port = "5001"
print("Connect Success")
client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)


message = input(">>> ")
client_socket.sendto(message.encode('utf-8'), (ip_addr, int(port)))
data, addr = client_socket.recvfrom(2000)
print(addr[0], ":", data.decode('ascii'))
