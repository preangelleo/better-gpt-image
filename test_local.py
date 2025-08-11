#!/usr/bin/env python3
"""
Interactive CLI for Better GPT Image
Test and use the tool locally with an interactive interface
"""

import os
import sys
import json
import time
from pathlib import Path
from datetime import datetime

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.prompt_optimizer import PromptOptimizer
from src.image_generator import ImageGenerator
from src.image_processor import ImageProcessor
from src.style_presets import get_style_list


class InteractiveCLI:
    """Interactive command-line interface for Better GPT Image"""
    
    def __init__(self):
        self.api_key = None
        self.optimizer = None
        self.generator = None
        self.processor = None
        self.use_gpt_image = False  # Toggle between responses API and images API
        self.optimization_model = "gpt-5"  # Default optimization model for responses API
        
        # Create necessary directories
        self.base_dir = Path(__file__).parent
        self.output_dir = self.base_dir / "output"
        self.input_dir = self.base_dir / "input"
        
        self.output_dir.mkdir(exist_ok=True)
        self.input_dir.mkdir(exist_ok=True)
        
        # Session timestamp for organizing outputs
        self.session_id = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.session_output = self.output_dir / self.session_id
        self.session_output.mkdir(exist_ok=True)
        
        print(f"\n📁 Output directory: {self.session_output}")
        print(f"📁 Input directory: {self.input_dir}")
    
    def check_api_key(self) -> bool:
        """Check for API key in environment variables"""
        self.api_key = os.getenv("OPENAI_API_KEY")
        
        if not self.api_key:
            print("\n❌ OpenAI API key not found in environment variables!")
            print("\n📝 To set your API key, use one of these methods:\n")
            print("   Method 1 - Temporary (current session only):")
            print("   macOS/Linux:")
            print("   $ export OPENAI_API_KEY='your-api-key-here'")
            print("   Windows:")
            print("   > set OPENAI_API_KEY=your-api-key-here\n")
            print("   Method 2 - Permanent (.env file):")
            print("   1. Create a .env file in this directory")
            print("   2. Add: OPENAI_API_KEY=your-api-key-here")
            print("   3. Install python-dotenv: pip install python-dotenv\n")
            
            # Ask if user wants to input key now (temporary)
            response = input("Would you like to enter your API key now? (y/n): ").strip().lower()
            if response == 'y':
                key = input("Enter your OpenAI API key: ").strip()
                if key:
                    self.api_key = key
                    os.environ["OPENAI_API_KEY"] = key
                    print("✅ API key set for this session")
                    return True
            return False
        
        print("✅ OpenAI API key found!")
        return True
    
    def initialize_components(self):
        """Initialize the AI components"""
        try:
            self.optimizer = PromptOptimizer(self.api_key, self.optimization_model)
            self.processor = ImageProcessor()
            self.generator = ImageGenerator(self.api_key)
            
            print("✅ Components initialized successfully!")
            print("   Using OpenAI Responses API (GPT-5) for image generation")
            print("   Alternative: gpt-image-1 API also available")
            
            return True
        except Exception as e:
            print(f"❌ Error initializing components: {e}")
            return False
    
    def show_menu(self):
        """Display main menu"""
        print("\n" + "="*60)
        print("🎨 BETTER GPT IMAGE - Interactive Mode")
        print("="*60)
        print("\n📋 Available Functions:")
        print("  1. Generate Image (Text to Image)")
        print("  2. Edit Image with Reference")
        print("  3. Inpaint with Mask")
        print("  4. Test Prompt Optimization Only")
        print("  5. View Cost Estimate")
        print("  6. Settings")
        print("  7. Help & Tips")
        print("  8. Exit")
        print("\n" + "-"*60)
    
    def generate_image(self):
        """Interactive image generation"""
        print("\n🎨 IMAGE GENERATION")
        print("-"*40)
        
        # Get prompt
        prompt = input("\n📝 Enter your prompt: ").strip()
        if not prompt:
            print("❌ Prompt cannot be empty!")
            return
        
        # Ask about optimization
        optimize = input("✨ Optimize prompt? (y/n) [y]: ").strip().lower()
        optimize = optimize != 'n'
        
        # If optimizing, ask which model to use
        optimization_model = None
        if optimize:
            print("\n🤖 Select optimization model:")
            print("  1. GPT-5 (latest, most advanced - recommended)")
            print("  2. GPT-4.1 (balanced, reliable)")
            
            model_choice = input("Select model (1-2) [1]: ").strip()
            if model_choice == "2":
                optimization_model = "gpt-4.1"
            else:
                optimization_model = "gpt-5"  # Default - latest and best
        
        # Style selection
        style = None
        if optimize:
            print("\n🎨 Available styles (showing first 20):")
            all_styles = get_style_list()
            # Show first 20 popular styles plus custom option
            display_styles = ["none"] + all_styles[:20] + ["custom"]
            
            for i, s in enumerate(display_styles):
                if i % 3 == 0:
                    print()
                print(f"  {i:2}. {s:20}", end="")
            
            print("\n\n  📝 For full list of 90+ styles, type 'list'")
            print("  ✏️ For custom style, select 'custom' option")
            
            style_input = input("\nSelect style number or type 'list': ").strip()
            
            if style_input.lower() == 'list':
                # Show all styles
                print("\n📚 ALL AVAILABLE STYLES:")
                print("=" * 60)
                for i, s in enumerate(all_styles):
                    if i % 3 == 0:
                        print()
                    print(f"  {s:20}", end="")
                print("\n" + "=" * 60)
                
                style_input = input("\nNow select style or type name: ").strip()
            
            # Process selection
            if style_input.isdigit():
                style_idx = int(style_input)
                if 0 <= style_idx < len(display_styles):
                    style = display_styles[style_idx]
                else:
                    style = "none"
            elif style_input in all_styles:
                style = style_input
            else:
                style = "none"
            
            # Handle custom style
            if style == "custom":
                custom_style = input("\n✏️ Enter your custom style: ").strip()
                if custom_style:
                    style = custom_style
                else:
                    style = "none"
        
        # Size selection
        print("\n📐 Available sizes:")
        sizes = ["1024x1024", "1536x1024", "1024x1536"]
        for i, s in enumerate(sizes):
            print(f"  {i}. {s}")
        
        size_choice = input("Select size (0-2) [0]: ").strip()
        try:
            size_idx = int(size_choice) if size_choice else 0
            size = sizes[size_idx] if 0 <= size_idx < len(sizes) else "1024x1024"
        except:
            size = "1024x1024"
        
        # Quality selection
        quality_choice = input("\n💎 Quality (low/medium/high) [high]: ").strip().lower()
        quality = quality_choice if quality_choice in ["low", "medium", "high"] else "high"
        
        # Number of images
        num_str = input("🔢 Number of images (1-4) [1]: ").strip()
        try:
            num_images = int(num_str) if num_str else 1
            num_images = max(1, min(4, num_images))
        except:
            num_images = 1
        
        # Post-processing options
        print("\n📸 Post-processing options:")
        compress_choice = input("  Compress to JPG? (y/n) [n]: ").strip().lower()
        compress_to_jpg = compress_choice == 'y'
        
        crop_choice = input("  Auto-crop to 16:9/9:16? (y/n) [n]: ").strip().lower()
        crop_to_16_9 = crop_choice == 'y'
        
        jpg_quality = 90
        if compress_to_jpg:
            quality_str = input("  JPG quality (1-100) [90]: ").strip()
            try:
                jpg_quality = int(quality_str) if quality_str else 90
                jpg_quality = max(1, min(100, jpg_quality))
            except:
                jpg_quality = 90
        
        # Process prompt if optimization requested
        final_prompt = prompt
        if optimize:
            print("\n⚙️ Optimizing prompt...")
            try:
                enhanced, negative, metadata = self.optimizer.enhance_prompt(
                    prompt,
                    style_preset=style if style != "none" else None,
                    use_gpt_enhancement=True,
                    optimization_model=optimization_model
                )
                final_prompt = enhanced
                print(f"\n✨ Enhanced prompt: {final_prompt[:200]}...")
                if negative:
                    print(f"⛔ Suggested negative: {negative}")
            except Exception as e:
                print(f"⚠️ Optimization failed, using original prompt: {e}")
        
        # Ask which API to use
        print("\n🔧 Select API mode:")
        print("  1. Direct gpt-image-1 API (faster, single generation)")
        print("  2. GPT-5 responses API (supports multi-turn conversation)")
        
        api_choice = input("Select API (1-2) [1]: ").strip()
        use_gpt_image = api_choice != "2"  # Use direct API unless user chooses responses API
        
        # Calculate and show cost estimate
        cost_est = self.generator.calculate_cost(
            size=size, 
            quality=quality, 
            n=num_images,
            model="gpt-image-1" if use_gpt_image else "gpt-5"
        )
        print(f"\n💰 Cost Estimate:")
        print(f"   Output tokens: {cost_est['output_tokens']:,}")
        print(f"   Total cost: {cost_est['total_cost']}")
        print(f"   Per image: {cost_est['cost_breakdown']['price_per_image']}")
        
        proceed = input("\n🚀 Generate image(s)? (y/n) [y]: ").strip().lower()
        if proceed == 'n':
            print("❌ Generation cancelled")
            return
        
        # Store cost for filename
        cost_cents = cost_est['total_cents']
        
        # Generate
        print("\n🎨 Generating image(s)...")
        print(f"   Using: {'gpt-image-1 API (direct call)' if use_gpt_image else 'GPT-5 Responses API (with conversation support)'}")
        
        try:
            result = self.generator.generate_image(
                prompt=final_prompt,
                size=size,
                quality=quality,
                n=num_images,
                use_gpt_image=use_gpt_image,
                model="gpt-5" if not use_gpt_image else None,
                compress_to_jpg=compress_to_jpg,
                crop_to_16_9=crop_to_16_9,
                jpg_quality=jpg_quality
            )
            
            if result["success"]:
                print(f"\n✅ Successfully generated {len(result['images'])} image(s)!")
                
                # Save images
                saved_files = []
                for i, img_data in enumerate(result["images"]):
                    if "b64_json" in img_data:
                        # Determine file extension based on format
                        ext = "jpg" if compress_to_jpg else "png"
                        # Include cost in filename (e.g., generated_1_165c.png for $1.65)
                        filename = f"generated_{i+1}_{cost_cents}c.{ext}"
                        filepath = self.session_output / filename
                        
                        self.generator.save_image(img_data["b64_json"], filepath)
                        saved_files.append(filepath)
                        print(f"  💾 Saved: {filepath}")
                        
                        # Show processing info if applied
                        if img_data.get("format"):
                            print(f"     Format: {img_data['format']}")
                        if img_data.get("dimensions"):
                            print(f"     Dimensions: {img_data['dimensions']}")
                        if img_data.get("aspect_ratio"):
                            print(f"     Aspect Ratio: {img_data['aspect_ratio']}")
                        
                        if img_data.get("revised_prompt"):
                            print(f"  📝 Revised: {img_data['revised_prompt'][:100]}...")
                
                # Save metadata
                metadata_file = self.session_output / f"metadata_{int(time.time())}.json"
                with open(metadata_file, "w") as f:
                    json.dump({
                        "original_prompt": prompt,
                        "final_prompt": final_prompt,
                        "settings": {
                            "size": size,
                            "quality": quality,
                            "style": style,
                            "num_images": num_images,
                            "compress_to_jpg": compress_to_jpg,
                            "crop_to_16_9": crop_to_16_9,
                            "jpg_quality": jpg_quality if compress_to_jpg else None
                        },
                        "post_processing": result.get("processing_applied", []),
                        "files": [str(f) for f in saved_files],
                        "result": result["metadata"]
                    }, f, indent=2)
                print(f"  📊 Metadata: {metadata_file}")
                
            else:
                print(f"❌ Generation failed: {result.get('error')}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def edit_image_with_reference(self):
        """Edit image using reference images"""
        print("\n✏️ IMAGE EDITING WITH REFERENCE")
        print("-"*40)
        
        # List available input images
        input_images = list(self.input_dir.glob("*"))
        image_files = [f for f in input_images if f.suffix.lower() in ['.png', '.jpg', '.jpeg', '.webp']]
        
        if not image_files:
            print(f"\n❌ No images found in {self.input_dir}")
            print(f"   Please copy your reference images to: {self.input_dir}")
            return
        
        print("\n📸 Available reference images:")
        for i, img in enumerate(image_files):
            print(f"  {i+1}. {img.name}")
        
        # Select images
        selected_images = []
        while True:
            choice = input("\nSelect image number (or 'done' to finish): ").strip()
            if choice.lower() == 'done':
                break
            try:
                idx = int(choice) - 1
                if 0 <= idx < len(image_files):
                    selected_images.append(image_files[idx])
                    print(f"  ✅ Added: {image_files[idx].name}")
            except:
                print("  ⚠️ Invalid selection")
        
        if not selected_images:
            print("❌ No images selected")
            return
        
        print(f"\n✅ Selected {len(selected_images)} reference image(s)")
        
        # Get edit prompt
        prompt = input("\n📝 Describe the edit you want: ").strip()
        if not prompt:
            print("❌ Edit description cannot be empty!")
            return
        
        # Input fidelity
        fidelity = input("🎯 Input fidelity (low/high) [low]: ").strip().lower()
        fidelity = "high" if fidelity == "high" else "low"
        
        # Calculate cost for editing (assume medium quality for reference)
        cost_est = self.generator.calculate_cost(
            size="1024x1024",
            quality="medium",
            n=1,
            input_image_tokens=1000 * len(selected_images),  # Estimate for input images
            model="gpt-4.1"
        )
        cost_cents = cost_est['total_cents']
        
        print(f"\n💰 Estimated cost: {cost_est['total_cost']}")
        
        # Generate
        print("\n✏️ Editing image...")
        try:
            # Process reference images and convert to base64
            reference_images = []
            for img_path in selected_images:
                # Convert image to base64
                b64_data = self.generator.image_to_base64(str(img_path))
                reference_images.append({"base64": b64_data})
            
            result = self.generator.edit_image_with_reference(
                prompt=prompt,
                reference_images=reference_images,
                input_fidelity=fidelity,
                quality="high",
                model="gpt-4.1"
            )
            
            if result["success"]:
                print(f"\n✅ Edit successful!")
                
                # Save result
                for i, img_data in enumerate(result["images"]):
                    if "b64_json" in img_data:
                        # Include cost in filename
                        filename = f"edited_{i+1}_{cost_cents}c.png"
                        filepath = self.session_output / filename
                        
                        self.generator.save_image(img_data["b64_json"], filepath)
                        print(f"  💾 Saved: {filepath}")
            else:
                print(f"❌ Edit failed: {result.get('error')}")
                
        except Exception as e:
            print(f"❌ Error: {e}")
    
    def test_prompt_optimization(self):
        """Test prompt optimization without generating images"""
        print("\n✨ PROMPT OPTIMIZATION ONLY")
        print("-"*40)
        
        prompt = input("\n📝 Enter prompt to optimize: ").strip()
        if not prompt:
            print("❌ Prompt cannot be empty!")
            return
        
        # Ask if user wants to use GPT optimization
        use_gpt = input("\n🤖 Use GPT for intelligent optimization? (y/n) [y]: ").strip().lower()
        use_gpt_enhancement = use_gpt != 'n'
        
        # Select style
        print("\n🎨 Select style preset:")
        styles = ["photorealistic", "cinematic", "anime", "oil_painting", 
                 "watercolor", "3d_render", "concept_art", "cyberpunk", 
                 "impressionist", "none", "custom"]
        
        for i, style in enumerate(styles):
            print(f"  {i}. {style}")
        
        style_choice = input("\nSelect style (0-10) [0]: ").strip()
        try:
            style_idx = int(style_choice) if style_choice else 0
            selected_style = styles[style_idx] if 0 <= style_idx < len(styles) else "photorealistic"
        except:
            selected_style = "photorealistic"
        
        # Handle custom style
        if selected_style == "custom":
            custom_style = input("\n✏️ Enter your custom style: ").strip()
            selected_style = custom_style if custom_style else "photorealistic"
        
        style_to_apply = None if selected_style == "none" else selected_style
        
        # Select optimization model
        optimization_model = "gpt-5"  # Default to latest
        if use_gpt_enhancement:
            print("\n🧠 Select optimization model:")
            print("  1. GPT-5 (latest, most advanced)")
            print("  2. GPT-4.1 (balanced, reliable)")
            
            model_choice = input("Select model (1-2) [1]: ").strip()
            if model_choice == "2":
                optimization_model = "gpt-4.1"
            # Default is GPT-5
        
        print(f"\n⚙️ Optimizing with {selected_style if selected_style else 'no'} style...")
        if use_gpt_enhancement:
            print(f"   Using {optimization_model} for enhancement")
        else:
            print("   Using rule-based enhancement (no GPT)")
        
        try:
            # Perform optimization
            enhanced, negative, metadata = self.optimizer.enhance_prompt(
                prompt,
                style_preset=style_to_apply,
                use_gpt_enhancement=use_gpt_enhancement,
                optimization_model=optimization_model,
                add_quality_modifiers=True
            )
            
            # Display results
            print("\n" + "="*60)
            print("OPTIMIZATION RESULTS")
            print("="*60)
            
            print(f"\n📝 ORIGINAL PROMPT:")
            print(f"   {prompt}")
            
            print(f"\n✨ ENHANCED PROMPT:")
            print(f"   {enhanced}")
            
            if negative:
                print(f"\n⛔ NEGATIVE PROMPT (auto-generated):")
                print(f"   {negative}")
            
            # Show metadata
            print(f"\n📊 METADATA:")
            print(f"   Original length: {len(prompt)} chars")
            print(f"   Enhanced length: {len(enhanced)} chars")
            print(f"   Enhancement ratio: {len(enhanced)/len(prompt):.1f}x")
            if metadata.get('gpt_enhanced'):
                print(f"   GPT enhanced: Yes ({metadata.get('optimization_model', 'unknown')})")
            else:
                print(f"   GPT enhanced: No (rule-based)")
            if metadata.get('applied_style'):
                print(f"   Applied style: {metadata['applied_style']}")
            
            # Save results
            results_file = self.session_output / f"optimized_prompt_{int(time.time())}.txt"
            with open(results_file, "w") as f:
                f.write("# Prompt Optimization Results\n")
                f.write(f"Generated: {time.strftime('%Y-%m-%d %H:%M:%S')}\n\n")
                f.write(f"## Original Prompt:\n{prompt}\n\n")
                f.write(f"## Enhanced Prompt:\n{enhanced}\n\n")
                if negative:
                    f.write(f"## Negative Prompt:\n{negative}\n\n")
                f.write(f"## Settings:\n")
                f.write(f"- Style: {selected_style}\n")
                f.write(f"- GPT Enhancement: {use_gpt_enhancement}\n")
                if use_gpt_enhancement:
                    f.write(f"- Model: {optimization_model}\n")
                f.write(f"- Original Length: {len(prompt)} chars\n")
                f.write(f"- Enhanced Length: {len(enhanced)} chars\n")
                f.write(f"- Enhancement Ratio: {len(enhanced)/len(prompt):.1f}x\n")
            
            print(f"\n💾 Results saved to: {results_file}")
            
            # Ask if user wants to copy to clipboard (optional)
            copy_choice = input("\n📋 Copy enhanced prompt to clipboard? (y/n) [n]: ").strip().lower()
            if copy_choice == 'y':
                try:
                    import pyperclip
                    pyperclip.copy(enhanced)
                    print("✅ Enhanced prompt copied to clipboard!")
                except ImportError:
                    print("⚠️ pyperclip not installed. Install with: pip install pyperclip")
                except Exception as e:
                    print(f"⚠️ Could not copy to clipboard: {e}")
        
        except Exception as e:
            print(f"❌ Optimization failed: {e}")
    
    def show_help(self):
        """Display help and tips"""
        print("\n" + "="*60)
        print("📚 HELP & TIPS")
        print("="*60)
        
        print("\n🎯 Prompt Tips:")
        print("  • Be specific about what you want")
        print("  • Include style, mood, and atmosphere")
        print("  • Mention lighting and composition")
        print("  • Specify camera angle for scenes")
        
        print("\n🎨 Style Guide:")
        print("  • Photorealistic: Best for real-world subjects")
        print("  • Cinematic: Great for dramatic scenes")
        print("  • Anime: Perfect for characters and fantasy")
        print("  • Oil Painting: Classical artistic look")
        print("  • 3D Render: Product shots and architecture")
        print("  • Concept Art: Game and movie designs")
        
        print("\n📁 File Management:")
        print(f"  • Input images go in: {self.input_dir}")
        print(f"  • Generated images saved to: {self.output_dir}")
        print("  • Each session creates a timestamped folder")
        
        print("\n💰 Cost Optimization:")
        print("  • Low quality: 272-408 tokens")
        print("  • Medium quality: 1,056-1,584 tokens")
        print("  • High quality: 4,160-6,240 tokens")
        
        input("\nPress Enter to continue...")
    
    def show_settings(self):
        """Show and modify settings"""
        print("\n" + "="*60)
        print("⚙️ SETTINGS")
        print("="*60)
        
        print(f"\n📝 Current Optimization Model: {self.optimization_model}")
        print("\nAvailable models (for responses API):")
        print("  1. GPT-4.1 (faster, balanced)")
        print("  2. GPT-4 (stable)")
        print("  3. GPT-5 (best quality, recommended)")
        print("\nNote: gpt-4-mini only works with chat API, not responses API")
        
        change = input("\nChange model? (y/n) [n]: ").strip().lower()
        if change == 'y':
            choice = input("Select new model (1-3): ").strip()
            if choice == "1":
                self.optimization_model = "gpt-4.1"
                print("✅ Changed to GPT-4.1")
            elif choice == "2":
                self.optimization_model = "gpt-4"
                print("✅ Changed to GPT-4")
            else:
                self.optimization_model = "gpt-5"
                print("✅ Changed to GPT-5")
            
            # Reinitialize optimizer with new model
            self.optimizer = PromptOptimizer(self.api_key, self.optimization_model)
            print("✅ Optimizer reinitialized with new model")
        
        input("\nPress Enter to continue...")
    
    def run(self):
        """Main interaction loop"""
        print("\n" + "="*60)
        print("🚀 BETTER GPT IMAGE - Interactive CLI")
        print("="*60)
        
        # Check API key
        if not self.check_api_key():
            print("\n❌ Cannot proceed without API key")
            return
        
        # Initialize components
        print("\n⚙️ Initializing components...")
        if not self.initialize_components():
            print("\n❌ Failed to initialize. Please check your API key.")
            return
        
        # Main loop
        while True:
            self.show_menu()
            
            choice = input("\n👉 Select option (1-8): ").strip()
            
            if choice == "1":
                self.generate_image()
            elif choice == "2":
                self.edit_image_with_reference()
            elif choice == "3":
                print("\n🚧 Mask inpainting coming soon!")
                print("   For now, use edit with reference")
            elif choice == "4":
                self.test_prompt_optimization()
            elif choice == "5":
                # Show cost estimate
                print("\n💰 TOKEN USAGE ESTIMATES")
                print("-"*40)
                for size in ["1024x1024", "1536x1024", "1024x1536"]:
                    print(f"\n📐 Size: {size}")
                    for quality in ["low", "medium", "high"]:
                        est = self.generator.estimate_cost(size, quality, 1)
                        print(f"  {quality:8} : {est['output_tokens']:,} tokens")
            elif choice == "6":
                self.show_settings()
            elif choice == "7":
                self.show_help()
            elif choice == "8":
                print("\n👋 Goodbye!")
                print(f"📁 Your outputs are in: {self.output_dir}")
                break
            else:
                print("⚠️ Invalid option. Please try again.")


def main():
    """Entry point"""
    # Try to load .env file if it exists
    try:
        from dotenv import load_dotenv
        load_dotenv()
    except ImportError:
        pass  # dotenv not installed, will use system env vars
    
    cli = InteractiveCLI()
    try:
        cli.run()
    except KeyboardInterrupt:
        print("\n\n👋 Interrupted by user. Goodbye!")
    except Exception as e:
        print(f"\n❌ Unexpected error: {e}")
        import traceback
        traceback.print_exc()


if __name__ == "__main__":
    main()