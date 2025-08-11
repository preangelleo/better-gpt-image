"""
Prompt Optimizer for Better GPT Image
Enhances user prompts for better image generation results
"""

import re
from typing import Dict, List, Optional, Tuple, Any
from openai import OpenAI
import json
from .style_presets import STYLE_PRESETS, get_style_list
import sys
import os
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
try:
    from image_optimizer_prompt import SYSTEM_PROMPT_STRUCTURED_IMAGE_DESCRIPTION
except ImportError:
    # Fallback if custom prompt not available
    SYSTEM_PROMPT_STRUCTURED_IMAGE_DESCRIPTION = None


class PromptOptimizer:
    """Optimizes prompts for image generation using GPT models"""
    
    # Default optimization model (can be overridden)
    # Using GPT-5 as default - latest and most advanced
    DEFAULT_OPTIMIZATION_MODEL = "gpt-5"  # Latest model for best results
    
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
        
        # Use GPT for intelligent enhancement if requested
        if use_gpt_enhancement:
            try:
                model = optimization_model or self.optimization_model
                # Simple intent for GPT - not needed for complex analysis
                intent = {}
                enhanced_prompt = self._gpt_enhance(prompt, style_preset, intent, model)
                metadata["gpt_enhanced"] = True
                metadata["optimization_model"] = model
                metadata["applied_style"] = style_preset if style_preset else "none"
            except Exception as e:
                # Fallback to rule-based if GPT fails
                print(f"GPT enhancement failed, using rule-based: {e}")
                metadata["gpt_enhancement_error"] = str(e)
                enhanced_prompt = self._rule_based_enhance(prompt, style_preset, add_quality_modifiers)
                metadata["gpt_enhanced"] = False
        else:
            # Rule-based enhancement
            enhanced_prompt = self._rule_based_enhance(prompt, style_preset, add_quality_modifiers)
            metadata["gpt_enhanced"] = False
        
        # Generate negative prompt suggestion based on style
        negative_prompt = None
        if style_preset in self.negative_suggestions:
            negative_prompt = ", ".join(self.negative_suggestions[style_preset])
        
        metadata["final_length"] = len(enhanced_prompt)
        metadata["enhancement_ratio"] = len(enhanced_prompt) / len(prompt) if prompt else 0
        
        return enhanced_prompt, negative_prompt, metadata
    
    def _rule_based_enhance(self, prompt: str, style_preset: Optional[str], add_quality_modifiers: bool) -> str:
        """Fallback rule-based enhancement when GPT is not available"""
        enhanced_parts = []
        
        # Add style prefix if available
        if style_preset and style_preset in self.style_presets:
            preset = self.style_presets[style_preset]
            enhanced_parts.append(preset["prefix"])
        
        # Add original prompt
        enhanced_parts.append(prompt)
        
        # Add style modifiers and suffix
        if style_preset and style_preset in self.style_presets:
            preset = self.style_presets[style_preset]
            if add_quality_modifiers:
                enhanced_parts.extend(preset["modifiers"][:2])
            enhanced_parts.append(preset["suffix"])
        elif add_quality_modifiers:
            # Add generic quality enhancers
            enhanced_parts.extend(self.quality_enhancers[:3])
        
        # Construct and clean final prompt
        enhanced_prompt = ", ".join(filter(None, enhanced_parts))
        enhanced_prompt = re.sub(r',\s*,', ',', enhanced_prompt)
        enhanced_prompt = re.sub(r'\s+', ' ', enhanced_prompt).strip()
        
        return enhanced_prompt

    def _gpt_enhance(self, prompt: str, style: Optional[str], intent: Dict, model: str = None) -> str:
        """Use GPT to enhance the prompt using the structured image description system"""
        
        # Always use the custom system prompt for structured image description
        system_prompt = SYSTEM_PROMPT_STRUCTURED_IMAGE_DESCRIPTION
        
        # Simple user message - just the prompt with optional style
        if style and style != "none":
            user_message = f"{prompt}\n\nArt Style: {style}"
        else:
            user_message = prompt
        
        try:
            # Use specified model for prompt optimization
            optimization_model = model or self.optimization_model
            
            # Map model names for API compatibility
            if optimization_model == "gpt-5":
                actual_model = "gpt-4-turbo-preview"  # Map GPT-5 to latest turbo
            elif optimization_model == "gpt-4.1":
                actual_model = "gpt-4-turbo-preview"  # GPT-4.1 also uses turbo
            else:
                actual_model = optimization_model
            
            # Direct call to GPT with the structured prompt system
            response = self.client.chat.completions.create(
                model=actual_model,
                messages=[
                    {"role": "system", "content": system_prompt},
                    {"role": "user", "content": user_message}
                ],
                max_tokens=800,  # Increased for detailed structured descriptions
                temperature=0.7
            )
            
            # Extract and return the enhanced prompt
            if response and response.choices:
                enhanced = response.choices[0].message.content.strip()
                return enhanced
            else:
                return prompt
                
        except Exception as e:
            print(f"GPT enhancement failed: {e}")
            # Try fallback model if primary fails
            if "model_not_found" in str(e) or "does not exist" in str(e):
                try:
                    # Fallback to GPT-4 if newer models not available
                    response = self.client.chat.completions.create(
                        model="gpt-4",  # Fallback to stable GPT-4
                        messages=[
                            {"role": "system", "content": system_prompt},
                            {"role": "user", "content": user_message}
                        ],
                        max_tokens=800,
                        temperature=0.7
                    )
                    if response and response.choices:
                        print("Note: Using GPT-4 fallback for optimization")
                        return response.choices[0].message.content.strip()
                except:
                    pass
            
            return prompt  # Return original if all fails

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