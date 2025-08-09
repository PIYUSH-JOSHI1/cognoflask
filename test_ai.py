#!/usr/bin/env python3
"""
Test script to verify AI helpers work correctly with local models
"""

from config import Config
from ai_helpers import AIHelpers

import os
os.environ["TF_ENABLE_ONEDNN_OPTS"] = "0"

def test_ai_helpers():
    print("Testing AI Helpers with Local Models...")
    print("-" * 50)
    
    # Create config
    config = Config()
    
    # Initialize AI Helper
    print("1. Initializing AI Helper...")
    ai_helper = AIHelpers(config.__dict__)
    
    # Test text simplification
    print("\n2. Testing text simplification...")
    test_text = "The magnificent elephant demonstrated extraordinary intelligence while investigating the complex problem presented by the researchers."
    
    print(f"Original text: {test_text}")
    
    try:
        simplified = ai_helper.simplify_text(test_text)
        print(f"Simplified text: {simplified}")
        print("✅ Text simplification successful!")
    except Exception as e:
        print(f"❌ Text simplification failed: {e}")
    
    # Test text annotation
    print("\n3. Testing text annotation...")
    try:
        annotations = ai_helper.annotate_text(test_text)
        print(f"Annotations: {annotations}")
        print("✅ Text annotation successful!")
    except Exception as e:
        print(f"❌ Text annotation failed: {e}")
    
    print("\n" + "=" * 50)
    print("Test completed!")

if __name__ == "__main__":
    test_ai_helpers()
