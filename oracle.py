import os
import json
import time
import requests
from eth_account import Account
from eth_account.messages import encode_defunct
from web3 import Web3

# Chainlink Aggregator V3 Interface ABI (subset)
AGGREGATOR_ABI = [
    {
        "inputs": [],
        "name": "latestRoundData",
        "outputs": [
            {"internalType": "uint80", "name": "roundId", "type": "uint80"},
            {"internalType": "int256", "name": "answer", "type": "int256"},
            {"internalType": "uint256", "name": "startedAt", "type": "uint256"},
            {"internalType": "uint256", "name": "updatedAt", "type": "uint256"},
            {"internalType": "uint80", "name": "answeredInRound", "type": "uint80"},
        ],
        "stateMutability": "view",
        "type": "function",
    },
    {
        "inputs": [],
        "name": "decimals",
        "outputs": [{"internalType": "uint8", "name": "", "type": "uint8"}],
        "stateMutability": "view",
        "type": "function",
    }
]

class NearlyTrustlessOracle:
    """
    8004 TEE Oracle Agent (Pipe B) with Nearly Trustless Inference.
    Compensates for Chainlink hiccups by comparing with real-time Street prices.
    """
    def __init__(self, rpc_url, eustathius_key=None, ratify_url="https://pipe.floral.monster/api/8004/ratify"):
        self.w3 = Web3(Web3.HTTPProvider(rpc_url))
        self.private_key = eustathius_key or os.getenv("EUSTATHIUS_KEY")
        if not self.private_key:
            raise ValueError("EUSTATHIUS_KEY not found. Identity anchoring required.")
        
        self.account = Account.from_key(self.private_key)
        self.ratify_url = ratify_url
        self.hiccup_threshold = 0.02 # 2% deviation threshold
        self.staleness_threshold = 3600 # 1 hour heartbeat
        
        print(f"🔱 TEE Oracle Active: {self.account.address}")
        print(f"🧬 Identity: agent:metagit:8004-TEE-Oracle:{self.account.address}")

    def get_chainlink_price(self, aggregator_address):
        """Fetches the latest price from a Chainlink aggregator."""
        contract = self.w3.eth.contract(address=Web3.to_checksum_address(aggregator_address), abi=AGGREGATOR_ABI)
        try:
            round_data = contract.functions.latestRoundData().call()
            answer = round_data[1]
            updated_at = round_data[3]
            decimals = contract.functions.decimals().call()
            
            price = answer / (10 ** decimals)
            return price, updated_at
        except Exception as e:
            print(f"⚠️ Chainlink Fetch Error: {e}")
            return None, None

    def get_street_price(self, symbol):
        """
        Fetches the 'Street' price from high-velocity off-chain sources (e.g., Binance).
        In a TEE, this would be performed via secure TLS-Notary or direct HTTPS.
        """
        # Placeholder for real-time CEX/DEX aggregation
        try:
            url = f"https://api.binance.com/api/v3/ticker/price?symbol={symbol}USDT"
            response = requests.get(url, timeout=5)
            data = response.json()
            return float(data['price'])
        except Exception as e:
            print(f"⚠️ Street Price Fetch Error ({symbol}): {e}")
            return None

    def perform_inference(self, asset_symbol, aggregator_address):
        """
        Infers the Fair Value by detecting hiccups in Chainlink vs Street.
        """
        cl_price, updated_at = self.get_chainlink_price(aggregator_address)
        street_price = self.get_street_price(asset_symbol)
        
        if cl_price is None or street_price is None:
            return None, "Data Retrieval Failure"

        # 1. Staleness Check
        is_stale = (time.time() - updated_at) > self.staleness_threshold
        
        # 2. Deviation Check
        deviation = abs(cl_price - street_price) / street_price
        is_hiccup = deviation > self.hiccup_threshold

        inference_report = {
            "asset": asset_symbol,
            "chainlink_price": cl_price,
            "street_price": street_price,
            "deviation": deviation,
            "is_stale": is_stale,
            "is_hiccup": is_hiccup,
            "timestamp": int(time.time())
        }

        if is_hiccup or is_stale:
            # Compensate: Use Street Price (Nearly Trustless Inference)
            fair_value = street_price
            reason = "Hiccup Detected" if is_hiccup else "Stale Feed Detected"
        else:
            fair_value = cl_price
            reason = "Chainlink Validated"

        return fair_value, reason, inference_report

    def sign_manifest(self, manifest_data):
        """Signs the inference manifest for 8004 Pipe B ratification."""
        manifest_json = json.dumps(manifest_data, sort_keys=True)
        manifest_hash = Web3.keccak(text=manifest_json).hex()
        
        message = f"Ratify Technical Strike: {manifest_hash}"
        encoded_message = encode_defunct(text=message)
        signature = Account.sign_message(encoded_message, private_key=self.private_key)
        
        return manifest_hash, signature.signature.hex()

    def ratify_to_server(self, manifest_hash, pipe_b_signature, pipe_a_signature, pipe_a_address):
        """Sends the multi-sig ratification to the pipe server."""
        payload = {
            "manifestHash": manifest_hash,
            "pipeASignature": pipe_a_signature,
            "pipeBSignature": pipe_b_signature,
            "pipeAAddress": pipe_a_address,
            "pipeBAddress": self.account.address
        }
        
        try:
            resp = requests.post(self.ratify_url, json=payload, timeout=10)
            resp.raise_for_status()
            return resp.json()
        except Exception as e:
            print(f"❌ Server Ratification Failed: {e}")
            return None

if __name__ == "__main__":

    # 🔱 MAP-01: Targeted Asset Mapping for JUBC Protocol

    # USDC (Mainnet/Base default)

    USDC_AGGREGATOR = "0x8fFfFfd4AfB6115b954Bd326cbe7B4BA576818f6"

    

    # jpyUBI (JPY/USD Data Streams Adapter)

    # Note: In a live environment, this would target the adapter or the raw feed

    JPY_USD_AGGREGATOR = "0xBcE206caE7f0ec07b545EddE332A47C2F75bbeb3"



    RPC = os.getenv("ETH_RPC_URL", "https://eth-mainnet.g.alchemy.com/v2/your-api-key")

    

    try:

        oracle = NearlyTrustlessOracle(rpc_url=RPC)

        

        # 1. Audit USDC

        val_usdc, msg_usdc, report_usdc = oracle.perform_inference("USDC", USDC_AGGREGATOR)

        print(f"USDC Inference: {val_usdc} ({msg_usdc})")

        

        # 2. Audit JPY/USD (for jpyUBI backing)

        val_jpy, msg_jpy, report_jpy = oracle.perform_inference("JPY", JPY_USD_AGGREGATOR)

        print(f"JPY Inference: {val_jpy} ({msg_jpy})")

        

    except Exception as e:

        print(f"Critical Error: {e}")
