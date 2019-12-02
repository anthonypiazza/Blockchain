# Paste your version of blockchain.py from the basic_block_gp
# folder here
# Take time to break down every line

# importing hashing, json, time, and unique ID
import hashlib
import json
from time import time
from uuid import uuid4

from flask import Flask, jsonify, request


class Blockchain(object):
    def __init__(self):
        self.chain = []
        self.current_transactions = []
        self.new_block(previous_hash=1, proof=100)

    def new_block(self, proof, previous_hash=None):
        block = {
            # TODO
            'index': len(self.chain)+1,
            'timestamp': time(),
            'transactions': self.current_transactions,
            'proof': proof,
            'previous_hash': previous_hash or self.hash(self.chain[-1]),
        }

        self.current_transactions = []
        self.chain.append(block)
        return block

    def hash(self, block):
        string_object = json.dumps(block, sort_keys=True)
        block_string = string_object.encode()
        raw_hash = hashlib.sha256(block_string)
        hex_hash = raw_hash.hexdigest()
        return hex_hash

    @property
    def last_block(self):
        return self.chain[-1]

    @staticmethod
    def valid_proof(block_string, proof):
        guess = f'{block_string}{proof}'.encode()
        guess_hash = hashlib.sha256(guess).hexdigest()
        # return True or False
        return guess_hash[:3] == "000"


# Instantiate our Node
app = Flask(__name__)

# Generate a globally unique address for this node
node_identifier = str(uuid4()).replace('-', '')

# Instantiate the Blockchain
blockchain = Blockchain()

# receive and validate or reject a new proof sent by a client.
    # * It should accept a POST
    # * Use `data = request.get_json()` to pull the data out of the POST
        # * Note that `request` and `requests` both exist in this project
    # * Check that 'proof', and 'id' are present
        # * return a 400 error using `jsonify(response)` with a 'message'
# * Return a message indicating success or failure.  Remember, a valid proof should fail for all senders except the first.
@app.route('/mine', methods=['POST'])
def mine():
    # Run the proof of work algorithm to get the next proof
    # proof = blockchain.proof_of_work(blockchain.last_block)
    # Forge the new Block by adding it to the chain with the proof
    data = request.get_json()
    required = ['proof', 'id'] 
    
    if not all(fields in data for fields in required):
        response={'message': "Missing Data"}
        return jsonify(response), 400
        
    inputted_proof = data.get('proof')

    last_block = blockchain.last_block
    last_block_string = json.dumps(last_block, sort_keys=True)
    
    if blockchain.valid_proof(last_block_string, inputted_proof):
        previous_hash = blockchain.hash(last_block)
        block = blockchain.new_block(inputted_proof, previous_hash)
        response = {
            'message': "New Block Forged",
            'index': block['index'],
            'transactions': block['transactions'],
            'proof': block['proof'],
            'previous_hash': block['previous_hash'],
        }
        return jsonify(response), 200
    else:
        response={'message': "Missing Data"}
        return jsonify(response), 400

   


@app.route('/chain', methods=['GET'])
def full_chain():
    response = {
        # TODO: Return the chain and its current length
        'length': len(blockchain.chain),
        'chain': blockchain.chain,
    }
    return jsonify(response), 200


@app.route('/last_block', methods=['GET'])
def last_block():
    response = {
        # TODO: Return the chain and its current length
        'last_block': blockchain.last_block,
    }
    return jsonify(response), 200

# Run the program on port 5000
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
