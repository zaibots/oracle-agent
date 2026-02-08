from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from oracle import NearlyTrustlessOracle
import os
import json
import uvicorn

app = FastAPI()

# Enable CORS for Next.js localhost
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize Oracle with the established demo key
EUSTATHIUS_KEY = "0x8b89412f12c6a0840a023712c6a0840a023712c6a0840a023712c6a0840a0237"
RPC = os.getenv("ETH_RPC_URL", "https://eth.drpc.org")
oracle = NearlyTrustlessOracle(rpc_url=RPC, eustathius_key=EUSTATHIUS_KEY)

# Load the Sovereign Soul (8004 Identity)
with open("soul.json", "r") as f:
    soul_data = json.load(f)

# Zaibots Asset Registry
ASSETS = {
    "BTC": "0xF4030086522a5bEEa4988F8cA5B36dbC97BeE88c",
    "USDC": "0x8fFfFfd4AfB6115b954Bd326cbe7B4BA576818f6",
    "JPY": "0xBcE206caE7f0ec07b545EddE332A47C2F75bbeb3"
}

@app.get("/api/inference")
async def get_inference():
    try:
        results = []
        for symbol, aggregator in ASSETS.items():
            inference = oracle.perform_inference(symbol, aggregator)
            if len(inference) == 3:
                val, msg, report = inference
                if val is not None:
                    # Sign each manifest to create the 8004 Artifact per asset
                    manifest_hash, signature = oracle.sign_manifest(report)
                    
                    results.append({
                        "asset": symbol,
                        "value": val,
                        "message": msg,
                        "report": report,
                        "hash": manifest_hash,
                        "signature": signature
                    })
        
        return {
            "audits": results,
            "identity": oracle.account.address,
            "soul": soul_data["agent_card"],
            "artifacts": {
                "tee_proof": {
                    "type": "Hardware Attestation (PCR0)",
                    "value": soul_data["agent_card"]["technical_specs"]["pcr0"],
                    "description": "Proves the audit logic is isolated within the AWS Nitro Enclave."
                },
                "8004_proof": {
                    "type": "Signed Manifest (Reputation)",
                    "description": "The agent's signed 'Proof of Truth', staking its reputation on the audit."
                }
            }
        }
    except Exception as e:
        return {"error": str(e)}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8004)
