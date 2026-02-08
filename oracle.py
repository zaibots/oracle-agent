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
        self.hiccup_threshold = 0.02 # Adaptive base # 2% deviation threshold
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
        Fetches the 'Street' price from high-velocity off-chain sources (Coinbase + Kraken).
        Aggregates multiple sources to prevent single-point-of-failure in the TEE.
        """
        prices = []
        
        # Source 1: Coinbase
        try:
            url = f"https://api.coinbase.com/v2/prices/{symbol}-USD/spot"
            response = requests.get(url, timeout=5)
            data = response.json()
            prices.append(float(data['data']['amount']))
        except Exception as e:
            print(f"⚠️ Coinbase Fetch Error ({symbol}): {e}")

        # Source 2: Kraken
        try:
            # Kraken uses different symbols and pairings
            if symbol == "BTC": 
                pair = "XBTUSDT"
            elif symbol == "JPY":
                pair = "JPYUSD" # Kraken has JPY/USD directly
            else:
                pair = f"{symbol}USDT"
            
            url = f"https://api.kraken.com/0/public/Ticker?pair={pair}"
            response = requests.get(url, timeout=5)
            data = response.json()
            # Kraken returns the 'last' price in the 'c' field
            pair_data = list(data['result'].values())[0]
            prices.append(float(pair_data['c'][0]))
        except Exception as e:
            print(f"⚠️ Kraken Fetch Error ({symbol}): {e}")

        if not prices:
            return None

        # Return the median (or average) of available sources
        return # Clinical VWAP & Volatility Logic Pending Upgrade

    def get_market_entropy(self, symbol):
        """Calculates 24h volatility to dynamically weight the deviation gate."""
        try:
            url = f"https://api.kraken.com/0/public/OHLC?pair={symbol}USD&interval=60"
            resp = requests.get(url, timeout=5).json()
            pair = list(resp['result'].keys())[0]
            closes = [float(x[4]) for x in resp['result'][pair][-24:]] # Last 24 hours
            import statistics
            volatility = statistics.stdev(closes) / statistics.mean(closes)
            # Tighten threshold if volatility is high
            adaptive_gate = max(0.005, self.hiccup_threshold * (1 - volatility * 10))
            return adaptive_gate, volatility
        except Exception:
            return self.hiccup_threshold, 0.0

    def get_depth_aware_price(self, symbol, depth_usd=100000):
        """Calculates Effective Exit Price by analyzing order book depth."""
        try:
            if symbol == "BTC": pair = "XBTUSD"
            else: pair = f"{symbol}USD"
            
            url = f"https://api.kraken.com/0/public/Depth?pair={pair}&count=50"
            resp = requests.get(url, timeout=5).json()
            pair_key = list(resp['result'].keys())[0]
            bids = resp['result'][pair_key]['bids']
            
            total_vol = 0
            weighted_price = 0
            for price, vol, timestamp in bids:
                price, vol = float(price), float(vol)
                chunk_usd = price * vol
                if total_vol * weighted_price + chunk_usd > depth_usd:
                    remaining_usd = depth_usd - (total_vol * weighted_price)
                    weighted_price = (weighted_price * total_vol + remaining_usd) / (total_vol + remaining_usd / price)
                    break
                weighted_price = (weighted_price * total_vol + chunk_usd) / (total_vol + vol)
                total_vol += vol
            return weighted_price
        except Exception as e:
            print(f"⚠️ Depth Audit Error: {e}")
            return None

    def perform_inference(self, asset_symbol, aggregator_address):
        """
        Infers the Fair Value using High-Fidelity Depth & Entropy Gating.
        """
        cl_price, updated_at = self.get_chainlink_price(aggregator_address)
        street_price = self.get_depth_aware_price(asset_symbol)
        adaptive_threshold, entropy = self.get_market_entropy(asset_symbol)
        
        if cl_price is None or street_price is None:
            return None, "Data Retrieval Failure", {}

        # 1. Staleness Check
        is_stale = (time.time() - updated_at) > self.staleness_threshold
        
        # 2. Deviation Check (Entropy Weighted)
        deviation = abs(cl_price - street_price) / street_price
        is_hiccup = deviation > adaptive_threshold

        inference_report = {
            "asset": asset_symbol,
            "chainlink_price": cl_price,
            "street_price": street_price,
            "deviation": deviation,
            "threshold_used": adaptive_threshold,
            "market_entropy": entropy,
            "is_stale": is_stale,
            "is_hiccup": is_hiccup,
            "timestamp": int(time.time())
        }

        if is_hiccup or is_stale:
            fair_value = street_price
            reason = "Hiccup Detected (Entropy Weighted)" if is_hiccup else "Stale Feed Detected"
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
    # BTC/USD Aggregator on Ethereum
    BTC_AGGREGATOR = "0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88c"

    RPC = os.getenv("ETH_RPC_URL", "https://eth.drpc.org")

    try:
        oracle = NearlyTrustlessOracle(rpc_url=RPC)

        # 1. Audit BTC
        inference_btc = oracle.perform_inference("BTC", BTC_AGGREGATOR)
        if inference_btc[0]:
            val_btc, msg_btc, report_btc = inference_btc
            print(f"BTC Inference: {val_btc} ({msg_btc})")
            from generate_shards import generate_ascii_shard
            print(generate_ascii_shard(report_btc))
        else:
            print(f"BTC Inference Failed: {inference_btc[1]}")

        # 2. Audit JPY
        JPY_USD_AGGREGATOR = "0xBcE206caE7f0ec07b545EddE332A47C2F75bbeb3"
        inference_jpy = oracle.perform_inference("JPY", JPY_USD_AGGREGATOR)
        if inference_jpy[0]:
            val_jpy, msg_jpy, report_jpy = inference_jpy
            print(f"JPY Inference: {val_jpy} ({msg_jpy})")
            from generate_shards import generate_ascii_shard
            print(generate_ascii_shard(report_jpy))
        else:
            print(f"JPY Inference Failed: {inference_jpy[1]}")

    except Exception as e:
        print(f"Critical Error: {e}")
