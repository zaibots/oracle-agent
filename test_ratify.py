import os
import json
import requests
from eth_account import Account
from eth_account.messages import encode_defunct
from web3 import Web3

def test_ratification():
    # 1. Setup Identities
    # Pipe A (Reasoning Agent - Placeholder dummy key)
    pipe_a_key = "0x" + "a" * 64
    pipe_a_account = Account.from_key(pipe_a_key)
    
    # Pipe B (Oracle - Eustathius - Placeholder dummy key)
    # In production, this would be the EUSTATHIUS_KEY inside the TEE
    pipe_b_key = "0x" + "b" * 64
    pipe_b_account = Account.from_key(pipe_b_key)
    
    ratify_url = "https://pipe.floral.monster/api/8004/ratify"
    manifest_hash = Web3.keccak(text="TEST-STRIKE-MANIFEST-001").hex()
    
    print(f"🔱 Starting Multi-Sig Verification for Strike: {manifest_hash}")
    print(f"Pipe A: {pipe_a_account.address}")
    print(f"Pipe B: {pipe_b_account.address}")

    # 2. Sign message for both pipes
    message = f"Ratify Technical Strike: {manifest_hash}"
    encoded_message = encode_defunct(text=message)
    
    signature_a = "0x" + Account.sign_message(encoded_message, private_key=pipe_a_key).signature.hex()
    signature_b = "0x" + Account.sign_message(encoded_message, private_key=pipe_b_key).signature.hex()

    # 3. Submit Ratification
    payload = {
        "manifestHash": manifest_hash,
        "pipeASignature": signature_a,
        "pipeBSignature": signature_b,
        "pipeAAddress": pipe_a_account.address,
        "pipeBAddress": pipe_b_account.address
    }
    
    print(f"🚀 Submitting to {ratify_url}...")
    try:
        response = requests.post(ratify_url, json=payload, timeout=10)
        print(f"Status: {response.status_code}")
        print(f"Response: {json.dumps(response.json(), indent=2)}")
        
        if response.status_code == 200:
            print("✅ Multi-Sig Ratification SUCCESSFUL.")
        else:
            print("❌ Multi-Sig Ratification FAILED.")
            
    except Exception as e:
        print(f"❌ Error during ratification request: {e}")

if __name__ == "__main__":
    test_ratification()
