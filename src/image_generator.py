"""
Image Generator for Better GPT Image
Core image generation functionality using OpenAI's latest APIs
"""

import base64
import io
import json
from pathlib import Path
from typing import Dict, List, Optional, Union, Any, AsyncGenerator
from PIL import Image
import aiohttp
import asyncio
from openai import OpenAI, AsyncOpenAI


class ImageGenerator:
    """Handles all image generation operations using OpenAI APIs"""
    
    def __init__(self, api_key: str):
        self.client = OpenAI(api_key=api_key)
        self.async_client = AsyncOpenAI(api_key=api_key)
        
        # Size options for images
        self.valid_sizes = ["1024x1024", "1536x1024", "1024x1536"]
        
        # Quality options
        self.valid_qualities = ["low", "medium", "high", "auto"]

    def generate_image(
        self,
        prompt: str,
        size: Optional[str] = None,
        quality: Optional[str] = None,
        n: int = 1,
        background: Optional[str] = None,
        use_gpt_image: bool = False,
        model: str = "gpt-5"
    ) -> Dict[str, Any]:
        """
        Generate images from text prompt using either responses API or images API
        
        Args:
            prompt: Text description of the image
            size: Image dimensions (1024x1024, 1536x1024, 1024x1536)
            quality: Image quality (low, medium, high, auto)
            n: Number of images to generate
            background: Background setting (transparent, opaque, auto)
            use_gpt_image: Use gpt-image-1 model directly instead of responses API
            model: Model to use for responses API (gpt-5, gpt-4.1, etc.)
            
        Returns:
            Dict containing generated images and metadata
        """
        try:
            if use_gpt_image:
                # Use direct images.generate API with gpt-image-1
                return self._generate_with_images_api(prompt, size, quality, n, background)
            else:
                # Use responses API with GPT-5 or other models
                return self._generate_with_responses_api(prompt, size, quality, background, model)
                
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "metadata": {"prompt": prompt}
            }
    
    def _generate_with_responses_api(
        self,
        prompt: str,
        size: Optional[str] = None,
        quality: Optional[str] = None,
        background: Optional[str] = None,
        model: str = "gpt-5"
    ) -> Dict[str, Any]:
        """Generate image using the responses API"""
        # Build tools configuration
        tools_config = [{"type": "image_generation"}]
        
        # Add optional parameters to the tool config
        if quality:
            tools_config[0]["quality"] = quality
        if size:
            tools_config[0]["size"] = size
        if background:
            tools_config[0]["background"] = background
        
        # Make API call
        print(f"[DEBUG] Calling responses API with model: {model}")
        print(f"[DEBUG] Tools config: {tools_config}")
        
        response = self.client.responses.create(
            model=model,
            input=prompt,
            tools=tools_config
        )
        
        # Debug response structure
        print(f"[DEBUG] Response type: {type(response)}")
        print(f"[DEBUG] Response attributes: {dir(response)}")
        
        if hasattr(response, 'output'):
            print(f"[DEBUG] response.output exists, type: {type(response.output)}")
            if response.output:
                print(f"[DEBUG] response.output length: {len(response.output)}")
                for i, out in enumerate(response.output):
                    print(f"[DEBUG] Output {i}: {out}")
                    if hasattr(out, 'type'):
                        print(f"[DEBUG]   - type: {out.type}")
                    if hasattr(out, 'result'):
                        print(f"[DEBUG]   - has result: {len(out.result) if out.result else 0} chars")
        
        # Process response
        result = {
            "success": True,
            "images": [],
            "metadata": {
                "model": model,
                "api": "responses",
                "prompt": prompt,
                "size": size or "1024x1024",
                "quality": quality or "high"
            }
        }
        
        # Extract images from response - matching reference code structure
        if hasattr(response, 'output') and response.output:
            image_data = [
                output.result
                for output in response.output
                if hasattr(output, 'type') and output.type == "image_generation_call"
            ]
            
            for i, b64_data in enumerate(image_data):
                if b64_data:
                    result["images"].append({
                        "b64_json": b64_data,
                        "revised_prompt": None,  # May not be available in responses API
                        "image_id": f"img_{i}"
                    })
                    print(f"[DEBUG] Added image {i} to results")
        
        return result
    
    def _generate_with_images_api(
        self,
        prompt: str,
        size: Optional[str] = None,
        quality: Optional[str] = None,
        n: int = 1,
        background: Optional[str] = None
    ) -> Dict[str, Any]:
        """Generate image using the direct images API with gpt-image-1"""
        # Build parameters
        params = {
            "model": "gpt-image-1",
            "prompt": prompt
        }
        
        # Add optional parameters
        if size:
            params["size"] = size
        if quality:
            params["quality"] = quality
        if n:
            params["n"] = n
        
        # Add background parameter if specified
        if background:
            params["background"] = background
        
        # Make API call
        response = self.client.images.generate(**params)
        
        # Process response
        result = {
            "success": True,
            "images": [],
            "metadata": {
                "model": "gpt-image-1",
                "api": "images",
                "prompt": prompt,
                "size": size or "1024x1024",
                "quality": quality or "standard",
                "count": n
            }
        }
        
        # Process images from response
        for image_data in response.data:
            # Check if response has b64_json or url
            if hasattr(image_data, 'b64_json'):
                result["images"].append({
                    "b64_json": image_data.b64_json,
                    "revised_prompt": getattr(image_data, 'revised_prompt', None)
                })
            elif hasattr(image_data, 'url'):
                # If URL is returned, we can fetch and convert to base64
                import requests
                try:
                    img_response = requests.get(image_data.url)
                    if img_response.status_code == 200:
                        b64_data = base64.b64encode(img_response.content).decode('utf-8')
                        result["images"].append({
                            "b64_json": b64_data,
                            "revised_prompt": getattr(image_data, 'revised_prompt', None),
                            "url": image_data.url
                        })
                except Exception as e:
                    result["images"].append({
                        "url": image_data.url,
                        "error": f"Could not convert to base64: {str(e)}"
                    })
        
        return result

    def edit_image_with_reference(
        self,
        prompt: str,
        reference_images: List[Dict[str, Any]],
        mask: Optional[Dict[str, Any]] = None,
        quality: Optional[str] = None,
        input_fidelity: str = "low",
        model: str = "gpt-4.1"
    ) -> Dict[str, Any]:
        """
        Edit images using reference images (using responses API)
        
        Args:
            prompt: Description of the desired edit
            reference_images: List of reference images as dicts with type and data
            mask: Optional mask configuration
            quality: Output quality
            input_fidelity: How closely to preserve input details (low/high)
            model: Model to use (gpt-4.1, gpt-4o, etc.)
            
        Returns:
            Dict containing edited images and metadata
        """
        try:
            # Build input content
            content = [{"type": "input_text", "text": prompt}]
            
            # Add reference images to content
            for ref_img in reference_images:
                if "base64" in ref_img:
                    content.append({
                        "type": "input_image",
                        "image_url": f"data:image/jpeg;base64,{ref_img['base64']}"
                    })
                elif "file_id" in ref_img:
                    content.append({
                        "type": "input_image",
                        "file_id": ref_img["file_id"]
                    })
                elif "url" in ref_img:
                    content.append({
                        "type": "input_image",
                        "image_url": ref_img["url"]
                    })
            
            # Build tools configuration
            tools_config = [{"type": "image_generation"}]
            
            if quality:
                tools_config[0]["quality"] = quality
            if input_fidelity:
                tools_config[0]["input_fidelity"] = input_fidelity
            if mask:
                tools_config[0]["input_image_mask"] = mask
            
            # Make API call
            response = self.client.responses.create(
                model=model,
                input=[{
                    "role": "user",
                    "content": content
                }],
                tools=tools_config
            )
            
            # Process response
            result = {
                "success": True,
                "images": [],
                "metadata": {
                    "model": model,
                    "prompt": prompt,
                    "num_references": len(reference_images),
                    "has_mask": mask is not None,
                    "input_fidelity": input_fidelity
                }
            }
            
            # Extract images
            for output in response.output:
                if output.type == "image_generation_call":
                    result["images"].append({
                        "b64_json": output.result,
                        "revised_prompt": getattr(output, 'revised_prompt', None),
                        "image_id": getattr(output, 'id', None)
                    })
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "metadata": {"prompt": prompt}
            }

    async def stream_generation(
        self,
        prompt: str,
        partial_images: int = 2,
        model: str = "gpt-image-1",
        **kwargs
    ) -> AsyncGenerator[Dict[str, Any], None]:
        """
        Stream image generation with partial images
        
        Args:
            prompt: Text description
            partial_images: Number of partial images (0-3)
            model: Model to use
            **kwargs: Additional parameters
            
        Yields:
            Dict containing partial or final images
        """
        try:
            # Use the images.generate API with streaming
            stream = await self.async_client.images.generate(
                model=model,
                prompt=prompt,
                stream=True,
                partial_images=partial_images,
                **kwargs
            )
            
            async for event in stream:
                if event.type == "image_generation.partial_image":
                    yield {
                        "type": "partial",
                        "index": event.partial_image_index,
                        "b64_json": event.b64_json
                    }
                elif hasattr(event, 'data'):
                    # Final image
                    for image_data in event.data:
                        if hasattr(image_data, 'b64_json'):
                            yield {
                                "type": "complete",
                                "b64_json": image_data.b64_json,
                                "revised_prompt": getattr(image_data, 'revised_prompt', None)
                            }
                            
        except Exception as e:
            yield {
                "type": "error",
                "error": str(e)
            }

    def multi_turn_generation(
        self,
        new_prompt: str,
        previous_response_id: str,
        quality: Optional[str] = None,
        model: str = "gpt-5"
    ) -> Dict[str, Any]:
        """
        Continue image generation from a previous response
        
        Args:
            new_prompt: New instruction for modification
            previous_response_id: ID of the previous response
            quality: Image quality
            model: Model to use
            
        Returns:
            Dict containing generated images
        """
        try:
            # Build tools configuration
            tools_config = [{"type": "image_generation"}]
            if quality:
                tools_config[0]["quality"] = quality
            
            # Make API call with previous response reference
            response = self.client.responses.create(
                model=model,
                previous_response_id=previous_response_id,
                input=new_prompt,
                tools=tools_config
            )
            
            # Process response
            result = {
                "success": True,
                "images": [],
                "response_id": response.id,
                "metadata": {
                    "model": model,
                    "prompt": new_prompt,
                    "continued_from": previous_response_id
                }
            }
            
            # Extract images
            for output in response.output:
                if output.type == "image_generation_call":
                    result["images"].append({
                        "b64_json": output.result,
                        "revised_prompt": getattr(output, 'revised_prompt', None),
                        "image_id": getattr(output, 'id', None)
                    })
            
            return result
            
        except Exception as e:
            return {
                "success": False,
                "error": str(e),
                "metadata": {"prompt": new_prompt}
            }

    def save_image(self, b64_json: str, filepath: Union[str, Path]) -> bool:
        """Save a base64 encoded image to file"""
        try:
            image_data = base64.b64decode(b64_json)
            with open(filepath, "wb") as f:
                f.write(image_data)
            return True
        except Exception as e:
            print(f"Error saving image: {e}")
            return False

    def image_to_base64(self, image_path: Union[str, Path]) -> str:
        """Convert an image file to base64 string"""
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode('utf-8')

    def calculate_cost(
        self,
        size: str = "1024x1024",
        quality: str = "medium",
        n: int = 1,
        input_text_tokens: int = 50,
        input_image_tokens: int = 0,
        model: str = "gpt-image-1"
    ) -> Dict[str, Any]:
        """
        Calculate the actual cost of image generation based on pricing
        
        Returns:
            Dict with token counts, costs, and price in cents
        """
        # Token counts for output based on documentation
        token_counts = {
            ("1024x1024", "low"): 272,
            ("1024x1024", "medium"): 1056,
            ("1024x1024", "high"): 4160,
            ("1024x1536", "low"): 408,
            ("1024x1536", "medium"): 1584,
            ("1024x1536", "high"): 6240,
            ("1536x1024", "low"): 400,
            ("1536x1024", "medium"): 1568,
            ("1536x1024", "high"): 6208,
        }
        
        # Direct per-image pricing for gpt-image-1 (in dollars)
        image_pricing = {
            ("1024x1024", "low"): 0.011,
            ("1024x1024", "medium"): 0.042,
            ("1024x1024", "high"): 0.167,
            ("1024x1536", "low"): 0.016,
            ("1024x1536", "medium"): 0.063,
            ("1024x1536", "high"): 0.250,
            ("1536x1024", "low"): 0.016,
            ("1536x1024", "medium"): 0.063,
            ("1536x1024", "high"): 0.250,
        }
        
        # Token-based pricing (per million tokens)
        text_input_price = 5.00  # $5 per 1M tokens
        image_input_price = 10.00  # $10 per 1M tokens
        image_output_price = 40.00  # $40 per 1M tokens
        
        output_tokens = token_counts.get((size, quality), 1056)
        total_output_tokens = output_tokens * n
        
        # Calculate costs
        if model == "gpt-image-1":
            # Use direct per-image pricing
            per_image_cost = image_pricing.get((size, quality), 0.042)
            total_image_cost = per_image_cost * n
            
            # Add input costs (if using responses API with input)
            input_text_cost = (input_text_tokens / 1_000_000) * text_input_price
            input_image_cost = (input_image_tokens / 1_000_000) * image_input_price
            
            total_cost = total_image_cost + input_text_cost + input_image_cost
        else:
            # Token-based calculation for other models
            input_text_cost = (input_text_tokens / 1_000_000) * text_input_price
            input_image_cost = (input_image_tokens / 1_000_000) * image_input_price
            output_cost = (total_output_tokens / 1_000_000) * image_output_price
            
            total_cost = input_text_cost + input_image_cost + output_cost
        
        # Convert to cents for filename
        total_cents = int(total_cost * 100)
        
        return {
            "input_text_tokens": input_text_tokens,
            "input_image_tokens": input_image_tokens,
            "output_tokens": total_output_tokens,
            "total_tokens": input_text_tokens + input_image_tokens + total_output_tokens,
            "input_text_cost": f"${input_text_cost:.6f}",
            "input_image_cost": f"${input_image_cost:.6f}" if input_image_tokens > 0 else "$0",
            "output_cost": f"${total_image_cost if model == 'gpt-image-1' else (total_output_tokens / 1_000_000) * image_output_price:.6f}",
            "total_cost": f"${total_cost:.6f}",
            "total_cost_dollars": total_cost,
            "total_cents": total_cents,
            "cost_breakdown": {
                "model": model,
                "size": size,
                "quality": quality,
                "images": n,
                "price_per_image": f"${image_pricing.get((size, quality), 0):.3f}" if model == "gpt-image-1" else "token-based"
            }
        }