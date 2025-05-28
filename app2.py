from flask import Flask, jsonify, request, render_template
from blockchain import Blockchain

# 建立 Flask 應用與區塊鏈實例
app = Flask(__name__)
blockchain = Blockchain()

# 開採區塊
@app.route('/mine_block', methods=['GET'])
def mine_block():
    previous_block = blockchain.get_previous_block()
    previous_proof = previous_block['proof']
    proof = blockchain.proof_of_work(previous_proof)
    previous_hash = blockchain.hash(previous_block)
    blockchain.add_transaction(sender='System', recipient='You', amount=1)
    block = blockchain.create_block(proof, previous_hash)
    return jsonify({
        'message': '成功挖礦！',
        'block': block
    }), 200

# 新增交易
@app.route('/add_transaction', methods=['POST'])
def add_transaction():
    json_data = request.get_json()
    required_fields = ['sender', 'recipient', 'amount']
    if not all(k in json_data for k in required_fields):
        return '交易資料有誤', 400
    index = blockchain.add_transaction(
        sender=json_data['sender'],
        recipient=json_data['recipient'],
        amount=json_data['amount']
    )
    return jsonify({'message': f'交易將新增至區塊 {index}'}), 201

# 取得整條區塊鏈
@app.route('/get_chain', methods=['GET'])
def get_chain():
    return jsonify({
        'chain': blockchain.chain,
        'length': len(blockchain.chain)
    }), 200

# 驗證區塊鏈
@app.route('/is_valid', methods=['GET'])
def is_valid():
    valid = blockchain.is_chain_valid(blockchain.chain)
    return jsonify({'valid': valid}), 200

# 首頁（如果你有 index.html）
@app.route('/')
def index():
    return render_template('index.html')

# 🧩 分散式節點功能

# 1️⃣ 節點註冊
@app.route('/connect_node', methods=['POST'])
def connect_node_route():
    json_data = request.get_json()
    nodes = json_data.get('nodes')
    if nodes is None:
        return "錯誤：請提供節點列表", 400
    for node in nodes:
        blockchain.add_node(node)
    return jsonify({
        'message': '節點新增成功',
        'total_nodes': list(blockchain.nodes)
    }), 200

# 2️⃣ 查看節點列表
@app.route('/get_nodes', methods=['GET'])
def get_nodes_route():
    return jsonify({
        'nodes': list(blockchain.nodes)
    }), 200

# 3️⃣ 共識機制：若鏈比較短則同步
@app.route('/replace_chain', methods=['GET'])
def replace_chain_route():
    is_replaced = blockchain.replace_chain()
    if is_replaced:
        return jsonify({
            'message': '鏈已被取代',
            'new_chain': blockchain.chain
        }), 200
    else:
        return jsonify({
            'message': '目前鏈已是最長',
            'chain': blockchain.chain
        }), 200

# 執行應用程式
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5051)
