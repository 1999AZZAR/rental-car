#!/usr/bin/env python3
"""
Video Thumbnail Generator Tool

This script generates thumbnail images from videos for web display.
"""

import os
import sys
import argparse
from utils.video_thumbnails import process_videos
import glob
from PIL import Image
import subprocess

def generate_image_thumbnails(source_dir, target_dir, size=(400, 300)):
    """Generate thumbnails for images in the source directory and save to target directory."""
    # Create target directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)
    
    # Find all image files
    image_extensions = ['*.jpg', '*.jpeg', '*.png', '*.webp']
    image_files = []
    for ext in image_extensions:
        image_files.extend(glob.glob(os.path.join(source_dir, ext)))
    
    if not image_files:
        print(f"No image files found in {source_dir}")
        return
    
    # Process each image file
    for img_path in image_files:
        filename = os.path.basename(img_path)
        name, ext = os.path.splitext(filename)
        thumbnail_path = os.path.join(target_dir, f"{name}.webp")
        
        # Skip if thumbnail already exists
        if os.path.exists(thumbnail_path):
            print(f"Thumbnail already exists for {filename}, skipping...")
            continue
        
        try:
            # Open and resize image
            with Image.open(img_path) as img:
                img = img.convert('RGB')  # Convert to RGB mode for webp conversion
                img.thumbnail(size)
                
                # Save as webp with good quality and compression
                img.save(thumbnail_path, 'WEBP', quality=85)
                print(f"Generated thumbnail for {filename} -> {thumbnail_path}")
        except Exception as e:
            print(f"Error generating thumbnail for {filename}: {e}")

def generate_video_thumbnails(source_dir, target_dir, size=(400, 300)):
    """Generate thumbnails for videos in the source directory and save to target directory."""
    # Create target directory if it doesn't exist
    os.makedirs(target_dir, exist_ok=True)
    
    # Find all video files
    video_extensions = ['*.mp4', '*.mov', '*.avi', '*.mkv']
    video_files = []
    for ext in video_extensions:
        video_files.extend(glob.glob(os.path.join(source_dir, ext)))
    
    if not video_files:
        print(f"No video files found in {source_dir}")
        return
    
    # Process each video file
    for video_path in video_files:
        filename = os.path.basename(video_path)
        name, ext = os.path.splitext(filename)
        thumbnail_path = os.path.join(target_dir, f"{name}.webp")
        
        # Skip if thumbnail already exists
        if os.path.exists(thumbnail_path):
            print(f"Thumbnail already exists for {filename}, skipping...")
            continue
        
        try:
            # Extract frame from the middle of the video using ffmpeg
            temp_jpg = os.path.join(target_dir, f"{name}_temp.jpg")
            
            # Extract frame at 1 second to avoid black frames at the beginning
            cmd = [
                'ffmpeg', 
                '-i', video_path, 
                '-ss', '00:00:01', 
                '-frames:v', '1', 
                '-q:v', '2',
                temp_jpg
            ]
            
            print(f"Extracting frame from {filename}...")
            subprocess.run(cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            
            # Resize and convert to webp
            with Image.open(temp_jpg) as img:
                img = img.convert('RGB')
                img.thumbnail(size)
                img.save(thumbnail_path, 'WEBP', quality=85)
            
            # Remove temporary jpg file
            os.remove(temp_jpg)
            print(f"Generated thumbnail for {filename} -> {thumbnail_path}")
            
        except Exception as e:
            print(f"Error generating thumbnail for {filename}: {e}")
            # If the file exists, clean up
            if os.path.exists(temp_jpg):
                os.remove(temp_jpg)

def create_placeholder_image(target_dir, size=(400, 300)):
    """Create a placeholder image for videos without thumbnails"""
    placeholder_path = os.path.join(target_dir, "video-placeholder.webp")
    
    if os.path.exists(placeholder_path):
        print(f"Video placeholder already exists at {placeholder_path}")
        return
    
    # Create a dark gray placeholder with a video play icon
    img = Image.new('RGB', size, color=(51, 51, 51))
    
    # Save as webp
    img.save(placeholder_path, 'WEBP', quality=85)
    print(f"Created video placeholder: {placeholder_path}")

def main():
    parser = argparse.ArgumentParser(description="Generate thumbnails for images and videos")
    parser.add_argument('--images', action='store_true', help='Generate thumbnails for images')
    parser.add_argument('--videos', action='store_true', help='Generate thumbnails for videos')
    parser.add_argument('--all', action='store_true', help='Generate thumbnails for both images and videos')
    parser.add_argument('--image-dir', default='static/assets/images', help='Source directory for images')
    parser.add_argument('--video-dir', default='static/assets/videos', help='Source directory for videos')
    parser.add_argument('--thumbnail-dir', default='static/assets/thumbnails', help='Target directory for thumbnails')
    parser.add_argument('--width', type=int, default=400, help='Thumbnail width')
    parser.add_argument('--height', type=int, default=300, help='Thumbnail height')
    
    args = parser.parse_args()
    
    # If no specific option is provided, process both
    if not (args.images or args.videos or args.all):
        args.all = True
    
    size = (args.width, args.height)
    
    # Create placeholder image
    create_placeholder_image(args.thumbnail_dir, size)
    
    # Process based on options
    if args.images or args.all:
        print(f"Generating image thumbnails from {args.image_dir} to {args.thumbnail_dir}...")
        generate_image_thumbnails(args.image_dir, args.thumbnail_dir, size)
    
    if args.videos or args.all:
        print(f"Generating video thumbnails from {args.video_dir} to {args.thumbnail_dir}...")
        generate_video_thumbnails(args.video_dir, args.thumbnail_dir, size)
    
    return 0

if __name__ == "__main__":
    sys.exit(main()) 