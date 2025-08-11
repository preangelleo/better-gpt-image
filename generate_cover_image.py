#!/usr/bin/env python3
"""
Generate a cover image for Better GPT Image on Replicate
This showcases the model's ability to create stunning images with various artistic styles
"""

import os
from datetime import datetime
from src.prompt_optimizer import PromptOptimizer
from src.image_generator import ImageGenerator
from image_optimizer_prompt import SYSTEM_PROMPT_STRUCTURED_IMAGE_DESCRIPTION

# Configuration
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    print("Please set OPENAI_API_KEY environment variable")
    exit(1)

# The prompt should showcase our model's capabilities
COVER_PROMPT = """
A magical artist's workshop where AI meets creativity: In the center, a glowing holographic canvas 
displays transforming artwork cycling through different styles - from photorealistic portraits to 
anime characters, oil paintings to 3D renders. Surrounding the canvas are floating art tools: 
traditional brushes mixing with digital styluses, paint palettes merging with color wheels, 
vintage easels beside futuristic tablets. The scene is bathed in ethereal light with particles 
of creativity floating in the air, rainbow prisms casting artistic shadows. The workshop has 
large windows showing different worlds outside - a cyberpunk city, a Ghibli forest, a Renaissance 
landscape. Text overlay reads 'Better GPT Image' in elegant, artistic lettering.
"""

# Style for the cover - let's use a cinematic/concept art style
STYLE_PRESET = "concept_art"

def generate_cover_image():
    """Generate the cover image for Replicate"""
    
    print("🎨 Generating Cover Image for Better GPT Image")
    print("=" * 60)
    
    # Initialize components
    optimizer = PromptOptimizer(API_KEY, "gpt-4")
    generator = ImageGenerator(API_KEY)
    
    # Enhance the prompt
    print("\n📝 Original Prompt:")
    print(COVER_PROMPT[:200] + "...")
    
    print("\n🚀 Enhancing prompt with GPT-4...")
    enhanced_prompt, negative_prompt, metadata = optimizer.enhance_prompt(
        COVER_PROMPT,
        style_preset=STYLE_PRESET,
        add_quality_modifiers=True,
        use_gpt_enhancement=True
    )
    
    print("\n✨ Enhanced Prompt:")
    print(enhanced_prompt[:300] + "...")
    
    # Generate the image in landscape format
    print("\n🎨 Generating image (1536x1024 landscape)...")
    image_path = generator.generate_image(
        prompt=enhanced_prompt,
        negative_prompt=negative_prompt,
        size="1536x1024",  # Landscape format for cover
        quality="high",
        num_images=1,
        style=STYLE_PRESET
    )
    
    if image_path:
        print(f"\n✅ Cover image generated successfully!")
        print(f"📁 Saved to: {image_path}")
        print("\n📤 Next steps:")
        print("1. Open the image file")
        print("2. Go to https://replicate.com/preangelleo/better-gpt-image/settings")
        print("3. Upload as Cover Image")
        return image_path
    else:
        print("\n❌ Failed to generate cover image")
        return None

if __name__ == "__main__":
    # Generate the cover image
    result = generate_cover_image()
    
    if result:
        print("\n🎉 Cover image ready for upload to Replicate!")
        print("This image showcases:")
        print("- Multiple artistic styles in one scene")
        print("- The transformation power of Better GPT Image")
        print("- Professional quality output")
        print("- Creative and technical capabilities")