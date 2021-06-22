import hashlib

from Crypto.Hash import SHA
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
    def printAll(self):
        for tx in self.Txlist:
            print(tx)
        print("끝")
    def printTx(self,nodeID):
        for tx in self.Txlist:
            if nodeID == tx.TxID:
                print(tx)
    def getMyTransaction(self,node): # 나한테 다른 사람이 보낸 Transaction 확인
        lists = []
        for tx in self.Txlist:
            if node.ID == tx.To:
                print(tx)
                lists.append(tx)
        #print(lists)
        return lists
class Transaction:
    def __init__(self, From, To, Energy, Money, GasPrice, sig1, sig2,x509,x509_2):
        rlp = str(From) + str(To) + str(Energy) + str(Money) + str(GasPrice) + str(sig1)+str(sig2)+str(x509)+str(x509_2)
        self.TxID = SHA.new(rlp.encode('utf-8')).hexdigest()
        self.From = From
        self.To = To
        self.Energy = Energy
        self.Money = Money
        self.GasPrice = GasPrice
        self.sig1 = sig1
        self.sig2 = sig2
        self.x509 = x509
        self.x509_2 = x509_2
    def __str__(self):
        return "------ TxID: "+self.TxID+" ------\nFrom: "+str(self.From)+"\nTo: "+str(self.To)+"\nEnergy: "+str(self.Energy)+"\nMoney: "+str(self.Money)+"\nGasPrice: "+str(self.GasPrice)+"\nsig1: "+str(crypto.b16encode(self.sig1).decode()[0:32])+"\nsig2: "+str(crypto.b16encode(self.sig2).decode()[0:32])+"\n-------------------------------------------------------------"
    def getFrom(self):
        return self.From
    def getTxID(self):
        return self.TxID
    def getInfo(self):
        lists=[self.From,self.To,self.Energy,self.Money,self.GasPrice,self.sig1,self.sig2,self.x509,self.x509_2]
        return lists
    #add to Pool
    def sendTx(self):
        return
    def printTx(self,TxID):
        print('new')

