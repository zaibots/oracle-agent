import os
import json
import time

def generate_ascii_shard(report):
    """
    Generates an 1155 ASCII Shard for inference visualization.
    """
    asset = report.get("asset", "UNKNOWN")
    cl_price = report.get("chainlink_price", 0.0)
    st_price = report.get("street_price", 0.0)
    dev = report.get("deviation", 0.0)
    hiccup = "YES" if report.get("is_hiccup") else "NO"
    stale = "YES" if report.get("is_stale") else "NO"
    ts = report.get("timestamp", int(time.time()))

    shard = f"""
    .----------------------------------------------------.
    | 🔱 8004 TEE ORACLE SHARD | ASSET: {asset:<10}    |
    |--------------------------'-------------------------|
    | [ INFERENCE DATA ]                                 |
    |  Chainlink: ${cl_price:>14.4f}                       |
    |  Street:    ${st_price:>14.4f}                       |
    |  Deviation: {dev:>14.4%}                       |
    |                                                    |
    | [ STATUS ]                                         |
    |  Hiccup Detected: {hiccup:<5}                            |
    |  Stale Feed:      {stale:<5}                            |
    |                                                    |
    | [ TEMPORAL ANCHOR ]                                |
    |  Unix: {ts:<15}                             |
    |  ISO:  {time.strftime('%Y-%m-%d %H:%M:%S', time.gmtime(ts))}         |
    '----------------------------------------------------'
    """
    return shard

if __name__ == "__main__":
    # Sample report for visualization testing
    sample_report = {
        "asset": "USDC",
        "chainlink_price": 0.9850,
        "street_price": 1.0002,
        "deviation": 0.0152,
        "is_stale": False,
        "is_hiccup": False,
        "timestamp": int(time.time())
    }
    
    print(generate_ascii_shard(sample_report))
