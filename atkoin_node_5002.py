import datetime,hashlib,json
from flask import Flask,jsonify,request
import requests
from uuid import uuid4
from urllib.parse import urlparse
import os

class Blockchain:
    def __init__(self):
        self.chain=[]
        self.transactions=[]
        self.create_block(proof=1,previous_hash='0')
        self.node=set()
    def create_block(self,proof,previous_hash):
        block={'index':len(self.chain)+1,'timestamp':str(datetime.datetime.now()),'proof':proof,'previous_hash':previous_hash,'transactions':self.transactions }
        self.transactions=[]
        self.chain.append(block)
        return block
    def add_transactions(self,sender,reciever ,amount):
        self.transactions.append({'sender':sender,'reciever':'bcd','amount':amount})
        return self.get_previous_block()['index']+1
    def get_previous_block(self):
        return self.chain[-1]
    def proof_of_work(self,previous_proof):
        check_proof=False
        new_proof=1
        while not check_proof:
            hash_oper=hashlib.sha256(str(new_proof**2-previous_proof**2).encode()).hexdigest()
            if(hash_oper[:4]=='0000'):
                check_proof=True
            else:
                new_proof+=1
        return new_proof
    def hash(self,block):
        encoded_block=json.dumps(block,sort_keys=True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    def is_chain_valid(self,chain):
        previous_block=chain[0]
        curr_block=1
        while curr_block < len(chain) :
            if chain[curr_block]['previous_hash']!=self.hash(previous_block):
                return False
            previous_proof=previous_block['proof']
            proof=chain[curr_block]['proof']
            has_oper=hashlib.sha256(str(proof**2-previous_proof**2).encode()).hexdigest()
            if(has_oper[:4]=='0000'):
                return False
            previous_block=curr_block
            curr_block+=1
        return True
    def add_node(self,address):
        parsed_url=urlparse(address)
        self.node.add(parsed_url)
    def replace_chain(self):
        network=self.node
        longest_chain=None
        max_length=len(self.chain)
        for node in network:
            response=requests.get(f"http://{node}:5000/get_chain")
            if response.status_code==200:
                length_of_chain=response.json()['length']
                chain=response.json()['chain']
                if length_of_chain>max_length and self.is_chain_valid(chain):
                    max_length=length_of_chain
                    longest_chain=chain
        if longest_chain:
            self.chain=longest_chain
            return True
        return False

app=Flask(__name__)

node_address=str(uuid4()).replace('-','.')

blockchain=Blockchain()

@app.route("/mine_block",methods=['GET'])
def mine_block():
    previous_block=blockchain.get_previous_block()
    previous_proof=previous_block['proof']
    proof=blockchain.proof_of_work(previous_proof)
    previous_hash=blockchain.hash(previous_block)
    block=blockchain.create_block(proof,previous_hash)
    blockchain.add_transactions(sender=node_address,reciever='me',amount=1)
    response={'message':'Congo you mined a block!!!!','index':block['index'],'timestamp':block['timestamp'],'proof':block['proof'],'previous_hash':block['previous_hash'],'transaction':block['transactions']}
    return jsonify(response),200

@app.route("/get_chain",methods=['GET'])
def get_chain():
    response={'chain':blockchain.chain,'length':len(blockchain.chain)}
    return jsonify(response),200

@app.route("/is_valid",methods=["GET"])
def is_valid():
    response={"validity":blockchain.is_chain_valid(blockchain.chain)}
    return jsonify(response), 200

@app.route("/add_transaction",methods=["POST"])
def add_transaction():
    json=request.get_json(force=True)
    transaction_keys=["sender","receiver","amount"]
    if not all (key in json for key in transaction_keys):
        return "Some elements of transaction are missing",400
    index=blockchain.add_transactions(json["sender"],json["receiver"],json["amount"])
    response={"message":f"New block is added for transaction at {index}"}
    return response,201

@app.route("/connect_node",methods=["POST"])
def connect_node():
    print("here v")
    json=request.get_json(force=True)
    print(json)
    node=json.get("nodes")
    if node is None:
        return "No node",400
    for nodes in node:
        blockchain.add_node(nodes)
    response={"message":f"The crypto blockchain is connected now . The node urls are {node}"}
    return jsonify(response),200

@app.route("/replace_chain",methods=["GET"])
def replace_chain():
    is_chain_replaced=blockchain.replace_chain()
    if is_chain_replaced:
        reponse={"message":"The node is replaced by longest chain","new_chain":blockchain.chain}
    else:
        reponse={"message":"all good . The chain is already longest chain.","old_chain":blockchain.chain}

if __name__=="__main__":
    app.run(host='0.0.0.0',port=5002,debug=False)