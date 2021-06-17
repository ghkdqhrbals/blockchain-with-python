import hashlib
from OpenSSL import crypto

class TransactionPool:
    def __init__(self):
        self.Txlist=[]
        return
    def addTx(self,Tx):
        self.Txlist.append(Tx)
    def removeTx(self,Tx):
        self.Txlist.remove(Tx)
    def getSize(self):
        return len(self.Txlist)

class Transaction:
    def __init__(self, From, To, Energy, Money, GasPrice, sig1, sig2,x509):
        print('init Transaction')
        self.From = From
        self.To = To
        self.Energy = Energy
        self.Money = Money
        self.GasPrice = GasPrice
        self.sig1 = sig1
        self.sig2 = sig2
        print("From:"+str(From))
        print("To:"+str(To))
        print("Energy:"+str(Energy))
        print("Money:"+str(Money))
        print("GasPrice:"+str(GasPrice))
        # 너무 길어서 16 bytes 까지만 표시
        print("sig1:"+crypto.b16encode(sig1).decode()[0:16])
        print("sig2:"+str(sig2))
    #add to Pool
    def sendTx(self):
        return
    def printTx(self):
        print('new')

