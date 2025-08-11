#!/usr/bin/env python3
"""
Image Compression and Cropping Utility
Converts PNG to JPG and crops to 16:9 aspect ratio
"""

import os
import sys
from PIL import Image
from pathlib import Path

def compress_and_crop_image(
    input_path: str,
    output_path: str = None,
    aspect_ratio: tuple = (16, 9),
    quality: int = 85,
    max_width: int = 1600
):
    """
    Compress PNG to JPG and crop to desired aspect ratio
    
    Args:
        input_path: Path to input image (PNG or other)
        output_path: Path for output JPG (optional)
        aspect_ratio: Target aspect ratio as tuple (width, height)
        quality: JPG compression quality (1-100)
        max_width: Maximum width for output image
    
    Returns:
        Path to output file
    """
    # Open the image
    img = Image.open(input_path)
    
    # Convert RGBA to RGB if necessary
    if img.mode in ('RGBA', 'LA', 'P'):
        # Create a white background
        background = Image.new('RGB', img.size, (255, 255, 255))
        if img.mode == 'P':
            img = img.convert('RGBA')
        background.paste(img, mask=img.split()[-1] if img.mode == 'RGBA' else None)
        img = background
    elif img.mode != 'RGB':
        img = img.convert('RGB')
    
    # Calculate target dimensions
    original_width, original_height = img.size
    target_ratio = aspect_ratio[0] / aspect_ratio[1]
    current_ratio = original_width / original_height
    
    if current_ratio > target_ratio:
        # Image is too wide, crop horizontally
        new_width = int(original_height * target_ratio)
        new_height = original_height
        left = (original_width - new_width) // 2
        right = left + new_width
        top = 0
        bottom = original_height
    else:
        # Image is too tall, crop vertically
        new_width = original_width
        new_height = int(original_width / target_ratio)
        left = 0
        right = original_width
        top = (original_height - new_height) // 2
        bottom = top + new_height
    
    # Crop the image
    img_cropped = img.crop((left, top, right, bottom))
    
    # Resize if needed
    if img_cropped.width > max_width:
        ratio = max_width / img_cropped.width
        new_height = int(img_cropped.height * ratio)
        img_cropped = img_cropped.resize((max_width, new_height), Image.Resampling.LANCZOS)
    
    # Generate output path if not provided
    if output_path is None:
        input_file = Path(input_path)
        output_path = input_file.parent / f"{input_file.stem}_16x9.jpg"
    
    # Save as JPG
    img_cropped.save(output_path, 'JPEG', quality=quality, optimize=True)
    
    # Print info
    print(f"✅ Image processed successfully!")
    print(f"   Original: {original_width}x{original_height} (ratio: {current_ratio:.2f})")
    print(f"   Cropped:  {img_cropped.width}x{img_cropped.height} (ratio: {img_cropped.width/img_cropped.height:.2f})")
    print(f"   Output:   {output_path}")
    print(f"   Size:     {os.path.getsize(output_path) / 1024:.1f} KB")
    
    return output_path

def process_batch(input_dir: str, output_dir: str = None):
    """Process all PNG files in a directory"""
    input_path = Path(input_dir)
    if output_dir:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = input_path
    
    png_files = list(input_path.glob("*.png"))
    print(f"Found {len(png_files)} PNG files to process")
    
    for png_file in png_files:
        output_file = output_path / f"{png_file.stem}_16x9.jpg"
        try:
            compress_and_crop_image(str(png_file), str(output_file))
        except Exception as e:
            print(f"❌ Error processing {png_file}: {e}")

def main():
    """Command line interface"""
    if len(sys.argv) < 2:
        print("Usage:")
        print("  python image_compress_crop.py <input_image> [output_image]")
        print("  python image_compress_crop.py --batch <input_dir> [output_dir]")
        print("\nOptions:")
        print("  input_image:  Path to PNG image to process")
        print("  output_image: Path for output JPG (optional)")
        print("  --batch:      Process all PNGs in a directory")
        print("\nExample:")
        print("  python image_compress_crop.py output.png compressed.jpg")
        print("  python image_compress_crop.py --batch ./output ./assets")
        sys.exit(1)
    
    if sys.argv[1] == "--batch":
        if len(sys.argv) < 3:
            print("Error: Please provide input directory for batch processing")
            sys.exit(1)
        input_dir = sys.argv[2]
        output_dir = sys.argv[3] if len(sys.argv) > 3 else None
        process_batch(input_dir, output_dir)
    else:
        input_file = sys.argv[1]
        output_file = sys.argv[2] if len(sys.argv) > 2 else None
        
        if not os.path.exists(input_file):
            print(f"Error: Input file '{input_file}' not found")
            sys.exit(1)
        
        compress_and_crop_image(input_file, output_file)

if __name__ == "__main__":
    main()