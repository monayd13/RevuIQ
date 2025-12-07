#!/bin/bash

# Set environment variables to avoid threading issues
export TOKENIZERS_PARALLELISM=false
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1

# Start the NLP API
echo "🚀 Starting NLP API with proper threading settings..."
python3 -u nlp_api_simple.py
