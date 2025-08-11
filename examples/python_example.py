#!/usr/bin/env python3
"""
Better GPT Image - Python Usage Examples
Complete examples showing all features and usage patterns
"""

import os
import sys
import json
from pathlib import Path

# Add parent directory to path for imports
sys.path.append(str(Path(__file__).parent.parent))

from src.prompt_optimizer import PromptOptimizer
from src.image_generator import ImageGenerator
from src.image_processor import ImageProcessor
from src.style_presets import get_style_list

# Get API key from environment
API_KEY = os.getenv("OPENAI_API_KEY")
if not API_KEY:
    print("Please set your OPENAI_API_KEY environment variable")
    sys.exit(1)

def example_basic_generation():
    """Example 1: Basic image generation with style preset"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Basic Image Generation")
    print("="*60)
    
    # Initialize components
    optimizer = PromptOptimizer(API_KEY)
    generator = ImageGenerator(API_KEY)
    
    # Original prompt
    prompt = "A serene Japanese garden with koi pond"
    print(f"Original prompt: {prompt}")
    
    # Enhance the prompt
    enhanced_prompt, negative_prompt, metadata = optimizer.enhance_prompt(
        prompt=prompt,
        style_preset="photorealistic",
        optimize_prompt=True
    )
    
    print(f"\nEnhanced prompt: {enhanced_prompt}")
    if negative_prompt:
        print(f"Negative prompt: {negative_prompt}")
    
    # Generate image
    result = generator.generate_image(
        prompt=enhanced_prompt,
        size="1024x1024",
        quality="high"
    )
    
    if result["success"]:
        # Save the image
        output_path = "output/example1_japanese_garden.png"
        os.makedirs("output", exist_ok=True)
        generator.save_image(result["images"][0]["b64_json"], output_path)
        print(f"\n✅ Image saved to: {output_path}")
    else:
        print(f"\n❌ Generation failed: {result.get('error')}")
    
    return result

def example_multiple_styles():
    """Example 2: Generate same subject in multiple styles"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Multiple Style Variations")
    print("="*60)
    
    optimizer = PromptOptimizer(API_KEY)
    generator = ImageGenerator(API_KEY)
    
    # Base prompt
    base_prompt = "A majestic phoenix rising from flames"
    styles = ["photorealistic", "anime", "oil_painting", "3d_render", "watercolor"]
    
    results = []
    for style in styles:
        print(f"\n🎨 Generating {style} version...")
        
        # Enhance with specific style
        enhanced_prompt, _, _ = optimizer.enhance_prompt(
            prompt=base_prompt,
            style_preset=style,
            optimize_prompt=True
        )
        
        # Generate image
        result = generator.generate_image(
            prompt=enhanced_prompt,
            size="1024x1024",
            quality="medium"
        )
        
        if result["success"]:
            # Save with style name
            output_path = f"output/example2_phoenix_{style}.png"
            os.makedirs("output", exist_ok=True)
            generator.save_image(result["images"][0]["b64_json"], output_path)
            print(f"   ✅ Saved to: {output_path}")
            results.append({"style": style, "path": output_path})
        else:
            print(f"   ❌ Failed: {result.get('error')}")
    
    return results

def example_anime_style():
    """Example 3: Anime/Ghibli style generation"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Anime/Ghibli Style")
    print("="*60)
    
    optimizer = PromptOptimizer(API_KEY)
    generator = ImageGenerator(API_KEY)
    
    prompt = "A flying castle in the clouds"
    
    # Enhance with Ghibli style
    enhanced_prompt, negative_prompt, metadata = optimizer.enhance_prompt(
        prompt=prompt,
        style_preset="ghibli",
        optimize_prompt=True,
        add_quality_modifiers=True
    )
    
    print(f"Original: {prompt}")
    print(f"Enhanced: {enhanced_prompt}")
    
    # Generate with high quality
    result = generator.generate_image(
        prompt=enhanced_prompt,
        size="1536x1024",  # Wide aspect ratio
        quality="high"
    )
    
    if result["success"]:
        output_path = "output/example3_ghibli_castle.png"
        os.makedirs("output", exist_ok=True)
        generator.save_image(result["images"][0]["b64_json"], output_path)
        print(f"\n✅ Ghibli-style image saved to: {output_path}")
    
    return result

def example_concept_art():
    """Example 4: Game concept art with multiple variations"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Game Concept Art")
    print("="*60)
    
    optimizer = PromptOptimizer(API_KEY)
    generator = ImageGenerator(API_KEY)
    
    prompt = "Alien marketplace on distant planet"
    
    # Generate multiple variations
    variations = optimizer.suggest_variations(prompt, num_variations=3)
    
    results = []
    for i, varied_prompt in enumerate(variations, 1):
        print(f"\n🎮 Variation {i}: {varied_prompt[:100]}...")
        
        result = generator.generate_image(
            prompt=varied_prompt,
            size="1024x1024",
            quality="high"
        )
        
        if result["success"]:
            output_path = f"output/example4_concept_art_v{i}.png"
            os.makedirs("output", exist_ok=True)
            generator.save_image(result["images"][0]["b64_json"], output_path)
            print(f"   ✅ Saved to: {output_path}")
            results.append(output_path)
    
    return results

