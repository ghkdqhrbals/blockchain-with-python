from datetime import datetime
import hashlib

nodeLength = 5
NodeAddresses = []

class Block:
    def __init__(self, prevBlockHash):
        self.prevBlockHash = prevBlockHash  # 이전 블록 해쉬
        self.minerNodeId = ""  # 블록 생성자
        self.transactions = []  # Transaction Pool에서 Transactions를 수집
        self.timestamp = datetime.now()  # 블록 타임스탬프
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

    def proofOfDraw(self):
        blockHashes = []  # 각 노드가 가지는 현재 해시값
        for node in range(0, nodeLength):  # 현재 참여한 마이너 노드만큼 반복
            blockString = self.getBlockString(node)  # 이전 블록 + 노드 주소 + 타임스탬프
            blockHash = hashlib.sha256(blockString).hexdigest()  # 해시화
            print("Node", node, "current hash =", blockHash)
            blockHashes.append(blockHash)

        maxHash = max(blockHashes)  # 모든 해시값중 가장 높은 해시값 선택
        currentMiner = blockHashes.index(maxHash)  # 가장 높은 해시값을 가지는 노드를 마이너로 설정
        print("Maximum Hash is", maxHash)
        print("Current Block Miner is", currentMiner)

        return currentMiner  # 선택된 마이너 반환

    def getBlockString(self, nodeId):
        pb = str(self.prevBlockHash)
        ts = str(self.timestamp)
        return (pb + str(nodeId) + ts).encode()

    def getBlockStringWithMiner(self):
        pb = str(self.prevBlockHash)
        ts = str(self.timestamp)
        tx = str(self.transactions)
        miner = str(self.minerNodeId)
        return (pb + miner + tx + ts).encode()


class BlockChain:
    def __init__(self):
        self.currentHeight = 0
        self.currentBlockHash = b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00'
        self.blockList = []

    def createGenesisBlock(self):
        byte = self.currentBlockHash
        genesisBlock = Block(byte)
        # currentMiner = genesisBlock.proofOfDraw()
        currentMiner = genesisBlock.proofOfDraw()
        genesisBlock.setBlockHashAndMiner(currentMiner, genesisBlock.transactions)  # 제네시스 블록에 마이너랑 블록해쉬 값 삽입

        return genesisBlock

    def attachAndFinalizeBlock(self, block):
        self.currentBlockHash = block.hash
        self.currentHeight += 1
        self.blockList.append(block)

    def createNewBlock(self, transactions):
        block = Block(self.currentBlockHash)  # previous block hash에 현재 블록 해시 집어넣은채로 생성

        currentMiner = block.proofOfDraw()  # 합의 수행, 블록 생성자 결정
        block.setBlockHashAndMiner(currentMiner, transactions)  # 블록 생성자가 트랜잭션과 함께 블록 생성
        print(block.minerNodeId)
        return block

    def getPubkey(self):
        return self.currentBlockHash
    # def newBlock(self):


if __name__ == '__main__':
    bc = BlockChain()
    gb = bc.createGenesisBlock()
    print("제네시스 블록 생성 완료 :", gb.hash)

    # BFT Consensus

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

        bc.attachAndFinalizeBlock(newBlock)
        print("블록을 체인에 연결하였습니다.")
        print("현재 블록체인의 높이 : ", bc.currentHeight)
        print("--------------------------------------------------")
        a += 1

    print(bc.blockList)
