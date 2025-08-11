"""
Replicate Prediction Interface for Better GPT Image
"""

from cog import BasePredictor, Input, Path as CogPath
from typing import Optional, List
import os
import json
import base64
from pathlib import Path

from src.prompt_optimizer import PromptOptimizer
from src.image_generator import ImageGenerator
from src.image_processor import ImageProcessor
from src.style_presets import get_style_list, STYLE_PRESETS


class Predictor(BasePredictor):
    """Replicate predictor for Better GPT Image"""
    
    def setup(self):
        """Load model components into memory"""
        # Initialize processors (no API key needed yet)
        self.image_processor = ImageProcessor()
        print("Better GPT Image initialized and ready!")
    
    def predict(
        self,
        # API Configuration
        api_key: str = Input(
            description="Your OpenAI API key (required - will be masked for security)",
            default="",
            secret=True  # This makes the input masked with dots on Replicate
        ),
        
        # Basic Generation
        prompt: str = Input(
            description="Describe the image you want to generate",
            default=""
        ),
        
        # Prompt Optimization
        optimize_prompt: bool = Input(
            description="Automatically enhance your prompt for better results",
            default=True
        ),
        optimization_model: str = Input(
            description="Model to use for prompt optimization (responses API models)",
            default="gpt-5",
            choices=["gpt-4.1", "gpt-4", "gpt-5"]
        ),
        style_preset: str = Input(
            description="Apply a style preset or enter custom style. Choose from our curated collection of artistic styles.",
            default="none",
            choices=[
                "none",
                "photorealistic",
                "cinematic",
                "anime",
                "ghibli",
                "oil_painting",
                "watercolor",
                "digital_art",
                "3d_render",
                "3d_cartoon",
                "pixar",
                "disney",
                "dreamworks",
                "concept_art",
                "pencil_sketch",
                "ink_drawing",
                "comic_book",
                "manga",
                "makoto_shinkai",
                "kyoto_animation",
                "cyberpunk",
                "steampunk",
                "vaporwave",
                "synthwave",
                "minimalist",
                "pop_art",
                "art_nouveau",
                "art_deco",
                "impressionist",
                "expressionist",
                "surrealist",
                "abstract",
                "graffiti",
                "street_art",
                "low_poly",
                "isometric",
                "pixel_art",
                "retro_game",
                "ps1_graphics",
                "vintage_poster",
                "propaganda_poster",
                "psychedelic",
                "gothic",
                "dark_fantasy",
                "high_fantasy",
                "sci_fi",
                "horror",
                "romantic",
                "baroque",
                "renaissance",
                "neoclassical",
                "rococo",
                "brutalist",
                "bauhaus",
                "memphis_design",
                "flat_design",
                "material_design",
                "glassmorphism",
                "neumorphism",
                "skeuomorphism",
                "line_art",
                "continuous_line",
                "stipple",
                "pointillism",
                "charcoal_drawing",
                "pastel_art",
                "crayon",
                "colored_pencil",
                "marker_art",
                "acrylic_painting",
                "gouache",
                "tempera",
                "fresco",
                "encaustic",
                "spray_paint",
                "airbrush",
                "collage",
                "mixed_media",
                "origami",
                "paper_cut",
                "woodcut",
                "linocut",
                "etching",
                "lithograph",
                "screen_print",
                "risograph",
                "polaroid",
                "film_noir",
                "technicolor",
                "lomography",
                "double_exposure",
                "glitch_art",
                "list",
                "custom"
            ]
        ),
        
        # Image Settings
        size: str = Input(
            description="Image size",
            default="1024x1024",
            choices=["1024x1024", "1536x1024", "1024x1536"]
        ),
        quality: str = Input(
            description="Image quality (higher quality = more tokens)",
            default="high",
            choices=["low", "medium", "high"]
        ),
        background: str = Input(
            description="Background type",
            default="auto",
            choices=["auto", "transparent", "opaque"]
        ),
        
        # Advanced Options
        reference_images: str = Input(
            description="URLs or paths to reference images (comma-separated)",
            default=""
        ),
        mask_image: CogPath = Input(
            description="Mask image for inpainting (optional)",
            default=None
        ),
        input_fidelity: str = Input(
            description="How closely to preserve input image details",
            default="low",
            choices=["low", "high"]
        ),
        
        # Generation Options
        num_images: int = Input(
            description="Number of images to generate",
            default=1,
            ge=1,
            le=4
        ),
        seed: int = Input(
            description="Random seed for reproducibility (optional)",
            default=-1,
            ge=-1
        ),
        
        # Multi-turn Options
        previous_response_id: str = Input(
            description="Previous response ID for multi-turn editing",
            default=""
        ),
        conversation_history: str = Input(
            description="JSON string of conversation history for context",
            default="[]"
        )
    ) -> List[CogPath]:
        """Run a prediction on the model"""
        
        # Validate API key
        if not api_key or api_key == "your_api_key_here" or api_key == "":
            raise ValueError(
                "⚠️ OpenAI API key is required!\n\n"
                "Please provide your OpenAI API key to use this model.\n"
                "You can get your API key from: https://platform.openai.com/api-keys\n\n"
                "This model requires YOUR OWN API key for security and billing purposes.\n"
                "Your API key is never stored and is only used for this generation."
            )
        
        # Handle style list request
        if style_preset == "list":
            all_styles = get_style_list()
            print("\n📚 ALL AVAILABLE STYLES (90+ options):")
            print("=" * 60)
            for i, style in enumerate(all_styles):
                if i % 3 == 0:
                    print()
                print(f"  {style:20}", end="")
            print("\n" + "=" * 60)
            print("\n✏️ You can also use any custom style by typing it directly")
            raise ValueError("Style list displayed. Please run again with your chosen style.")
        
        # Initialize components with API key and optimization model
        prompt_optimizer = PromptOptimizer(api_key, optimization_model)
        image_generator = ImageGenerator(api_key)
        
        # Process prompt
        original_prompt = prompt
        negative_prompt = None
        metadata = {"original_prompt": original_prompt}
        
        if optimize_prompt and prompt:
            # Apply style preset if selected
            style_to_apply = None if style_preset == "none" else style_preset
            
            enhanced_prompt, negative_prompt, opt_metadata = prompt_optimizer.enhance_prompt(
                prompt,
                style_preset=style_to_apply,
                auto_detect_style=True,
                add_quality_modifiers=True,
                use_gpt_enhancement=True,
                optimization_model=optimization_model
            )
            prompt = enhanced_prompt
            metadata.update(opt_metadata)
            print(f"Enhanced prompt: {prompt[:200]}...")
            if negative_prompt:
                print(f"Suggested negative prompt: {negative_prompt}")
        
        # Process reference images if provided
        reference_image_data = []
        if reference_images and reference_images.strip():
            ref_paths = [p.strip() for p in reference_images.split(",")]
            for ref_path in ref_paths:
                if ref_path.startswith("http"):
                    # Handle URL - would need to download
                    print(f"URL reference images not yet supported: {ref_path}")
                else:
                    # Handle local file
                    try:
                        processed = self.image_processor.prepare_input_image(ref_path)
                        reference_image_data.append(processed)
                    except Exception as e:
                        print(f"Error processing reference image {ref_path}: {e}")
        
        # Process mask if provided
        mask_data = None
        if mask_image:
            try:
                mask_data = self.image_processor.add_alpha_channel(str(mask_image))
            except Exception as e:
                print(f"Error processing mask: {e}")
        
        # Parse conversation history
        conv_history = []
        if conversation_history and conversation_history != "[]":
            try:
                conv_history = json.loads(conversation_history)
            except:
                print("Could not parse conversation history")
        
        # Generate images
        output_paths = []
        
        try:
            # Determine generation mode
            if reference_image_data or mask_data:
                # Use edit mode
                print("Using edit mode with reference images/mask")
                result = image_generator.edit_image(
                    prompt=prompt,
                    images=reference_image_data if reference_image_data else [],
                    mask=mask_data,
                    size=size,
                    quality=quality,
                    input_fidelity=input_fidelity,
                    n=num_images
                )
            elif conv_history or previous_response_id:
                # Use multi-turn mode
                print("Using multi-turn generation mode")
                result = image_generator.multi_turn_generation(
                    conversation_history=conv_history,
                    new_prompt=prompt,
                    previous_response_id=previous_response_id if previous_response_id else None,
                    size=size,
                    quality=quality,
                    background=background
                )
            else:
                # Standard generation
                print("Using standard generation mode")
                result = image_generator.generate_image(
                    prompt=prompt,
                    size=size,
                    quality=quality,
                    n=num_images,
                    background=background if background != "auto" else None
                )
            
            # Process results
            if result["success"]:
                for i, img_data in enumerate(result["images"]):
                    # Save image
                    output_path = f"/tmp/output_{i}.png"
                    
                    if "b64_json" in img_data:
                        image_generator.save_image(img_data["b64_json"], output_path)
                    else:
                        print(f"No image data for image {i}")
                        continue
                    
                    output_paths.append(CogPath(output_path))
                    
                    # Log revised prompt if available
                    if img_data.get("revised_prompt"):
                        print(f"Revised prompt for image {i}: {img_data['revised_prompt'][:200]}...")
                
                # Log metadata
                print(f"Generation metadata: {json.dumps(result.get('metadata', {}), indent=2)}")
                
                # Estimate cost
                cost_estimate = image_generator.estimate_cost(
                    size=size,
                    quality=quality,
                    n=num_images,
                    input_images=len(reference_image_data),
                    high_fidelity=(input_fidelity == "high")
                )
                print(f"Token usage estimate: {json.dumps(cost_estimate, indent=2)}")
                
            else:
                error_msg = result.get("error", "Unknown error occurred")
                raise Exception(f"Generation failed: {error_msg}")
        
        except Exception as e:
            print(f"Error during generation: {str(e)}")
            raise
        
        if not output_paths:
            raise Exception("No images were generated")
        
        return output_paths