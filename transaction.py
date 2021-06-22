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
    def printTx(self,nodeID):
        for tx in self.Txlist:
            if nodeID == tx.From:
                print(tx)

class Transaction:
    def __init__(self, From, To, Energy, Money, GasPrice, sig1, sig2,x509):
        rlp = str(From) + str(To) + str(Energy) + str(Money) + str(GasPrice) + str(sig1)+str(sig2)+str(x509)
        self.TxID = SHA.new(rlp.encode('utf-8')).hexdigest()
        self.From = From
        self.To = To
        self.Energy = Energy
        self.Money = Money
        self.GasPrice = GasPrice
        self.sig1 = sig1
        self.sig2 = sig2
    def __str__(self):
        return "------ TxID: "+self.TxID+" ------\nFrom: "+str(self.From)+"\nTo: "+str(self.To)+"\nEnergy: "+str(self.Energy)+"\nMoney: "+str(self.Money)+"\nGasPrice: "+str(self.GasPrice)+"\nsig1: "+str(crypto.b16encode(self.sig1).decode()[0:32])+"\nsig2: "+str(self.sig2)+"\n-------------------------------------------------------------"
    def getFrom(self):
        return self.From
    def getTxID(self):
        return self.TxID
    #add to Pool
    def sendTx(self):
        return
    def printTx(self):
        print('new')

