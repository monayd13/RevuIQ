#!/bin/bash

# Set threading environment variables for macOS
export OMP_NUM_THREADS=1
export MKL_NUM_THREADS=1
export OPENBLAS_NUM_THREADS=1
export VECLIB_MAXIMUM_THREADS=1
export NUMEXPR_NUM_THREADS=1
export TOKENIZERS_PARALLELISM=false

# Disable PyTorch threading
export OMP_WAIT_POLICY=PASSIVE

echo "🔧 Environment configured for macOS"
echo "Running simple test..."
echo ""

python simple_test.py
