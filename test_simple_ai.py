#!/usr/bin/env python3
"""
Simple test script for AI helpers with minimal dependencies
"""

import os

# Set environment to avoid TensorFlow
os.environ['USE_TF'] = 'false'
os.environ['USE_TORCH'] = 'true'

from config import Config
from ai_helpers import AIHelpers

def test_simple_ai():
    print("Testing AI Helpers with Local Models...")
    print("-" * 50)
    
    # Create config
    config_dict = {
        'USE_LOCAL_MODELS': True,
        'AI_MODEL_NAME': 'google/flan-t5-small',
        'MODEL_CACHE_DIR': './data/ai_models'
    }
    
    # Initialize AI Helper
    print("1. Initializing AI Helper...")
    try:
        ai_helper = AIHelpers(config_dict)
        print("✅ AI Helper initialized successfully!")
    except Exception as e:
        print(f"❌ AI Helper initialization failed: {e}")
        return
    
    # Test text simplification
    print("\n2. Testing text simplification...")
    test_text = "The magnificent elephant demonstrated extraordinary intelligence."
    
    print(f"Original text: {test_text}")
    
    try:
        simplified = ai_helper.simplify_text(test_text)
        print(f"Simplified text: {simplified}")
        print("✅ Text simplification successful!")
    except Exception as e:
        print(f"❌ Text simplification failed: {e}")
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    test_simple_ai()
