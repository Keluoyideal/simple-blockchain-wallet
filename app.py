from flask import Flask, jsonify, request, render_template
from blockchain import Blockchain
import json
from ecdsa import SigningKey, SECP256k1
import hashlib

# 建立 Flask 應用與區塊鏈實例
app = Flask(__name__)
blockchain = Blockchain()

# 協助函式：生成簽章資料
def generate_signed_tx(sender_private_key, sender_public_key, recipient, amount):
    tx = {
        'sender': sender_public_key,
        'recipient': recipient,
        'amount': amount
    }
    tx_json = json.dumps(tx, sort_keys=True).encode()
    sk = SigningKey.from_string(bytes.fromhex(sender_private_key), curve=SECP256k1)
    signature = sk.sign(tx_json).hex()
    tx['signature'] = signature
    return tx

@app.route('/generate_wallet', methods=['GET'])
def generate_wallet():
    sk = SigningKey.generate(curve=SECP256k1)
    vk = sk.get_verifying_key()
    return jsonify({
        'private_key': sk.to_string().hex(),
        'public_key': vk.to_string().hex()
    })

@app.route('/sign_and_send_transaction', methods=['POST'])
def sign_and_send_transaction():
    data = request.get_json()
    tx = generate_signed_tx(data['sender_private_key'], data['sender_public_key'], data['recipient'], data['amount'])
    blockchain.add_transaction(tx['sender'], tx['recipient'], tx['amount'])
    return jsonify({'message': '交易簽章完成並已加入交易池'}), 201

@app.route('/preview_signed_tx', methods=['POST'])
def preview_signed_tx():
    data = request.get_json()
    tx = generate_signed_tx(data['sender_private_key'], data['sender_public_key'], data['recipient'], data['amount'])
    return jsonify(tx)

@app.route('/search_address/<public_key>', methods=['GET'])
def search_address(public_key):
    result = []
    for block in blockchain.chain:
        for tx in block['transactions']:
            if tx.get('sender') == public_key or tx.get('recipient') == public_key:
                result.append(tx)
    return jsonify(result)

# 其他路由（挖礦、新增交易、取得鏈、驗證鏈等）可維持不變

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    json_data = request.get_json()
    required_fields = ['sender_public_key', 'recipient', 'amount', 'signature']
    if not all(k in json_data for k in required_fields):
        return '交易資料有誤', 400

    is_valid = blockchain.is_valid_transaction(
        sender_public_key=json_data['sender_public_key'],
        recipient=json_data['recipient'],
        amount=json_data['amount'],
        signature=json_data['signature']
    )
    if not is_valid:
        return '簽章驗證失敗，交易非法', 403

    index = blockchain.add_transaction(
        sender=json_data['sender_public_key'],
        recipient=json_data['recipient'],
        amount=json_data['amount']
    )
    return jsonify({'message': f'交易將新增至區塊 {index}'}), 201

@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender='System', recipient='You', amount=1)
    block = blockchain.create_block(proof, previous_hash)
    return jsonify({
        'message': '成功挖礦',
        'block': block
    }), 200


@app.route('/get_chain', methods=['GET'])
def get_chain():
    return jsonify({
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }), 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5050)
