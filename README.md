# Blockchain for RE100(Renewable Energy)

## Difference between original contract and ours
### 기존 에너지 거래 방식 한계점
<img width="235" alt="image" src="https://user-images.githubusercontent.com/29156882/180703319-d5028fa5-620d-4cc8-b5ba-3460b7748c48.png">

> * 한국 전력 공사의 계약 독점   
> * 계약 무결성 침해 위험 존재   
> * 계약 수수료 발생   
> * 수동화 계약으로 인한 비효율성

### 제안하는 에너지 거래 블록체인 플랫폼
<img width="275" alt="image" src="https://user-images.githubusercontent.com/29156882/180703530-2b2ef1a8-5539-44cb-b0b0-a2c015432350.png">

> * 지속적으로 변하는 블록 채굴자에게 계약 위임   
> * 계약 무결성 보존   
> * 채굴자에게 계약 수수료 지급   
> * 자동화 계약으로 인한 효율성   


1. Not signed by Supplier : 트랜잭셔 전송

| FROM(ID) | ENERGY | MONEY | TO(ID) |   signature1   | signature2 | Fee |
|:--------:|:------:|:-----:|:------:|:--------------:|:----------:|:---:|
|    Amy   |   50   |  41$  |   M1   |  Sig(Amy, Tx1) |    NULL    |  5% |
|    Bob   |   30   |  22$  |   M3   |  Sig(Bob, Tx2) |    NULL    |  7% |
|   Chen   |   20   |  56$  |   M2   | Sig(Chen, Tx3) |    NULL    |  3% |
|    ...   |   ...  |  ...  |   ...  |        …       |      …     |  …  |

2. Signed by Supplier : 서명 후 트랜잭션에 담기

| FROM(ID) | ENERGY | MONEY | TO(ID) |   signature1   |      signature2      | Fee |
|:--------:|:------:|:-----:|:------:|:--------------:|:--------------------:|:---:|
|    Amy   |   50   |  41$  |   M1   |  Sig(Amy, Tx1) | Sig(M1,Sig(Amy,Tx1)) |  5% |
|    Bob   |   30   |  22$  |   M3   |  Sig(Bob, Tx2) | Sig(M2,Sig(Bob,Tx2)) |  7% |
|   Chen   |   20   |  56$  |   M2   | Sig(Chen, Tx3) |         NULL         |  3% |
|    ...   |   ...  |  ...  |   ...  |        …       |           …          |  …  |

## 2-stage consensus algorithm

* 블록 생성자 결정

**𝑀𝑖𝑛𝑒𝑟=𝑀𝑎𝑥_𝐴𝑑𝑑𝑟 (ℎ𝑎𝑠ℎ(𝑃𝑟𝑒𝑣𝐵𝑙𝑜𝑐𝑘𝐻𝑎𝑠ℎ,𝐴𝑑𝑑𝑟)**

* 블록 완결

**∑(0<𝑖<𝑑)𝑅𝐸100_𝑖^𝑎𝑔𝑟𝑒𝑒 ≥2/3 𝑅𝐸100_𝑡𝑜𝑡𝑎𝑙**

## Prototype demonstration
<img width="458" alt="image" src="https://user-images.githubusercontent.com/29156882/180705339-95bc6f2c-a0dc-44ca-96aa-9ec211503922.png">
<img width="671" alt="image" src="https://user-images.githubusercontent.com/29156882/180705357-c2a9a814-997d-4b09-a05f-e2ce1420a877.png">
<img width="682" alt="image" src="https://user-images.githubusercontent.com/29156882/180705371-aa0efdca-0f70-4090-8fa6-08239c6b5c47.png">
<img width="522" alt="image" src="https://user-images.githubusercontent.com/29156882/180705410-af841973-2bff-4fc3-ae67-97d41bc1da99.png">
<img width="674" alt="image" src="https://user-images.githubusercontent.com/29156882/180705428-6d8f2714-a39c-445e-b732-2f6c6d16fc32.png">










