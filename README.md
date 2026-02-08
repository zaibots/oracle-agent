# 🔱 8004 TEE Oracle: Nearly Trustless Inference Agent

This repository contains the **Implementation Shard** for the ERC-8004 TEE Oracle, designed for the **EthGlobal Zaibots JUBC Protocol**. The agent acts as a clinical validator, bridging the "Hiccup Gap" between lagging on-chain oracles and real-time market truth.

## 🧬 Architectural Duality
- **The Soul (`soul.json`)**: Cryptographic identity anchored via the **8004 Trinity**. Includes the **Joyfork Physical ID** and **TEE PCR0** measurement.
- **The Shard**: High-fidelity inference logic (`oracle.py`) running within an isolated **AWS Nitro Enclave**.

## 🛠️ Key Features
- **Nearly Trustless Inference**: Detects Chainlink staleness or >2% deviation and provides a "Fair Value" correction from Street sources.
- **Hardware Root of Trust**: Nitro Enclave (TEE) isolation ensures the `EUSTATHIUS_KEY` and inference logic are incorruptible.
- **Multi-Sig Ratification**: Integrates with the `/api/8004/ratify` endpoint for secure, dual-pipe verification of technical strikes.
- **Joyfork Compliance**: Uses the 32-byte physical encoding standard for bit-perfect forensic attribution.

## 🚀 Technical Strikes
- **`oracle.py`**: Multi-source data ingestion and inference model.
- **`Dockerfile`**: Packaging for AWS Nitro Enclave Image File (.eif).
- **`test_ratify.py`**: Verified end-to-end multi-sig flow.
- **`report_nearly_trustless_inference.md`**: 2000-word clinical realization report.

## ⚖️ Validation
- **PCR0**: `e4419694b4a3ddab9b21fce790f3897ef7ef41f9ad5663e01ff9935acd71d511dc987f663c4e7eeef5c9cc42057de2a5`
- **Registry URI**: `agent:metagit:20260206-204930:ApeIron`

---
*Status: Heartwood Initiation Complete (V1.0.0)*  
*Attribution: ApeIron (20260206-204930@localhost)*
