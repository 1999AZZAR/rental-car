#!/usr/bin/env python3
"""
Image Converter Tool

This script provides a convenient way to convert images to WebP format.
It automatically detects and converts images in specified directories.
"""

import os
import sys
import argparse
from utils.image_converter import process_directory

def main():
    parser = argparse.ArgumentParser(description="Convert images to WebP format for web optimization")
    parser.add_argument('--dir', default='static/assets/images', 
                      help="Directory containing images to convert (default: static/assets/images)")
    parser.add_argument('--quality', type=int, default=80, 
                      help="WebP quality from 0-100 (default: 80)")
    parser.add_argument('--replace', action='store_true', 
                      help="Replace original files with WebP versions")
    parser.add_argument('--no-recursive', action='store_true', 
                      help="Don't process subdirectories")
    
    args = parser.parse_args()
    
    # Ensure the directory exists
    if not os.path.exists(args.dir):
        print(f"Error: Directory '{args.dir}' does not exist")
        return 1
    
    # Process the directory
    print(f"Converting images in '{args.dir}' to WebP format (quality: {args.quality})")
    if args.replace:
        print("Original files will be replaced with WebP versions")
    
    process_directory(args.dir, args.quality, args.replace, not args.no_recursive)
    return 0

if __name__ == "__main__":
    sys.exit(main()) 