from ecdsa import SigningKey, SECP256k1
import json

# 這裡請貼上你自己的私鑰（從 wallet.py 複製來）
PRIVATE_KEY_HEX = '8d03e1b18729a5c5d1858cb60002c02cca58ef35507bb3da4d7fc8e314e63bfa'

# 從 hex 還原回私鑰物件
private_key = SigningKey.from_string(bytes.fromhex(PRIVATE_KEY_HEX), curve=SECP256k1)

# 要簽的交易內容（注意 sender_public_key 也要填）
transaction = {
    'sender_public_key': '8d03e1b18729a5c5d1858cb60002c02cca58ef35507bb3da4d7fc8e314e63bfa',
    'recipient': 'bob_public_key_here',
    'amount': 10
}

# 序列化交易資料（不包含 signature）
message = json.dumps(transaction, sort_keys=True)

# 使用私鑰簽章
signature = private_key.sign(message.encode()).hex()

# 最後你要送給區塊鏈節點的資料是這個：
signed_transaction = transaction.copy()
signed_transaction['signature'] = signature

print("✅ 請貼到 Postman：")
print(json.dumps(signed_transaction, indent=2))
