import socket
import struct


def answer(packet: bytes, address: tuple[str, int], ip: str) -> None:
    transaction_id = packet[:2]
    question_end = packet.find(b"\0", 12) + 5
    response = transaction_id + b"\x81\x80\x00\x01\x00\x01\x00\x00\x00\x00"
    response += packet[12:question_end]
    response += b"\xc0\x0c" + struct.pack("!HHIH", 1, 1, 1, 4) + socket.inet_aton(ip)
    server.sendto(response, address)


server = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server.bind(("0.0.0.0", 5353))
count = 0
while True:
    packet, address = server.recvfrom(512)
    count += 1
    answer(packet, address, "192.0.2.1" if count % 2 else "127.0.0.1")
