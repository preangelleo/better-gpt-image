"""
Image Processor for Better GPT Image
Handles image preprocessing, mask creation, and optimization
"""

import base64
import io
from pathlib import Path
from typing import Optional, Tuple, Union, List
from PIL import Image, ImageOps, ImageFilter
import numpy as np


class ImageProcessor:
    """Handles image preprocessing and optimization"""
    
    def __init__(self):
        # Supported formats
        self.supported_formats = {'.jpg', '.jpeg', '.png', '.gif', '.webp', '.bmp'}
        
        # Size constraints for GPT-Image-1
        self.max_file_size = 50 * 1024 * 1024  # 50MB
        self.valid_dimensions = [(1024, 1024), (1536, 1024), (1024, 1536)]
        
    def prepare_input_image(
        self,
        image_path: Union[str, Path, bytes, Image.Image],
        target_size: Optional[Tuple[int, int]] = None,
        maintain_aspect_ratio: bool = True,
        format: str = "PNG"
    ) -> bytes:
        """
        Prepare an image for API input
        
        Args:
            image_path: Input image (path, bytes, or PIL Image)
            target_size: Target dimensions (width, height)
            maintain_aspect_ratio: Whether to maintain aspect ratio
            format: Output format (PNG, JPEG, WEBP)
            
        Returns:
            Processed image as bytes
        """
        # Load image
        if isinstance(image_path, Image.Image):
            img = image_path
        elif isinstance(image_path, bytes):
            img = Image.open(io.BytesIO(image_path))
        else:
            img = Image.open(image_path)
        
        # Convert RGBA to RGB if saving as JPEG
        if format.upper() == "JPEG" and img.mode in ("RGBA", "LA", "P"):
            # Create white background
            background = Image.new("RGB", img.size, (255, 255, 255))
            if img.mode == "P":
                img = img.convert("RGBA")
            background.paste(img, mask=img.split()[-1] if img.mode == "RGBA" else None)
            img = background
        
        # Resize if needed
        if target_size:
            img = self._resize_image(img, target_size, maintain_aspect_ratio)
        else:
            # Auto-resize to nearest valid dimension if too large
            img = self._auto_resize_to_valid(img)
        
        # Convert to bytes
        buffer = io.BytesIO()
        img.save(buffer, format=format, optimize=True, quality=95)
        
        # Check file size
        if buffer.tell() > self.max_file_size:
            # Reduce quality if too large
            buffer = io.BytesIO()
            img.save(buffer, format=format, optimize=True, quality=85)
        
        buffer.seek(0)
        return buffer.read()
    
    def _resize_image(
        self,
        img: Image.Image,
        target_size: Tuple[int, int],
        maintain_aspect_ratio: bool
    ) -> Image.Image:
        """Resize image to target size"""
        if maintain_aspect_ratio:
            img.thumbnail(target_size, Image.Resampling.LANCZOS)
            
            # Create new image with target size and paste resized image
            new_img = Image.new(img.mode, target_size, (255, 255, 255) if img.mode == "RGB" else (255, 255, 255, 0))
            
            # Center the image
            x = (target_size[0] - img.width) // 2
            y = (target_size[1] - img.height) // 2
            new_img.paste(img, (x, y))
            
            return new_img
        else:
            return img.resize(target_size, Image.Resampling.LANCZOS)
    
    def _auto_resize_to_valid(self, img: Image.Image) -> Image.Image:
        """Auto-resize to nearest valid dimension"""
        current_size = (img.width, img.height)
        
        # Find nearest valid dimension
        best_size = min(
            self.valid_dimensions,
            key=lambda s: abs(s[0] - current_size[0]) + abs(s[1] - current_size[1])
        )
        
        # Only resize if current size is not valid
        if current_size not in self.valid_dimensions:
            return self._resize_image(img, best_size, maintain_aspect_ratio=True)
        
        return img
    
    def create_mask(
        self,
        image: Union[str, Path, bytes, Image.Image],
        mask_type: str = "center",
        mask_data: Optional[dict] = None
    ) -> bytes:
        """
        Create a mask for image editing
        
        Args:
            image: Reference image for mask dimensions
            mask_type: Type of mask (center, edges, custom)
            mask_data: Additional data for mask creation
            
        Returns:
            Mask image as bytes (PNG with alpha channel)
        """
        # Load reference image to get dimensions
        if isinstance(image, Image.Image):
            ref_img = image
        elif isinstance(image, bytes):
            ref_img = Image.open(io.BytesIO(image))
        else:
            ref_img = Image.open(image)
        
        width, height = ref_img.size
        
        # Create mask based on type
        if mask_type == "center":
            mask = self._create_center_mask(width, height, mask_data)
        elif mask_type == "edges":
            mask = self._create_edge_mask(width, height, mask_data)
        elif mask_type == "custom" and mask_data and "coordinates" in mask_data:
            mask = self._create_custom_mask(width, height, mask_data["coordinates"])
        else:
            # Default to center mask
            mask = self._create_center_mask(width, height)
        
        # Ensure mask has alpha channel
        if mask.mode != "RGBA":
            mask = mask.convert("RGBA")
        
        # Convert to bytes
        buffer = io.BytesIO()
        mask.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer.read()
    
    def _create_center_mask(
        self,
        width: int,
        height: int,
        params: Optional[dict] = None
    ) -> Image.Image:
        """Create a centered circular/elliptical mask"""
        # Default parameters
        size_ratio = 0.5
        if params:
            size_ratio = params.get("size_ratio", 0.5)
        
        # Create mask
        mask = Image.new("L", (width, height), 0)
        
        # Calculate ellipse bounds
        center_x, center_y = width // 2, height // 2
        radius_x = int(width * size_ratio / 2)
        radius_y = int(height * size_ratio / 2)
        
        # Draw ellipse
        from PIL import ImageDraw
        draw = ImageDraw.Draw(mask)
        draw.ellipse(
            [center_x - radius_x, center_y - radius_y,
             center_x + radius_x, center_y + radius_y],
            fill=255
        )
        
        # Apply gaussian blur for smooth edges
        mask = mask.filter(ImageFilter.GaussianBlur(radius=10))
        
        # Convert to RGBA
        mask_rgba = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        mask_rgba.putalpha(mask)
        
        return mask_rgba
    
    def _create_edge_mask(
        self,
        width: int,
        height: int,
        params: Optional[dict] = None
    ) -> Image.Image:
        """Create a mask for edges/borders"""
        border_width = 100
        if params:
            border_width = params.get("border_width", 100)
        
        # Create mask with border
        mask = Image.new("L", (width, height), 255)
        
        from PIL import ImageDraw
        draw = ImageDraw.Draw(mask)
        draw.rectangle(
            [border_width, border_width, width - border_width, height - border_width],
            fill=0
        )
        
        # Apply blur for smooth transition
        mask = mask.filter(ImageFilter.GaussianBlur(radius=20))
        
        # Convert to RGBA
        mask_rgba = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        mask_rgba.putalpha(mask)
        
        return mask_rgba
    
    def _create_custom_mask(
        self,
        width: int,
        height: int,
        coordinates: List[Tuple[int, int]]
    ) -> Image.Image:
        """Create a custom polygon mask from coordinates"""
        mask = Image.new("L", (width, height), 0)
        
        from PIL import ImageDraw
        draw = ImageDraw.Draw(mask)
        
        if len(coordinates) >= 3:
            draw.polygon(coordinates, fill=255)
        
        # Apply slight blur
        mask = mask.filter(ImageFilter.GaussianBlur(radius=5))
        
        # Convert to RGBA
        mask_rgba = Image.new("RGBA", (width, height), (0, 0, 0, 0))
        mask_rgba.putalpha(mask)
        
        return mask_rgba
    
    def add_alpha_channel(
        self,
        image: Union[str, Path, bytes, Image.Image]
    ) -> bytes:
        """
        Add alpha channel to an image if it doesn't have one
        
        Args:
            image: Input image
            
        Returns:
            Image with alpha channel as bytes
        """
        # Load image
        if isinstance(image, Image.Image):
            img = image
        elif isinstance(image, bytes):
            img = Image.open(io.BytesIO(image))
        else:
            img = Image.open(image)
        
        # Convert to RGBA if needed
        if img.mode != "RGBA":
            if img.mode == "RGB":
                img = img.convert("RGBA")
            elif img.mode == "L":
                # For grayscale, use the image itself as alpha
                img_rgba = img.convert("RGBA")
                img_rgba.putalpha(img)
                img = img_rgba
            elif img.mode == "P":
                # For palette images
                img = img.convert("RGBA")
        
        # Convert to bytes
        buffer = io.BytesIO()
        img.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer.read()
    
    def optimize_for_transparency(
        self,
        image: Union[str, Path, bytes, Image.Image],
        threshold: int = 240
    ) -> bytes:
        """
        Optimize image for transparent background generation
        
        Args:
            image: Input image
            threshold: Threshold for white background removal (0-255)
            
        Returns:
            Optimized image as bytes
        """
        # Load image
        if isinstance(image, Image.Image):
            img = image
        elif isinstance(image, bytes):
            img = Image.open(io.BytesIO(image))
        else:
            img = Image.open(image)
        
        # Convert to RGBA
        if img.mode != "RGBA":
            img = img.convert("RGBA")
        
        # Get data as numpy array
        data = np.array(img)
        
        # Find white or near-white pixels
        r, g, b, a = data[:, :, 0], data[:, :, 1], data[:, :, 2], data[:, :, 3]
        white_pixels = (r > threshold) & (g > threshold) & (b > threshold)
        
        # Make white pixels transparent
        data[white_pixels] = [255, 255, 255, 0]
        
        # Create new image
        new_img = Image.fromarray(data, mode="RGBA")
        
        # Convert to bytes
        buffer = io.BytesIO()
        new_img.save(buffer, format="PNG")
        buffer.seek(0)
        return buffer.read()
    
    def batch_process(
        self,
        images: List[Union[str, Path, bytes]],
        target_size: Optional[Tuple[int, int]] = None,
        format: str = "PNG"
    ) -> List[bytes]:
        """Process multiple images in batch"""
        processed = []
        for image in images:
            processed.append(
                self.prepare_input_image(image, target_size, format=format)
            )
        return processed