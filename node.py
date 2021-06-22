import hashlib

import OpenSSL.crypto
from Crypto.PublicKey import RSA
from transaction import Transaction, TransactionPool
from OpenSSL.crypto import load_privatekey, FILETYPE_PEM, sign, load_publickey, verify, X509
from Crypto.Hash import SHA256 as SHA
from OpenSSL import crypto


class Network:
    def __init__(self):
        self.Td = 0
        self.peerlist = {}
        return

    def getTd(self):
        return self.Td

    def getSize(self):
        return len(self.peerlist)

    def addNode(self, node):
        self.Td += 1
        self.peerlist[node.ID] = [node.state, node.Energy, node.Money, node.pub_key]

    def removeNode(self, node):
        del self.peerlist[node]

    # dict 반환
    def getPeerlist(self):
        return self.peerlist

    def getNode(self, nodeID):
        return self.peerlist[nodeID]

    # value 반환
    def getPeerInfo(self, node):
        return self.peerlist[node.ID]

    # state 1: energy +
    # state 2: money +
    def supply(self, node, state, N):
        templist = []
        if state == 1:
            tempEnergy = self.peerlist[node.ID][1] + N
            templist = [node.state, tempEnergy, node.Money, node.pub_key]
        if state == 2:
            tempMoney = self.peerlist[node.ID][1] + N
            templist = [node.state, node.Energy, tempMoney, node.pub_key]
        self.peerlist[node.ID] = templist

    def change_currency(self, node, energy, money, address):
        templist = [node[0], energy, money, node[3]]
        print(templist)
        self.peerlist[address] = templist
        return self

    def change_currency_for_gas_price(self, node, money, address):
        templist = [node[0], node[1], node[2] + money, node[3]]
        print(templist)

        self.peerlist[address] = templist
        return self


class NodeList:
    def __init__(self):
        self.nodes = []

    def addNode(self, node):
        self.nodes.append(node)


class Node:
    # KEY 생성 및 노드 생성.
    def __init__(self, number, network, Energy, Money, state):
        # print("현재 네트워크 피어 개수 : ",network.getSize())
        self.state = state  # user : 0, minor : 1
        self.Energy = Energy
        self.Money = Money
        self.peerlistm = network.getPeerlist()
        self.number = number
        self.isMinor = False
        self.pub_key = ""
        self.pub_key_str = ""
        self.ID = ""
        pkey = crypto.PKey()
        pkey.generate_key(crypto.TYPE_RSA, 1024 + number)
        print("RSA KEY 생성완료")
        with open("public" + str(number) + ".pem", 'ab+') as f:
            f.write(crypto.dump_publickey(crypto.FILETYPE_PEM, pkey))
        with open("private" + str(number) + ".pem", 'ab+') as f:
            f.write(crypto.dump_privatekey(crypto.FILETYPE_PEM, pkey))
        with open("public" + str(self.number) + ".pem", 'rb+') as f:
            for i in f.readlines():
                j = str(i)
                if '---' in j:
                    continue
                j.replace('\n', '')
                j = j[2:len(j) - 3]
                self.pub_key_str += j
            self.ID = hashlib.sha256(self.pub_key_str.encode('utf-8')).hexdigest()[:16]
            print("ID : " + self.ID)

        with open("public" + str(self.number) + ".pem", 'rb+') as f:
            self.pub_key = crypto.load_publickey(crypto.FILETYPE_PEM, f.read())

    def __str__(self):
        return "Node : " + str(self.ID) + ", Money : " + str(self.Money) + ", Energy : " + str(self.Energy) + ", State : "+str(self.state)

    def change_currency_node(self, node):
        self.Energy = node[1]
        self.Money = node[2]
        return self

    # state 1: energy +
    # state 2: money +
    def supply(self, state, N):
        if state == 1:
            self.Energy += N
        if state == 2:
            self.Money += N

    def getID(self):
        return self.ID

    def getPubKey(self):
        return self.pub_key

    def sign1(self, To, Energy, Money, GasPrice):
        with open("private" + str(self.number) + ".pem", 'rb+') as f:
            self.priv_key = crypto.load_privatekey(crypto.FILETYPE_PEM, f.read())
        with open("public" + str(self.number) + ".pem", 'rb+') as f:
            self.pub_key = crypto.load_publickey(crypto.FILETYPE_PEM, f.read())

        rlp = str(self.ID) + str(To) + str(Energy) + str(Money) + str(GasPrice)
        hash = SHA.new(rlp.encode('utf-8')).digest()
        sig1 = sign(self.priv_key, hash, 'sha256')

        x509 = X509()
        x509.set_pubkey(self.pub_key)
        Tx = Transaction(self.ID, To, Energy, Money, GasPrice, sig1, b'0', x509, b'0')
        print("sign 1")
        return Tx

    def sign2(self, From, To, Energy, Money, GasPrice, sig1, x509_1):
        with open("private" + str(self.number) + ".pem", 'rb+') as f:
            self.priv_key = crypto.load_privatekey(crypto.FILETYPE_PEM, f.read())
        with open("public" + str(self.number) + ".pem", 'rb+') as f:
            self.pub_key = crypto.load_publickey(crypto.FILETYPE_PEM, f.read())

        rlp = str(From) + str(To) + str(Energy) + str(Money) + str(GasPrice) + str(sig1)
        hash = SHA.new(rlp.encode('utf-8')).digest()
        sig2 = sign(self.priv_key, hash, 'sha256')

        x509 = X509()
        x509.set_pubkey(self.pub_key)
        Tx = Transaction(From, To, Energy, Money, GasPrice, sig1, sig2, x509_1, x509)
        print("sign 2")
        print(Tx)
        return Tx

    def sendConnectMsg(self):
        for i in self.peerlistm:
            msgServer.sendConnectMsg(self.ID, i)
        return


class MSG():
    def __init__(self):
        self.dicts = []
        return

    def sendConnectMsg(self, node1, node2):
        temp = [node1, node2, 'ConnectMsg']
        self.dicts.append(temp)

    # 내가 받은 메세지
    def getMSGprint(self, node1):
        print("-----getMSG start-------")
        for i in self.dicts:
            if str(node1.ID) == str(i[1]):
                # 밑에 수정 필요
                print("[ME:" + str(node1.ID) + "] [MSG:" + str(i[2]) + "] [FROM:" + str(i[0]) + "]")
        print("-----getMSG end-------")

    def sendMSGprint(self, node1):
        print("-----sendMSG start-------")
        for i in self.dicts:
            if str(node1.ID) == str(i[0]):
                # 밑에 수정 필요
                print("[ME:" + str(node1.ID) + "] [MSG:" + str(i[2]) + "] [TO:" + str(i[1]) + "]")
        print("-----getMSG end-------")


msgServer = MSG()
