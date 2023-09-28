import struct
from socket import socket


class MySocket(socket):

    def recv_msg(self):
        raw_msglen = self.recvall(4)
        if not raw_msglen:
            return None
        msglen = struct.unpack('>I', raw_msglen)[0]
        return self.recvall(msglen)

    def recvall(self, n):
        data = b''
        while len(data) < n:
            packet = self.recv(n - len(data))
            if not packet:
                return None
            data += packet
        return data
