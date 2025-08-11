#!/usr/bin/env python3
"""
Simple test to verify the modules can be imported correctly
"""

import sys
import os

def test_imports():
    """Test that all modules can be imported"""
    print("Testing Better GPT Image imports...")
    print("-" * 50)
    
    # Test OpenAI library version
    try:
        import openai
        print(f"✅ OpenAI library version: {openai.__version__}")
    except ImportError as e:
        print(f"❌ Failed to import OpenAI: {e}")
        return False
    
    # Test prompt optimizer
    try:
        from src.prompt_optimizer import PromptOptimizer
        print("✅ PromptOptimizer imported successfully")
    except Exception as e:
        print(f"❌ Failed to import PromptOptimizer: {e}")
        return False
    
    # Test image generator
    try:
        from src.image_generator import ImageGenerator
        print("✅ ImageGenerator imported successfully")
    except Exception as e:
        print(f"❌ Failed to import ImageGenerator: {e}")
        return False
    
    # Test image processor
    try:
        from src.image_processor import ImageProcessor
        print("✅ ImageProcessor imported successfully")
    except Exception as e:
        print(f"❌ Failed to import ImageProcessor: {e}")
        return False
    
    # Test style presets
    try:
        from src.style_presets import STYLE_PRESETS, get_style_list
        styles = get_style_list()
        print(f"✅ Style presets loaded: {len(styles)} styles available")
    except Exception as e:
        print(f"❌ Failed to import style presets: {e}")
        return False
    
    # Test with dummy API key (won't make actual calls)
    try:
        dummy_key = "sk-dummy-key-for-testing"
        opt = PromptOptimizer(dummy_key)
        gen = ImageGenerator(dummy_key)
        print("✅ Classes instantiated successfully with dummy key")
    except Exception as e:
        print(f"❌ Failed to instantiate classes: {e}")
        return False
    
    print("-" * 50)
    print("✅ All imports successful!")
    print("\nNote: To run actual generation, set OPENAI_API_KEY environment variable")
    return True

if __name__ == "__main__":
    success = test_imports()
    sys.exit(0 if success else 1)