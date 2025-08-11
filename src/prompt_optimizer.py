"""
Prompt Optimizer for Better GPT Image
Enhances user prompts for better image generation results
"""

import re
from typing import Dict, List, Optional, Tuple, Any
from openai import OpenAI
import json
from .style_presets import STYLE_PRESETS, get_style_list


class PromptOptimizer:
    """Optimizes prompts for image generation using GPT models"""
    
    # Default optimization model (can be overridden)
    # Using GPT-5 as default - works with responses API
    DEFAULT_OPTIMIZATION_MODEL = "gpt-5"  # GPT-5 works best with responses API
    
    def __init__(self, api_key: str, optimization_model: str = None):
        self.client = OpenAI(api_key=api_key)
        self.optimization_model = optimization_model or self.DEFAULT_OPTIMIZATION_MODEL
        
        # Use comprehensive style presets from style_presets.py
        self.style_presets = STYLE_PRESETS
        
        # Quality enhancers
        self.quality_enhancers = [
            "highly detailed",
            "intricate details",
            "professional quality",
            "stunning composition",
            "perfect lighting"
        ]
        
        # Negative prompt suggestions
        self.negative_suggestions = {
            "photorealistic": ["cartoon", "anime", "illustration", "painting", "low quality", "blurry"],
            "anime": ["realistic", "photograph", "3d render", "western cartoon"],
            "oil_painting": ["digital art", "3d render", "photograph", "modern art"],
            "3d_render": ["2d", "flat", "painting", "photograph", "hand-drawn"]
        }

    def analyze_intent(self, prompt: str) -> Dict[str, any]:
        """Analyze user intent from the prompt"""
        intent = {
            "style": None,
            "subject": None,
            "mood": None,
            "technical_requirements": [],
            "detected_language": "en"
        }
        
        # Detect style keywords
        prompt_lower = prompt.lower()
        for style, keywords in {
            "photorealistic": ["photo", "realistic", "real", "photography"],
            "cinematic": ["cinematic", "movie", "film", "dramatic"],
            "anime": ["anime", "manga", "kawaii", "chibi"],
            "oil_painting": ["oil painting", "painting", "traditional art", "canvas"],
            "3d_render": ["3d", "render", "cgi", "digital sculpture"],
            "concept_art": ["concept art", "illustration", "design", "artwork"]
        }.items():
            if any(keyword in prompt_lower for keyword in keywords):
                intent["style"] = style
                break
        
        # Extract main subject (simplified - could use NLP)
        # This is a basic implementation
        subjects = re.findall(r'\b(?:a|an|the)\s+([a-zA-Z\s]+?)(?:\s+(?:with|in|at|on)|[,.])', prompt, re.I)
        if subjects:
            intent["subject"] = subjects[0].strip()
        
        # Detect mood/atmosphere
        moods = {
            "dramatic": ["dramatic", "intense", "powerful", "epic"],
            "peaceful": ["peaceful", "calm", "serene", "tranquil"],
            "mysterious": ["mysterious", "enigmatic", "mystical", "magical"],
            "cheerful": ["happy", "cheerful", "bright", "joyful", "vibrant"],
            "dark": ["dark", "gloomy", "ominous", "gothic", "noir"]
        }
        
        for mood, keywords in moods.items():
            if any(keyword in prompt_lower for keyword in keywords):
                intent["mood"] = mood
                break
        
        return intent

    def enhance_prompt(
        self,
        prompt: str,
        style_preset: Optional[str] = None,
        auto_detect_style: bool = True,
        add_quality_modifiers: bool = True,
        use_gpt_enhancement: bool = True,
        optimization_model: Optional[str] = None
    ) -> Tuple[str, Optional[str], Dict[str, any]]:
        """
        Enhance the user's prompt for better image generation
        
        Returns:
            Tuple of (enhanced_prompt, suggested_negative_prompt, metadata)
        """
        metadata = {"original_prompt": prompt}
        
        # Analyze intent
        intent = self.analyze_intent(prompt)
        metadata["intent"] = intent
        
        # Auto-detect style if not specified
        if not style_preset and auto_detect_style and intent["style"]:
            style_preset = intent["style"]
            metadata["auto_detected_style"] = style_preset
        
        # Start building enhanced prompt
        enhanced_parts = []
        
        # Add style preset prefix if available
        if style_preset:
            if style_preset in self.style_presets:
                preset = self.style_presets[style_preset]
                enhanced_parts.append(preset["prefix"])
                metadata["applied_style"] = style_preset
            elif style_preset != "none" and style_preset != "custom":
                # Custom style - add it directly to the prompt
                enhanced_parts.append(f"{style_preset} style,")
                metadata["applied_style"] = f"custom: {style_preset}"
        
        # Use GPT for intelligent enhancement
        if use_gpt_enhancement:
            try:
                model = optimization_model or self.optimization_model
                enhanced_base = self._gpt_enhance(prompt, style_preset, intent, model)
                enhanced_parts.append(enhanced_base)
                metadata["gpt_enhanced"] = True
                metadata["optimization_model"] = model
            except Exception as e:
                # Fallback to original prompt if GPT fails
                enhanced_parts.append(prompt)
                metadata["gpt_enhancement_error"] = str(e)
        else:
            enhanced_parts.append(prompt)
        
        # Add style suffix and modifiers
        if style_preset:
            if style_preset in self.style_presets:
                preset = self.style_presets[style_preset]
                
                # Add some modifiers
                if add_quality_modifiers:
                    selected_modifiers = preset["modifiers"][:2]  # Use top 2 modifiers
                    enhanced_parts.extend(selected_modifiers)
                
                # Add suffix
                enhanced_parts.append(preset["suffix"])
            elif style_preset != "none" and style_preset != "custom":
                # For custom styles, add generic quality enhancers
                if add_quality_modifiers:
                    enhanced_parts.extend(["high quality", "detailed", "professional"])
        
        # Add general quality enhancers if requested
        if add_quality_modifiers and not style_preset:
            enhanced_parts.extend(self.quality_enhancers[:3])
        
        # Construct final prompt
        enhanced_prompt = ", ".join(filter(None, enhanced_parts))
        
        # Clean up redundant commas and spaces
        enhanced_prompt = re.sub(r',\s*,', ',', enhanced_prompt)
        enhanced_prompt = re.sub(r'\s+', ' ', enhanced_prompt).strip()
        
        # Generate negative prompt suggestion
        negative_prompt = None
        if style_preset in self.negative_suggestions:
            negative_prompt = ", ".join(self.negative_suggestions[style_preset])
        
        metadata["final_length"] = len(enhanced_prompt)
        metadata["enhancement_ratio"] = len(enhanced_prompt) / len(prompt) if prompt else 0
        
        return enhanced_prompt, negative_prompt, metadata

    def _gpt_enhance(self, prompt: str, style: Optional[str], intent: Dict, model: str = None) -> str:
        """Use GPT to intelligently enhance the prompt"""
        
        system_prompt = """You are an expert at writing prompts for image generation AI. 
        Your task is to enhance user prompts to get better, more detailed, and more artistic results.
        
        Guidelines:
        1. Preserve the user's core intent and subject
        2. Add relevant artistic and technical details
        3. Include lighting, composition, and atmosphere descriptions
        4. Be specific about visual elements
        5. Keep the enhanced prompt under 200 words
        6. Return ONLY the enhanced description, no explanations"""
        
        user_message = f"Original prompt: {prompt}"
        
        if style:
            user_message += f"\nDesired style: {style}"
        
        if intent.get("mood"):
            user_message += f"\nDetected mood: {intent['mood']}"
        
        user_message += "\n\nEnhance this prompt for image generation:"
        
        try:
            # Use specified model for prompt optimization
            optimization_model = model or self.optimization_model
            
            # Try different model names if one fails
            models_to_try = [optimization_model]
            
            # Add fallback models for responses API
            if optimization_model not in ["gpt-5", "gpt-4.1", "gpt-4"]:
                # If using an unknown model, fallback to known working models
                models_to_try.extend(["gpt-5", "gpt-4.1", "gpt-4"])
            
            last_error = None
            for try_model in models_to_try:
                try:
                    # Remove reasoning parameter as it's not supported
                    response = self.client.responses.create(
                        model=try_model,
                        instructions=system_prompt,
                        input=user_message
                    )
                    # If successful, update the model for future use
                    if try_model != optimization_model:
                        print(f"Note: Using {try_model} instead of {optimization_model} for optimization")
                    break
                except Exception as e:
                    last_error = e
                    if "model_not_found" in str(e) or "does not exist" in str(e):
                        continue  # Try next model
                    else:
                        raise  # Re-raise if it's a different error
            else:
                # If all models failed, raise the last error
                if last_error:
                    raise last_error
            
            # Extract the enhanced prompt from response
            if hasattr(response, 'output_text'):
                return response.output_text.strip()
            else:
                # Fallback if response structure is different
                return prompt
                
        except Exception as e:
            print(f"GPT enhancement failed: {e}")
            return prompt

    def batch_enhance(self, prompts: List[str], **kwargs) -> List[Tuple[str, Optional[str], Dict]]:
        """Enhance multiple prompts in batch"""
        results = []
        for prompt in prompts:
            results.append(self.enhance_prompt(prompt, **kwargs))
        return results

    def suggest_variations(self, prompt: str, num_variations: int = 3) -> List[str]:
        """Generate variations of a prompt for diverse results"""
        base_enhanced, _, _ = self.enhance_prompt(prompt, use_gpt_enhancement=False)
        
        variations = [base_enhanced]
        
        # Add style variations
        styles = ["photorealistic", "cinematic", "anime", "oil_painting"]
        for i, style in enumerate(styles[:num_variations-1]):
            varied, _, _ = self.enhance_prompt(prompt, style_preset=style, use_gpt_enhancement=False)
            variations.append(varied)
        
        return variations[:num_variations]