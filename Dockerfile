FROM python:3.11-slim

WORKDIR /app

# Install dependencies
RUN pip install --no-cache-dir web3 eth-account requests

# Copy the oracle script
COPY oracle.py .

# Environment variables (to be provided via enclave-cid or secure injection)
ENV ETH_RPC_URL=""
ENV EUSTATHIUS_KEY=""
ENV RATIFY_URL="https://pipe.floral.monster/api/8004/ratify"

# The oracle will run in a loop or as a request-response server
# For this hackathon, we'll start with a loop that monitors specific assets
CMD ["python", "oracle.py"]
