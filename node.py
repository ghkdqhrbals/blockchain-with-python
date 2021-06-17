import hashlib

import OpenSSL.crypto
from Crypto.PublicKey import RSA
from transaction import Transaction
from transaction import TransactionPool
from OpenSSL.crypto import load_privatekey, FILETYPE_PEM, sign, load_publickey, verify, X509
from Crypto.Hash import SHA256 as SHA
from OpenSSL import crypto


class Network:
    def __init__(self):
        self.Td = 0
        self.peerlist = []
        return
    def getTd(self):
        return self.Td
    def getSize(self):
        return len(self.peerlist)
    def addNode(self,address):
        self.Td += 1
        self.peerlist.append(address)
    def removeNode(self,address):
        self.peerlist.remove(address)
    def getPeerlist(self):
        return self.peerlist

class Node:
    # KEY 생성 및 노드 생성.
    def __init__(self,nodeID,network):
        self.peerlistm = network.getPeerlist()
        self.nodeID = nodeID
        self.isMinor = False
        self.pub_key = ""
        pkey = crypto.PKey()
        pkey.generate_key(crypto.TYPE_RSA, 1024)
        print("RSA KEY 생성완료")
        with open("public"+str(nodeID)+".pem", 'ab+') as f:
            f.write(crypto.dump_publickey(crypto.FILETYPE_PEM, pkey))
        with open("private"+str(nodeID)+".pem", 'ab+') as f:
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey))
        with open("public"+str(self.nodeID)+".pem", 'rb+') as f:
            self.pub_key = crypto.load_publickey(crypto.FILETYPE_PEM, f.read())
            #print(crypto.b16encode(self.pub_key))
    def getPubKey(self):
        return self.pub_key
    def sendTx(self,To,Energy,Money,GasPrice,sig1,sig2):
        with open("private"+str(self.nodeID)+".pem", 'rb+') as f:
            self.priv_key = crypto.load_privatekey(crypto.FILETYPE_PEM, f.read())
        with open("public"+str(self.nodeID)+".pem", 'rb+') as f:
            self.pub_key = crypto.load_publickey(crypto.FILETYPE_PEM, f.read())
        print("a ",self.pub_key.to_cryptography_key())

        rlp = str(self.pub_key)+str(To)+str(Energy)+str(Money)+str(GasPrice)+str(sig1)
        hash = SHA.new(rlp.encode('utf-8')).digest()
        sig = sign(self.priv_key,hash,'sha256')

        x509 = X509()
        x509.set_pubkey(self.pub_key)

        Tx = Transaction(self.nodeID,To,Energy,Money,GasPrice,sig,sig2,x509)
        print("send transaction")
        return Tx
    def sendConnectMsg(self):
        for i in self.peerlistm:
            msgServer.sendConnectMsg(self.nodeID,i)
        return
class MSG():
    def __init__(self):
        self.dicts = []
        return
    def sendConnectMsg(self, node1, node2):
        temp = [node1,node2,'ConnectMsg']
        self.dicts.append(temp)
    def getMSGprint(self,node1):
        for i in self.dicts:
            if str(node1.nodeID) == str(i[1]):
                print(str(node1)+" MSG : "+str(i[2]) + " FROM : "+ str(i[0]))
    def sendMSGprint(self, node1):
        for i in self.dicts:
            if str(node1.nodeID) == str(i[0]):
                print(str(node1) + " MSG : " + str(i[2]) + " To : " + str(i[1]))

msgServer=MSG()

if __name__ == '__main__':                 
    TxPool = TransactionPool()
    bootstrap = Network()
    print("nodeA 생성")
    nodeA = Node(bootstrap.Td,bootstrap)
    bootstrap.addNode(nodeA)
    print("nodeB 생성")
    nodeB = Node(bootstrap.Td,bootstrap)
    bootstrap.addNode(nodeA)
    print("\n현재 메인 네트워크 참가자 크기:" + str(bootstrap.getSize()))

    print("nodeA -> nodeB로 Tx 전송")
    nodeA.sendConnectMsg()
    TxPool.addTx(nodeA.sendTx(nodeB.getPubKey(),50,4.1,0.04,0,0))
    msgServer.getMSGprint(nodeB)
    msgServer.sendMSGprint(nodeB)