def example_custom_style():
    """Example 5: Custom style without preset"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Custom Style")
    print("="*60)
    
    optimizer = PromptOptimizer(API_KEY)
    generator = ImageGenerator(API_KEY)
    
    # Custom prompt with specific instructions
    prompt = "Victorian steampunk laboratory"
    custom_instructions = "brass and copper machinery, vintage scientific equipment, warm lighting, intricate gears and pipes"
    negative_prompt = "modern, plastic, neon, minimalist"
    
    # Enhance without preset
    enhanced_prompt, _, metadata = optimizer.enhance_prompt(
        prompt=f"{prompt}, {custom_instructions}",
        style_preset=None,  # No preset
        optimize_prompt=True
    )
    
    print(f"Custom prompt: {enhanced_prompt[:150]}...")
    
    # Generate with custom settings
    result = generator.generate_image(
        prompt=enhanced_prompt,
        size="1024x1024",
        quality="high"
    )
    
    if result["success"]:
        output_path = "output/example5_steampunk_lab.png"
        os.makedirs("output", exist_ok=True)
        generator.save_image(result["images"][0]["b64_json"], output_path)
        print(f"\n✅ Custom style image saved to: {output_path}")
    
    return result

def example_cost_estimation():
    """Example 6: Cost estimation before generation"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Cost Estimation")
    print("="*60)
    
    generator = ImageGenerator(API_KEY)
    
    # Different configurations to estimate
    configs = [
        {"size": "1024x1024", "quality": "low", "n": 1},
        {"size": "1024x1024", "quality": "medium", "n": 1},
        {"size": "1024x1024", "quality": "high", "n": 1},
        {"size": "1536x1024", "quality": "high", "n": 2},
    ]
    
    print("\n💰 Cost Estimates:")
    print("-" * 50)
    
    for config in configs:
        cost_info = generator.calculate_cost(**config)
        print(f"\nConfig: {config}")
        print(f"  Output tokens: {cost_info['output_tokens']}")
        print(f"  Total cost: {cost_info['total_cost']}")
        print(f"  Cost breakdown: {cost_info['cost_breakdown']}")
    
    return configs

def example_edit_with_reference():
    """Example 7: Edit image with reference (requires input image)"""
    print("\n" + "="*60)
    print("EXAMPLE 7: Edit with Reference Image")
    print("="*60)
    
    generator = ImageGenerator(API_KEY)
    
    # Check if reference image exists
    reference_path = "input/reference.jpg"
    if not os.path.exists(reference_path):
        print(f"⚠️  Please place a reference image at: {reference_path}")
        print("   Skipping this example...")
        return None
    
    # Convert image to base64
    b64_image = generator.image_to_base64(reference_path)
    
    # Edit the image
    result = generator.edit_image_with_reference(
        prompt="Add a beautiful sunset in the background",
        reference_images=[{"base64": b64_image}],
        input_fidelity="high",
        quality="high"
    )
    
    if result["success"]:
        output_path = "output/example7_edited_with_sunset.png"
        os.makedirs("output", exist_ok=True)
        generator.save_image(result["images"][0]["b64_json"], output_path)
        print(f"\n✅ Edited image saved to: {output_path}")
    else:
        print(f"\n❌ Edit failed: {result.get('error')}")
    
    return result

