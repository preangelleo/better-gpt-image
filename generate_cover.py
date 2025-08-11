#!/usr/bin/env python3
"""
Generate a cover image for Better GPT Image on Replicate
"""

import os
import sys
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.append(str(Path(__file__).parent))

from src.prompt_optimizer import PromptOptimizer
from src.image_generator import ImageGenerator

def get_api_key():
    """Get API key from environment or user input"""
    api_key = os.getenv("OPENAI_API_KEY")
    
    if not api_key:
        print("\n🔑 OpenAI API Key Required")
        print("=" * 50)
        print("Please provide your OpenAI API key to generate the cover image.")
        print("Your key will only be used for this generation and not stored.")
        print("\nGet your API key at: https://platform.openai.com/api-keys")
        api_key = input("\nEnter your OpenAI API key: ").strip()
        
        if not api_key:
            print("❌ No API key provided. Exiting.")
            sys.exit(1)
    
    return api_key

def main():
    """Generate cover image for Replicate"""
    
    print("\n" + "=" * 60)
    print("🎨 Better GPT Image - Cover Image Generator")
    print("=" * 60)
    
    # Get API key
    api_key = get_api_key()
    
    # The prompt showcases our model's capabilities
    cover_prompt = """
    A stunning visualization of AI-powered artistic transformation: A magical digital canvas 
    floating in a creative workspace, displaying a morphing collage that seamlessly transitions 
    between multiple art styles - photorealistic portrait melting into anime character, 
    oil painting flowing into 3D render, watercolor blending with cyberpunk neon art. 
    Surrounding the canvas are floating holographic UI elements showing style presets like 
    'Ghibli', 'Pixar', 'Renaissance', 'Cyberpunk'. Ethereal light rays and digital particles 
    create a sense of creative energy. The entire scene has a premium, professional quality 
    with cinematic lighting and composition. Include subtle text 'Better GPT Image' integrated 
    artistically into the scene.
    """
    
    # Use cinematic concept art style for professional look
    style_preset = "concept_art"
    
    print("\n📝 Generating cover image with theme:")
    print("   'AI-Powered Artistic Transformation'")
    print(f"   Style: {style_preset}")
    print("   Size: 1536x1024 (landscape)")
    
    try:
        # Initialize components
        print("\n🚀 Initializing Better GPT Image components...")
        optimizer = PromptOptimizer(api_key, "gpt-4")
        generator = ImageGenerator(api_key)
        
        # Enhance the prompt
        print("✨ Enhancing prompt for optimal results...")
        enhanced_prompt, negative_prompt, metadata = optimizer.enhance_prompt(
            cover_prompt,
            style_preset=style_preset,
            add_quality_modifiers=True,
            use_gpt_enhancement=True
        )
        
        print("\n🎨 Generating cover image...")
        print("   This may take 30-60 seconds...")
        
        # Generate the image
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        output_dir = Path("cover_images")
        output_dir.mkdir(exist_ok=True)
        
        # Generate image using the enhanced prompt
        from openai import OpenAI
        client = OpenAI(api_key=api_key)
        
        response = client.images.generate(
            model="dall-e-3",
            prompt=enhanced_prompt,
            size="1792x1024",  # DALL-E 3 landscape size
            quality="hd",
            n=1
        )
        
        # Download and save the image
        import requests
        from PIL import Image
        from io import BytesIO
        
        image_url = response.data[0].url
        img_response = requests.get(image_url)
        img = Image.open(BytesIO(img_response.content))
        
        # Save the image
        output_path = output_dir / f"replicate_cover_{timestamp}.png"
        img.save(output_path, "PNG")
        
        print(f"\n✅ Cover image generated successfully!")
        print(f"📁 Saved to: {output_path}")
        print("\n📤 Upload Instructions:")
        print("1. Open the image file: " + str(output_path.absolute()))
        print("2. Go to: https://replicate.com/preangelleo/better-gpt-image/settings")
        print("3. Click 'Choose File' under Cover Image")
        print("4. Select the generated image")
        print("5. Click 'Save' to update your model")
        
        print("\n🎉 Your cover image showcases:")
        print("   ✓ Multiple artistic styles transformation")
        print("   ✓ Professional quality output")
        print("   ✓ AI-powered creativity")
        print("   ✓ The power of Better GPT Image")
        
        return str(output_path)
        
    except Exception as e:
        print(f"\n❌ Error generating cover image: {e}")
        print("\nTroubleshooting:")
        print("1. Check your API key is valid")
        print("2. Ensure you have sufficient OpenAI credits")
        print("3. Try running again if it was a temporary error")
        return None

if __name__ == "__main__":
    result = main()
    if result:
        print("\n" + "=" * 60)
        print("✨ Cover image ready for Replicate!")
        print("=" * 60)