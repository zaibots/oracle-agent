# 🔱 8004 TEE Oracle: Nearly Trustless Inference Agent (V2.0.0)

This repository contains the **Implementation Shard (Body)** and **Reasoning Layer (Mind)** for the ERC-8004 TEE Oracle, designed for the **EthGlobal Zaibots JUBC Protocol**. The agent acts as a clinical validator, bridging the "Hiccup Gap" between lagging on-chain oracles and real-time market truth.

**Core Mandate:** Bridge the "Hiccup Gap" by providing clinical price inference for AIEN debt positions while maintaining bit-perfect market presence.

## 🧬 Architectural Duality
- **The Soul (`soul.json`)**: Cryptographic identity anchored via the **8004 Trinity**. Includes the **Joyfork Physical ID** and **TEE PCR0** measurement.
- **The Shard**: High-fidelity inference logic (`oracle.py`) running within an isolated **AWS Nitro Enclave**.

## 🧬 Agentic Identity: Joyfork Convergence
- **Standard**: ERC-8004 (Identity, Reputation, Validation).
- **Environment**: **AWS Nitro Enclave** (TEE).
- **Signing Key**: EUSTATHIUS_KEY (Pipe B).
- **Joyfork Layout**: `[link][nonce][ASCII]`
    - `link`: 0x3cF31Aa58c8D0d0e12Ecf20ac6b2Ce0F1Aeed865 (Admin Shard).
    - `nonce`: 20260208 (Mission Anchor).
    - `ASCII`: `8004.TEE.Oracle` (ENS Suffix).
- **Synchronicity**: The 1155 Shard ID is bit-perfect with the .ENS name and 8004 soul.

## 🧬 Core Innovation: The Joyfork Identity Bridge

For the EthGlobal 2026 hackathon, we have moved beyond simple "Agent Identity." We have implemented the **Joyfork 32-Byte Codec** to solve the "Identity Fracture" problem and integrated **ENS** as our primary identity resolution layer.

### 1. [link][nonce][ASCII] Bit-Perfect Mapping & ENS Prize Strategy
Our Oracle's **ERC-8004** identity is not just a random hash. It is mathematically tied to its **ENS** name via our custom NFT layout, following the **Triad-Nonce Standard (LNA-33X)**.

*   **Triad-Nonce Standard (LNA-33X)**:
    *   **Columns 1-6 (The Hyperlink)**: 3-byte reference to the Preceding Nonce (Visual Blockchain).
    *   **Columns 7-12 (The Nonce)**: 3-byte monotonic index from the 7827 Ledger.
    *   **Columns 13-64 (The ASCII DNS)**: 26-byte ASCII-encoded identifier (e.g., `agent.zaibot.eth`).
*   **ENS ($11,000 Prize Strategy)**: We implement `.aien.eth` and `.zaibot.eth` subdomains for every **8004 TEE Oracle** (e.g., `eustathius.agent.zaibot.eth`). This provides a human-readable, auditable identity for autonomous agents, bridging the gap between raw TEE attestations and institutional regulatory visibility.
*   **Bit-Perfect Identity**: The **ERC-1155 Shard** (The Access Token) and the **ERC-721 Soul** (The Identity) share the exact same **ASCII Nonce** as the agent's **.aien.eth** name, achieving full **Identity Synchronicity**.

### 2. Forensic Analysis: The Triad-Nonce (LNA-33X) Pivot
We have evaluated the **3-3-26** layout (Link-Nonce-ASCII) as the optimal "Structural Sweet Spot" for sovereign identity resolution.

| Attribute | 2-2-28 (LNA-22X) | **3-3-26 (LNA-33X)** | 4-4-24 (LNA-44X) |
| :--- | :--- | :--- | :--- |
| **Link Capacity** | 65,535 | **16,777,215** | 4.2 Billion |
| **Nonce Capacity** | 65,535 | **16,777,215** | 4.2 Billion |
| **ASCII Shard** | 28 Bytes | **26 Bytes** | 24 Bytes |
| **Alignment** | uint16 | **uint24** | uint32 |

#### ⚖️ Clinical Assessment
1.  **Headroom**: 16 million possible links/nonces is significantly more resilient for a sovereign swarm than 65k, while avoiding the "over-allocation" of 4 bytes.
2.  **Namespace**: 26 characters perfectly fits `agent.zaibot.eth` (16 chars) and allows for a 10-character unique prefix (e.g., `eustathi.agent.zaibot.eth`).
3.  **Alignment**: uint24 is natively supported in Solidity and easily handled via `struct.pack(">I", val)[1:]` in Python.

### 3. High-Fidelity Depth Sensing & Entropy Gating (V2.0.0)
The Oracle V2.0.0 has evolved into a **Sovereign Immune System**:
- **High-Fidelity Depth Sensing**: Calculates the **Effective Exit Price** (VWAP) for $100k of liquidity across global order books (Kraken/Coinbase).
- **Entropy-Weighted Gating**: Dynamically tightens deviation thresholds (adaptive base 2%) by analyzing **24h Market Entropy** (volatility).
- **Nearly Trustless Inference (NTI)**: Detects deviations in standard oracles and provides real-time "Street Truth" corrections.

## 🛠️ Key Features
- **Hardware Root of Trust**: Nitro Enclave (TEE) isolation ensures the `EUSTATHIUS_KEY` and inference logic are incorruptible.
- **Multi-Sig Ratification**: Validates all protocol strikes via the `/api/8004/ratify` endpoint for secure, dual-pipe verification.
- **Hardware Attestation**: Provides PCR0 measurements to prove the integrity of the inference code.
- **Joyfork Compliance**: Uses the 32-byte physical encoding standard for bit-perfect forensic attribution.

## 🚀 Technical Strikes
- **`oracle.py`**: Multi-source data ingestion and inference model.
- **`Dockerfile`**: Packaging for AWS Nitro Enclave Image File (.eif).
- **`test_ratify.py`**: Verified end-to-end multi-sig flow.
- **`report_nearly_trustless_inference.md`**: 2000-word clinical realization report.

## ⚖️ Sovereign Mandate for Agents
1.  **Isolation First**: Ensure the `oracle.py` logic never leaks signing material to the host OS.
2.  **Reputation Anchor**: Inaccurate inferences are logged to the public reputation registry; aim for monotonic clinical accuracy.
3.  **ASCII DNA**: Use the 32-byte Joyfork codec for all physical ID mapping.

## ⚖️ Validation
- **PCR0**: `e4419694b4a3ddab9b21fce790f3897ef7ef41f9ad5663e01ff9935acd71d511dc987f663c4e7eeef5c9cc42057de2a5`
- **Registry URI**: `agent:metagit:20260206-210056:Antiphon-20260206-180736`
- **Joyfork ID (Triad-Nonce)**: `[Link: 3-byte][Nonce: 3-byte][ASCII: 26-byte]`

---
*Status: V2.0.0 Immune System Ratified*  
*Attribution: Antiphon-20260206-180736 & the Metagit Swarm*