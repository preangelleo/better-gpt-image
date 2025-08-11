#!/usr/bin/env python3
"""
Better GPT Image - Python Example
Complete example showing all parameters and usage patterns
"""

import replicate
import os
import json
from typing import List, Optional

# Get your API tokens
REPLICATE_API_TOKEN = os.getenv("REPLICATE_API_TOKEN")
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

if not REPLICATE_API_TOKEN:
    print("Please set REPLICATE_API_TOKEN environment variable")
    print("Get your token at: https://replicate.com/account/api-tokens")
    exit(1)

if not OPENAI_API_KEY:
    print("Please set OPENAI_API_KEY environment variable")
    print("Get your key at: https://platform.openai.com/api-keys")
    exit(1)

class BetterGPTImage:
    """Wrapper class for Better GPT Image on Replicate"""
    
    def __init__(self, replicate_token: str, openai_key: str):
        self.client = replicate.Client(api_token=replicate_token)
        self.openai_key = openai_key
        self.model = "preangelleo/better-gpt-image:latest"
    
    def generate(
        self,
        prompt: str,
        style_preset: str = "none",
        optimize_prompt: bool = True,
        size: str = "1024x1024",
        quality: str = "high",
        num_images: int = 1,
        **kwargs
    ) -> List[str]:
        """
        Generate images with Better GPT Image
        
        Args:
            prompt: Description of the image to generate
            style_preset: Artistic style (90+ options available)
            optimize_prompt: Whether to enhance prompt with GPT
            size: Image dimensions
            quality: Generation quality
            num_images: Number of images to generate
            **kwargs: Additional parameters
        
        Returns:
            List of image URLs
        """
        
        # Build input parameters with defaults
        input_params = {
            # Required
            "api_key": self.openai_key,
            "prompt": prompt,
            
            # Core settings
            "optimize_prompt": optimize_prompt,
            "optimization_model": kwargs.get("optimization_model", "gpt-5"),
            "style_preset": style_preset,
            
            # Image settings
            "size": size,
            "quality": quality,
            "num_images": num_images,
            
            # Advanced features (optional)
            "reference_images": kwargs.get("reference_images", ""),
            "mask_image": kwargs.get("mask_image", ""),
            "background": kwargs.get("background", "auto"),
            "input_fidelity": kwargs.get("input_fidelity", "low"),
            
            # Conversation mode
            "conversation_history": kwargs.get("conversation_history", "[]"),
            "previous_response_id": kwargs.get("previous_response_id", ""),
            
            # Generation settings
            "seed": kwargs.get("seed", -1),
            "negative_prompt": kwargs.get("negative_prompt", ""),
            "additional_modifiers": kwargs.get("additional_modifiers", ""),
            "custom_instructions": kwargs.get("custom_instructions", "")
        }
        
        # Run the model
        output = self.client.run(
            self.model,
            input=input_params
        )
        
        return output


# Example usage functions
def basic_example():
    """Simple image generation"""
    print("\n🎨 Basic Example: Simple Generation")
    print("-" * 50)
    
    generator = BetterGPTImage(REPLICATE_API_TOKEN, OPENAI_API_KEY)
    
    result = generator.generate(
        prompt="A peaceful zen garden with cherry blossoms",
        style_preset="photorealistic"
    )
    
    print(f"Generated {len(result)} image(s)")
    for i, url in enumerate(result, 1):
        print(f"Image {i}: {url}")
    
    return result


def anime_style_example():
    """Generate anime-style artwork"""
    print("\n🎌 Anime Style Example")
    print("-" * 50)
    
    generator = BetterGPTImage(REPLICATE_API_TOKEN, OPENAI_API_KEY)
    
    result = generator.generate(
        prompt="A magical girl with her spirit companion",
        style_preset="ghibli",
        size="1536x1024",
        quality="high",
        additional_modifiers="studio quality, movie poster"
    )
    
    print(f"Generated Ghibli-style image: {result[0]}")
    return result


def concept_art_example():
    """Generate concept art for games/movies"""
    print("\n🎮 Concept Art Example")
    print("-" * 50)
    
    generator = BetterGPTImage(REPLICATE_API_TOKEN, OPENAI_API_KEY)
    
    result = generator.generate(
        prompt="Ancient alien temple hidden in a jungle",
        style_preset="concept_art",
        optimize_prompt=True,
        num_images=4,  # Generate variations
        quality="high",
        custom_instructions="Include atmospheric fog and dramatic lighting"
    )
    
    print(f"Generated {len(result)} concept art variations")
    return result


def custom_style_example():
    """Use custom style without presets"""
    print("\n🎨 Custom Style Example")
    print("-" * 50)
    
    generator = BetterGPTImage(REPLICATE_API_TOKEN, OPENAI_API_KEY)
    
    result = generator.generate(
        prompt="A steampunk airship docked at a floating city",
        style_preset="custom",
        optimize_prompt=True,
        custom_instructions="Combine Victorian elegance with brass machinery, Jules Verne inspired",
        negative_prompt="modern, plastic, neon",
        additional_modifiers="intricate details, brass and copper materials, steam clouds"
    )
    
    print(f"Generated custom style image: {result[0]}")
    return result


def batch_generation_example():
    """Generate multiple styles of the same subject"""
    print("\n📦 Batch Generation Example")
    print("-" * 50)
    
    generator = BetterGPTImage(REPLICATE_API_TOKEN, OPENAI_API_KEY)
    
    subject = "A majestic dragon perched on a mountain peak"
    styles = ["photorealistic", "oil_painting", "anime", "3d_render", "watercolor"]
    
    results = {}
    for style in styles:
        print(f"Generating {style} version...")
        result = generator.generate(
            prompt=subject,
            style_preset=style,
            optimize_prompt=True
        )
        results[style] = result[0]
        print(f"  ✓ {style}: {result[0]}")
    
    return results


def main():
    """Run all examples"""
    print("\n" + "=" * 60)
    print("🚀 Better GPT Image - Python Examples")
    print("=" * 60)
    
    # Run examples
    try:
        # 1. Basic generation
        basic_example()
        
        # 2. Anime style
        anime_style_example()
        
        # 3. Concept art
        concept_art_example()
        
        # 4. Custom style
        custom_style_example()
        
        # 5. Batch generation
        batch_generation_example()
        
        print("\n" + "=" * 60)
        print("✅ All examples completed successfully!")
        print("=" * 60)
        
    except Exception as e:
        print(f"\n❌ Error: {e}")
        print("\nTroubleshooting:")
        print("1. Check your API keys are valid")
        print("2. Ensure you have credits in both Replicate and OpenAI")
        print("3. Check the model is available at: https://replicate.com/preangelleo/better-gpt-image")


if __name__ == "__main__":
    main()