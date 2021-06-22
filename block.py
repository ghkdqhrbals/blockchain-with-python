from datetime import datetime
import hashlib
import node
import transaction
import random
import numpy as np

nodeLength = 5
NodeAddresses = []


class Block:
    def __init__(self, prevBlockHash):
        self.prevBlockHash = prevBlockHash  # 이전 블록 해쉬
        self.minerNodeId = ""  # 블록 생성자
        self.transactions = []  # Transaction Pool에서 Transactions를 수집
        self.timestamp = ""  # 블록 타임스탬프
        self.hash = ""  # 현재 블록 해쉬

    def setBlockHashAndMiner(self, currentMiner, transactions):
        self.transactions = transactions  # 트랜잭션을 블록에 담음
        self.minerNodeId = currentMiner
        print("Transactions :", transactions)
        blockString = self.getBlockStringWithMiner()  #
        blockHash = hashlib.sha256(blockString).hexdigest()  # 해시화
        self.hash = blockHash

    def getBlockMiner(self):
        return self.minerNodeId

    def proofOfDraw(self, _bootstrap):
        blockHashes = {}  # 각 노드가 가지는 현재 해시값
        peerList = _bootstrap.getPeerlist()
        miner_address = []
        for peer_address, peer_state in peerList.items():
            if peer_state[0]:  # Miner라면 마이너 address에 추가, state의 첫번째는 miner or user 할당
                miner_address.append(peer_address)
        for node_addr in miner_address:  # 현재 참여한 마이너 노드만큼 반복
            blockString = self.getBlockString(node_addr)  # 이전 블록 + 노드 주소 + 타임스탬프
            blockHash = hashlib.sha256(blockString).hexdigest()  # 해시화
            print("Node", node_addr, "current hash =", blockHash)
            blockHashes[node_addr] = blockHash

        currentMiner = max(blockHashes, key=blockHashes.get)  # 가장 높은 해시값을 가지는 노드를 마이너로 설정
        maxHash = blockHashes[currentMiner]  # 모든 해시값중 가장 높은 해시값 선택
        print("Maximum Hash is", maxHash)
        print("Current Block Miner is", currentMiner)

        return currentMiner  # 선택된 마이너 반환

    def getBlockString(self, nodeId):
        pb = str(self.prevBlockHash)
        return (pb + str(nodeId)).encode()

    def getBlockStringWithMiner(self):
        self.timestamp = datetime.now()
        pb = str(self.prevBlockHash)
        ts = str(self.timestamp)
        tx = str(self.transactions)
        miner = str(self.minerNodeId)
        return (pb + miner + tx + ts).encode()

    def BFT_consensus(self, _bootstrap):
        gs = _bootstrap.getPeerlist()  # global state 가져오기
        miner_list = list([[addr, state[1]] for addr, state in gs.items() if state[0] == 1])
        print(miner_list)
        total_energy, agree = 0, 0

        for miner in miner_list: # 모든 마이너를 순회하면서
            total_energy += miner[1] # 전체 에너지에 마이너 에너지 추가
            behavior = np.random.choice([True, False], p=[0.8, 0.2])
            if behavior:
                agree += miner[1] # 90% 확률로 마이너가 동의한다면 마이너 에너지 추가
        agree_ratio = float(agree) / float(total_energy)
        if agree_ratio >= float(2/3):
            print("BFT Consensus is Successful")
            print("Total Miner Energy(REC) :",total_energy)
            print("Agreed Miner Energy(REC) :",agree)
            print("Agree ratio is",agree_ratio)
            return True
        else:
            print("BFT Consensus is Failed")
            print("Total Miner Energy(REC) :", total_energy)
            print("Agreed Miner Energy(REC) :", agree)
            print("Agree ratio is", agree_ratio)
            return False

            # Miner라면 합의에 참여가능


