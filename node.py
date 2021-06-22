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

    # value 반환
    def getPeerInfo(self, node):
        return self.peerlist[node.ID]


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
            # self.pub_key_str = self.pub_key_str.replace('+','').replace('/','')
            # print(self.pub_key_str)
            self.ID = hashlib.sha256(self.pub_key_str.encode('utf-8')).hexdigest()[:16]
            print("ID : " + self.ID)

        with open("public" + str(self.number) + ".pem", 'rb+') as f:
            self.pub_key = crypto.load_publickey(crypto.FILETYPE_PEM, f.read())

            # print(crypto.b16encode(bytes(str(self.pub_key),encoding='utf-8')).decode())
            # print(bytes(str(self.pub_key),encoding='utf-8'))
            # self.pub_key = crypto.load_publickey(crypto.FILETYPE_PEM, f.read())

    def getID(self):
        return self.ID

    def getPubKey(self):
        return self.pub_key

    def sign1(self,To,Energy,Money,GasPrice):
        with open("private"+str(self.number)+".pem", 'rb+') as f:
            self.priv_key = crypto.load_privatekey(crypto.FILETYPE_PEM, f.read())
        with open("public" + str(self.number) + ".pem", 'rb+') as f:
            self.pub_key = crypto.load_publickey(crypto.FILETYPE_PEM, f.read())

        rlp = str(self.pub_key) + str(To) + str(Energy) + str(Money) + str(GasPrice)
        hash = SHA.new(rlp.encode('utf-8')).digest()
        sig1 = sign(self.priv_key, hash, 'sha256')

        x509 = X509()
        x509.set_pubkey(self.pub_key)
        Tx = Transaction(self.ID, To, Energy, Money, GasPrice, sig1, b'0', x509,b'0')
        print("sign 1")
        return Tx
      
    def sign2(self,To,Energy,Money,GasPrice,sig1,x509_1):
        with open("private"+str(self.number)+".pem", 'rb+') as f:
            self.priv_key = crypto.load_privatekey(crypto.FILETYPE_PEM, f.read())
        with open("public"+str(self.number)+".pem", 'rb+') as f:
            self.pub_key = crypto.load_publickey(crypto.FILETYPE_PEM, f.read())

        rlp = str(self.pub_key)+str(To)+str(Energy)+str(Money)+str(GasPrice)+str(sig1)
        hash = SHA.new(rlp.encode('utf-8')).digest()
        sig2 = sign(self.priv_key,hash,'sha256')

        x509 = X509()
        x509.set_pubkey(self.pub_key)
        Tx = Transaction(self.ID,To,Energy,Money,GasPrice,sig1,sig2,x509_1,x509)
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
    def getMSGprint(self,node1):
        print("-----getMSG start-------")
        for i in self.dicts:
            if str(node1.ID) == str(i[1]):
                # 밑에 수정 필요
                print("[ME:"+str(node1.ID)+"] [MSG:"+str(i[2]) + "] [FROM:"+ str(i[0])+"]")
        print("-----getMSG end-------")

    def sendMSGprint(self, node1):
        print("-----sendMSG start-------")
        for i in self.dicts:
            if str(node1.ID) == str(i[0]):
                # 밑에 수정 필요
                print("[ME:"+str(node1.ID)+"] [MSG:"+str(i[2]) + "] [TO:"+ str(i[1])+"]")
        print("-----getMSG end-------")


msgServer = MSG()

if __name__ == '__main__':
    TxPool = TransactionPool()  # TxPool 생성
    bootstrap = Network()  # 초기 사용자 노드에게 현재 네트워크 참여 노드 리스트를 전송해주는 bootstrap node

    nodeA = Node(bootstrap.Td, bootstrap, 100, 150, 1)  # 노드A 생성
    nodeA.sendConnectMsg()  # 노드A가 bootstrap에 노드리스트 메세지 전송
    bootstrap.addNode(nodeA)  # 부트노드에 노드A 추가 및 노드A에게 전체 노드리스트 반환
    print("현재 메인 네트워크 참가자 크기:" + str(bootstrap.getSize())+"\n")

    nodeB = Node(bootstrap.Td, bootstrap,200,250,1)  # 노드B 생성
    nodeB.sendConnectMsg() # 노드B가 bootstrap에 노드리스트 메세지 전송
    bootstrap.addNode(nodeB) # 부트노드에 노드B 추가 및 노드B에게 전체 노드리스트 반환
    print("현재 메인 네트워크 참가자 크기:" + str(bootstrap.getSize())+"\n")

    nodeC = Node(bootstrap.Td, bootstrap, 500, 1000, 1)  # 노드B 생성
    nodeC.sendConnectMsg()  # 노드B가 bootstrap에 노드리스트 메세지 전송
    bootstrap.addNode(nodeC)  # 부트노드에 노드B 추가 및 노드B에게 전체 노드리스트 반환
    print("현재 메인 네트워크 참가자 크기:" + str(bootstrap.getSize())+"\n")

    #msgServer.getMSGprint(nodeB)  # nodeB가 받은 message 출력
    #msgServer.sendMSGprint(nodeB)  # nodeB가 전송한 message 출력

    #msgServer.getMSGprint(nodeA)  # nodeB가 받은 message 출력
    #msgServer.sendMSGprint(nodeA)  # nodeB가 전송한 message 출력

    print(bootstrap.getPeerInfo(nodeA))  # 네트워크에서 nodeA정보 반환.

    print("\'nodeA가 nodeB에게 50 에너지를 4.1원에 살것이다\' Transaction 전송")
    TxPool.addTx(nodeA.sign1(nodeB.getID(), 50, 4.1, 0.04)) # TxPool에 Tx추가.

    print("TxPool내에 있는 모든 Transaction PRINT 개수:"+str(TxPool.getSize()))
    TxPool.printAll()

    ToB = TxPool.getMyTransaction(nodeB)[0].getInfo() # B는 자기에게 온 Transaction의 첫번째 Tx를 확인

    print("nodeB는 Transaction 확인 후, 재서명하여 TxPool에 올림.")
    TxPool.addTx(nodeB.sign2(ToB[1],ToB[2],ToB[3],ToB[4],ToB[5],ToB[7]))
    TxPool.printAll()
