import socket

HOST = '188.120.248.147'
PORT = 9999

with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    
    print('Connecting...')
    s.connect((HOST, PORT))
    
    msg = b''
    
    print('Sending')
    s.sendall(msg)
    
    res = s.recv(1024)
    print(res.decode('utf-8'))

print('Closed connection')
