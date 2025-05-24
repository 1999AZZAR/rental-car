#!/usr/bin/env python3
"""
WebP Image Converter Utility

This script converts images (JPG, PNG, etc.) to WebP format for optimization.
"""

import os
import sys
from pathlib import Path
from PIL import Image
import argparse

def convert_to_webp(source_path, quality=80, replace=False):
    """
    Convert an image to WebP format
    
    Args:
        source_path (str): Path to the source image
        quality (int): WebP quality (0-100)
        replace (bool): Whether to replace the original file
        
    Returns:
        str: Path to the converted image
    """
    # Get the file path
    image_path = Path(source_path)
    
    # Skip if it's already a WebP file
    if image_path.suffix.lower() == '.webp':
        print(f"Skipping {image_path} (already WebP)")
        return None
    
    # Check if file exists and is an image
    if not image_path.exists():
        print(f"Error: {image_path} does not exist")
        return None
    
    try:
        # Open the image
        with Image.open(image_path) as img:
            # Create output path
            if replace:
                webp_path = image_path.with_suffix('.webp')
            else:
                webp_path = image_path.with_name(f"{image_path.stem}.webp")
            
            # Save as WebP
            img.save(str(webp_path), 'WEBP', quality=quality)
            print(f"Converted: {image_path} -> {webp_path}")
            
            # If replacing, remove the original
            if replace and webp_path.exists():
                image_path.unlink()
                print(f"Removed original: {image_path}")
            
            return str(webp_path)
    except Exception as e:
        print(f"Error converting {image_path}: {e}")
        return None

def process_directory(directory, quality=80, replace=False, recursive=True):
    """
    Process all images in a directory
    
    Args:
        directory (str): Directory to process
        quality (int): WebP quality (0-100)
        replace (bool): Whether to replace original files
        recursive (bool): Whether to process subdirectories
    """
    extensions = {'.jpg', '.jpeg', '.png', '.gif', '.bmp', '.tiff'}
    directory_path = Path(directory)
    
    if not directory_path.exists():
        print(f"Error: Directory {directory} does not exist")
        return
    
    # Get all files in directory
    if recursive:
        all_files = list(directory_path.glob('**/*.*'))
    else:
        all_files = list(directory_path.glob('*.*'))
    
    # Filter image files
    image_files = [f for f in all_files if f.suffix.lower() in extensions]
    
    if not image_files:
        print(f"No images found in {directory}")
        return
    
    print(f"Found {len(image_files)} images to convert")
    
    # Convert all images
    converted_count = 0
    for image_file in image_files:
        if convert_to_webp(image_file, quality, replace):
            converted_count += 1
    
    print(f"Conversion complete. Converted {converted_count} images.")

def main():
    parser = argparse.ArgumentParser(description="Convert images to WebP format")
    parser.add_argument('path', help="File or directory to convert")
    parser.add_argument('--quality', type=int, default=80, help="WebP quality (0-100)")
    parser.add_argument('--replace', action='store_true', help="Replace original files")
    parser.add_argument('--no-recursive', action='store_true', help="Don't process subdirectories")
    
    args = parser.parse_args()
    
    path = Path(args.path)
    if path.is_file():
        convert_to_webp(path, args.quality, args.replace)
    elif path.is_dir():
        process_directory(path, args.quality, args.replace, not args.no_recursive)
    else:
        print(f"Error: {path} is not a valid file or directory")
        return 1
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 