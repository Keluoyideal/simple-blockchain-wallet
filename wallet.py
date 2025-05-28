from ecdsa import SigningKey, SECP256k1

def generate_wallet():
    private_key = SigningKey.generate(curve=SECP256k1)
    public_key = private_key.get_verifying_key()

    return {
        'private_key': private_key.to_string().hex(),
        'public_key': public_key.to_string().hex()
    }

# 執行範例
if __name__ == '__main__':
    wallet = generate_wallet()
    print("🧾 這是你的錢包")
    print("🔐 私鑰:", wallet['private_key'])
    print("📬 公開金鑰（地址）:", wallet['public_key'])

