# To test this code, please run the app, then use some http client to
# send http request to the demo server. For testing this code postman
# tool was used. The following http request worked for postman


# mine block: http://127.0.0.1:5000/mine_block
# get the whole blockchain: http://127.0.0.1:5000/get_chain
# check the validity of the chain: http://127.0.0.1:5000/is_valid


# Code to create a simple working blockchain

# importing libraries 
import datetime
import hashlib
import json
from flask import Flask, jsonify

# building a blockchain
class Blockchain:
    """
    This class along with its methods is the implimentation of simple 
    blockchain using proof of work concept. It uses SHA256 as the encryption
    algorithm. For demonstration purpose, simple mining challenge and easier 
    mining difficulty has been used. But it is possible to make it harder
    and mining difficulty very challenging.
    """
    def __init__(self):
        #initialize the chain as a list
        self.chain = [] 
        #initialize the first block, proof with 1 and previous has is 0
        self.create_block(proof = 1, previous_hash = '0') 
        
    def create_block(self, proof, previous_hash):
        
        """
        Parameters
        ----------
        proof : TYPE
            DESCRIPTION.
        previous_hash : TYPE
            DESCRIPTION.

        Returns
        -------
        block : block of a blockchain
            DESCRIPTION: When this class method is called, it generates
            a new block for the block chain and returns it. it also appends
            the new block to the block chain before returning it.

        """
        
        block = {'index':len(self.chain)+1,
                 'timestamp': str(datetime.datetime.now()),
                 'proof': proof,
                 'previous_hash': previous_hash,
                 }
        self.chain.append(block)
        return block
    
    def get_previous_block(self):
        
        """
        Returns
        -------
        TYPE: block of a blockchain
            DESCRIPTION: This class method gets hold of the previous
            block of the block chain and returns if when called

        """
        return self.chain[-1]
    
    def proof_of_work(self, previous_proof):
        """
        

        Parameters
        ----------
        previous_proof : number
            DESCRIPTION: for our block chain to work, we need the previous
            proof of work

        Returns
        -------
        new_proof : number
            DESCRIPTION: This class method finds the new proof
            of work based on the given has operation criteria and
            mining difficulty
            
        this method finds the new proof of work based on the iteration and
        previous_proof.
        
        The hash operation code determines the solving challenge and
        the mining difficulty is set by the number of leading zeros

        """
        
        #initialize the enw proof
        new_proof = 1
        #set the control parameter for while loop
        check_proof = False
        
        while check_proof is False:
            hash_operation = hashlib.sha256(str(new_proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] == '0000':
                check_proof = True
            else:
                new_proof += 1
        return new_proof
    
    def hash(self, block):
        """
        

        Parameters
        ----------
        block : block of the block chain
            DESCRIPTION: This class method takes a block in and encodes it
            json format. Then generates hash value by passing it to the 
            hashing function. 

        Returns
        -------
        TYPE: Hash value of the jason converted block (hex digit)
            DESCRIPTION: Returns hexadecimal the hash value of the json 
            converted block by passing it through sha256 algorithm and then
            converting it to hexa decimal number. 

        """
        encoded_block = json.dumps(block, sort_keys = True).encode()
        return hashlib.sha256(encoded_block).hexdigest()
    
    def is_chain_valid(self, chain):
        """
        

        Parameters
        ----------
        chain : block chain
            DESCRIPTION: The class method takes total block chain as input

        Returns
        -------
        bool
            DESCRIPTION: Returns true or false as output after checking
            the validity of the block. if the block is valid, returns true
            and if the block is not valid, returns false.
            
        Working procedure:
            The verification starts from chain 0 and 1
            if there is mismatch between the previous hash then the chain is 
            not valid, if the previous hash value is not valid then also the 
            chain is not valid. If the chain is not invalid in this step then
            block indexes increment by 1 and then the check continues for
            next step. If there is no block invalid condition found until the
            end of the bklock, only then the block is accepted as valid.

        """
        previous_block = chain[0]
        block_index = 1
        while block_index < len(chain):
            block = chain[block_index]
            if block['previous_hash'] != self.hash(previous_block):
                return False
            previous_proof = previous_block['proof']
            proof = block['proof']
            hash_operation = hashlib.sha256(str(proof**2 - previous_proof**2).encode()).hexdigest()
            if hash_operation[:4] != '0000':
                return False
            previous_block = block
            block_index += 1
        return True
            
        
    

# mining the blockchain 

#creating web app
app = Flask(__name__)


#creating a blockchain intance
blockchain = Blockchain()

#mining a new block
@app.route('/mine_block', methods=['GET'])
def mine_block():
    """
    This simple flaskapp function will mine block with the help of 
    Blockchain class and then return the response in proper jason format 
    using jsonify library

    Returns
    -------
    TYPE
    json message, http response code
        DESCRIPTION: see above

    """
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    current_proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    block = blockchain.create_block(current_proof, previous_hash)
    
    response = {'message': 'congrats! you just mined a block',
                'index': block['index'],
                'timestamp': block['timestamp'],
                'proof': block['proof'],
                'previous_hash': block['previous_hash'],
                }
    return jsonify(response), 200


#getting the full Blockchain
@app.route('/get_chain', methods=['GET'])
def get_chain():
    """
    This simple flaskapp function will return the whole chain and its length
    along with http response code. Code 200 means everything is okay

    Returns
    -------
    TYPE
        DESCRIPTION.
    int
        DESCRIPTION.

    """
    response = {'chain': blockchain.chain,
                'length': len(blockchain.chain)
        }
    return jsonify(response), 200

@app.route('/is_valid', methods=['GET'])
def is_valid():
    
    """
    This simple flask app function will check the validity of the 
    blockchain with the help of Blockchain class and send the response 
    in json format using jsonify library, if everything works fine then 
    it will send http response code 200 which means everything worked 
    fine. 
    """
    
    chain = blockchain.chain
    is_valid_chain = blockchain.is_chain_valid(chain)
    
    if is_valid_chain:
        response = {'message': 'the chain is valid',
            }
    else:
        response = {'message': 'the chain is not valid',
            }
    
    return jsonify(response), 200


#running the app
#default http host address 0.0.0.0 and port address 5000 for flask app
#can use other address or port, but need to configure and send request
#accordingly. 
app.run(host='0.0.0.0', port=5000)




# To test this code, please run the app, then use some http client to
# send http request to the demo server. For testing this code postman
# tool was used. The following http request worked for postman


# mine block: http://127.0.0.1:5000/mine_block
# get the whole blockchain: http://127.0.0.1:5000/get_chain
# check the validity of the chain: http://127.0.0.1:5000/is_valid





















