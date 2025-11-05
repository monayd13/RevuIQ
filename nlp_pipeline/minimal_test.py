"""
Minimal Test - Ultra-safe version for macOS
Uses smaller models and CPU-only mode
"""

print("🧠 RevuIQ - Minimal Test (macOS Safe Mode)\n")

# Test 1: Basic imports
print("Step 1: Testing basic imports...")
try:
    import torch
    import transformers
    print("✅ PyTorch and Transformers installed")
    print(f"   PyTorch version: {torch.__version__}")
    print(f"   Transformers version: {transformers.__version__}")
except ImportError as e:
    print(f"❌ Import failed: {e}")
    print("Run: pip install torch transformers")
    exit(1)

# Force CPU mode
import os
os.environ['CUDA_VISIBLE_DEVICES'] = ''
print("✅ Forced CPU-only mode\n")

# Test 2: Load a simple sentiment model
print("Step 2: Loading sentiment model (this will download ~500MB)...")
try:
    from transformers import pipeline
    
    # Use a smaller, faster model
    classifier = pipeline(
        "sentiment-analysis",
        model="distilbert-base-uncased-finetuned-sst-2-english",
        device=-1  # Force CPU
    )
    print("✅ Model loaded successfully!\n")
    
    # Test it
    print("Step 3: Testing sentiment analysis...")
    test_review = "The coffee was amazing!"
    result = classifier(test_review)[0]
    
    print(f"Review: {test_review}")
    print(f"Result: {result['label']} (confidence: {result['score']:.1%})")
    print("\n✅ SUCCESS! NLP pipeline is working!\n")
    
    print("="*70)
    print("🎉 Your system is ready for RevuIQ!")
    print("="*70)
    print("\nNext steps:")
    print("1. The models are now cached (won't download again)")
    print("2. Try: bash run_test.sh")
    print("3. Or continue with the full demo")
    
except Exception as e:
    print(f"\n❌ Error: {e}")
    print("\nTroubleshooting:")
    print("1. Check internet connection (models need to download)")
    print("2. Try: pip install --upgrade torch transformers")
    print("3. Restart terminal and try again")
    import traceback
    traceback.print_exc()