class BlockChain:
    def __init__(self):
        self.currentHeight = 0
        self.currentBlockHash = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        self.blockList = []

    def createGenesisBlock(self, bootstrap):
        byte = self.currentBlockHash
        genesisBlock = Block(byte)
        # currentMiner = genesisBlock.proofOfDraw()
        currentMiner = genesisBlock.proofOfDraw(bootstrap)
        genesisBlock.setBlockHashAndMiner(currentMiner, genesisBlock.transactions)  # 제네시스 블록에 마이너랑 블록해쉬 값 삽입

        return genesisBlock

    def attachAndFinalizeBlock(self, block):
        self.currentBlockHash = block.hash
        self.currentHeight += 1
        self.blockList.append(block)

    def createNewBlock(self, transactions):
        block = Block(self.currentBlockHash)  # previous block hash에 현재 블록 해시 집어넣은채로 생성

        currentMiner = block.proofOfDraw(bootstrap)  # 합의 수행, 블록 생성자 결정
        block.setBlockHashAndMiner(currentMiner, transactions)  # 블록 생성자가 트랜잭션과 함께 블록 생성
        print(block.minerNodeId)
        return block

    def getPubkey(self):
        return self.currentBlockHash
    # def newBlock(self):


if __name__ == '__main__':
    bc = BlockChain()
    TxPool = transaction.TransactionPool()  # TxPool 생성
    bootstrap = node.Network()  # 초기 사용자 노드에게 현재 네트워크 참여 노드 리스트를 전송해주는 bootstrap node

    nodeA = node.Node(bootstrap.Td, bootstrap, 100, 150, 1)  # 노드A 생성
    nodeA.sendConnectMsg()  # 노드A가 bootstrap에 노드리스트 메세지 전송
    bootstrap.addNode(nodeA)  # 부트노드에 노드A 추가 및 노드A에게 전체 노드리스트 반환
    print("\n현재 메인 네트워크 참가자 크기:" + str(bootstrap.getSize()))

    nodeB = node.Node(bootstrap.Td, bootstrap, 200, 250, 1)  # 노드B 생성
    nodeB.sendConnectMsg()  # 노드B가 bootstrap에 노드리스트 메세지 전송
    bootstrap.addNode(nodeB)  # 부트노드에 노드B 추가 및 노드B에게 전체 노드리스트 반환
    print("\n현재 메인 네트워크 참가자 크기:" + str(bootstrap.getSize()))

    print("Node A 출력 ------------")
    print(bootstrap.getPeerInfo(nodeA))  # 네트워크에서 nodeA정보 반환.
    print("Peer List 출력 ---------")
    print(bootstrap.getPeerlist())
    # print("nodeA -> nodeB로 Tx 전송")
    # TxPool.addTx(nodeA.sendTx(nodeB.getPubKey(), 50, 4.1, 0.04, 0, 0))  # TxPool에 Tx추가.

    # node.msgServer.getMSGprint(nodeB)  # nodeB가 받은 message 출력
    # node.msgServer.sendMSGprint(nodeB)  # nodeB가 전송한 message 출력

    print("모든 Node가 생성되었습니다.")
    print("제네시스 블록을 생성합니다.")

    gb = bc.createGenesisBlock(bootstrap)
    print("제네시스 블록 생성 완료 :", gb.hash)

    # BFT Consensus
    isSuccessful = gb.BFT_consensus(bootstrap)

    bc.attachAndFinalizeBlock(gb)
    print("제네시스 블록을 체인에 연결하였습니다.")
    print("현재 블록체인의 높이 : ", bc.currentHeight)
    print("--------------------------------------------------")
    a = 0
    while a < 5:
        print("트랜잭션을 입력해주세요")
        trans = ["123", "1245"]
        print("다음 블록 생성자를 결정합니다.")
        newBlock = bc.createNewBlock(trans)
        print("이전 블록 해시 :", newBlock.prevBlockHash)
        print("블록 생성 완료 :", newBlock.hash)

        # BFT Consensus
        newBlock.BFT_consensus(bootstrap)

        bc.attachAndFinalizeBlock(newBlock)
        print("블록을 체인에 연결하였습니다.")
        print("현재 블록체인의 높이 : ", bc.currentHeight)
        print("--------------------------------------------------")
        a += 1

    print(bc.blockList)