def example_mask_editing():
    """Example 8: Mask-based inpainting"""
    print("\n" + "="*60)
    print("EXAMPLE 8: Mask-Based Editing")
    print("="*60)
    
    generator = ImageGenerator(API_KEY)
    processor = ImageProcessor()
    
    # Check if source image exists
    source_path = "input/source.jpg"
    if not os.path.exists(source_path):
        print(f"⚠️  Please place a source image at: {source_path}")
        print("   Skipping this example...")
        return None
    
    # Create a center mask
    mask_config = processor.create_mask(
        source_path,
        mask_type="center",
        mask_data={"size_ratio": 0.3}
    )
    
    # Convert image to base64
    b64_image = generator.image_to_base64(source_path)
    
    # Edit with mask
    result = generator.edit_image_with_reference(
        prompt="Replace with a blooming flower",
        reference_images=[{"base64": b64_image}],
        mask=mask_config,
        input_fidelity="high"
    )
    
    if result["success"]:
        output_path = "output/example8_masked_edit.png"
        os.makedirs("output", exist_ok=True)
        generator.save_image(result["images"][0]["b64_json"], output_path)
        print(f"\n✅ Masked edit saved to: {output_path}")
    
    return result

def example_list_all_styles():
    """Example 9: List all available style presets"""
    print("\n" + "="*60)
    print("EXAMPLE 9: Available Style Presets")
    print("="*60)
    
    styles = get_style_list()
    
    print(f"\n📚 Total styles available: {len(styles)}")
    print("\nCategories:")
    
    # Group styles by category (simplified)
    categories = {
        "Photography": ["photorealistic", "cinematic", "portrait", "landscape", "street_photography"],
        "Animation": ["anime", "ghibli", "pixar", "disney", "3d_cartoon"],
        "Traditional Art": ["oil_painting", "watercolor", "pencil_sketch", "charcoal", "pastel"],
        "Digital Art": ["3d_render", "concept_art", "digital_painting", "vector_art"],
        "Stylized": ["cyberpunk", "steampunk", "vaporwave", "synthwave", "retrowave"],
        "Historical": ["renaissance", "baroque", "impressionism", "art_nouveau", "gothic"]
    }
    
    for category, style_list in categories.items():
        available = [s for s in style_list if s in styles]
        if available:
            print(f"\n{category}:")
            for style in available:
                print(f"  - {style}")
    
    # Show remaining styles
    shown_styles = set(sum(categories.values(), []))
    remaining = [s for s in styles if s not in shown_styles]
    if remaining:
        print(f"\nOther styles ({len(remaining)}):")
        for i in range(0, min(10, len(remaining))):
            print(f"  - {remaining[i]}")
        if len(remaining) > 10:
            print(f"  ... and {len(remaining) - 10} more")
    
    return styles

def main():
    """Run all examples"""
    print("\n" + "🎨"*30)
    print(" BETTER GPT IMAGE - PYTHON EXAMPLES")
    print("🎨"*30)
    
    # Create necessary directories
    os.makedirs("input", exist_ok=True)
    os.makedirs("output", exist_ok=True)
    
    # Run examples
    examples = [
        ("Basic Generation", example_basic_generation),
        ("Multiple Styles", example_multiple_styles),
        ("Anime/Ghibli Style", example_anime_style),
        ("Concept Art", example_concept_art),
        ("Custom Style", example_custom_style),
        ("Cost Estimation", example_cost_estimation),
        ("Edit with Reference", example_edit_with_reference),
        ("Mask Editing", example_mask_editing),
        ("List All Styles", example_list_all_styles),
    ]
    
    print("\nSelect an example to run:")
    for i, (name, _) in enumerate(examples, 1):
        print(f"{i}. {name}")
    print("0. Run all examples")
    
    try:
        choice = input("\nEnter your choice (0-9): ").strip()
        
        if choice == "0":
            # Run all examples
            for name, func in examples:
                try:
                    func()
                except Exception as e:
                    print(f"\n❌ Error in {name}: {e}")
        elif choice.isdigit() and 1 <= int(choice) <= len(examples):
            # Run selected example
            idx = int(choice) - 1
            name, func = examples[idx]
            func()
        else:
            print("Invalid choice")
    
    except KeyboardInterrupt:
        print("\n\n👋 Goodbye!")
    except Exception as e:
        print(f"\n❌ Error: {e}")
    
    print("\n" + "="*60)
    print("✅ Examples completed!")
    print(f"📁 Check the 'output/' folder for generated images")
    print("="*60)

if __name__ == "__main__":
    main()