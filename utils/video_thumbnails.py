#!/usr/bin/env python3
"""
Video Thumbnail Generator

This script extracts thumbnail images from video files.
It uses OpenCV to capture frames from videos and saves them as image files.
"""

import os
import sys
import argparse
import cv2
from pathlib import Path
from PIL import Image, ImageEnhance


def extract_thumbnail(video_path, output_path=None, timestamp=1.0, quality=85, format='webp', 
                      enhance=False, width=None, brightness=1.0, contrast=1.0, saturation=1.2):
    """
    Extract a thumbnail from a video at a specific timestamp
    
    Args:
        video_path (str): Path to the video file
        output_path (str): Path to save the thumbnail
        timestamp (float): Time in seconds to extract the frame
        quality (int): Image quality (0-100)
        format (str): Output format ('webp', 'jpg', 'png')
        enhance (bool): Whether to enhance the thumbnail
        width (int): Resize width (keeps aspect ratio if set)
        brightness (float): Brightness factor (1.0 = original)
        contrast (float): Contrast factor (1.0 = original)
        saturation (float): Saturation factor (1.0 = original)
        
    Returns:
        str: Path to the saved thumbnail
    """
    # Get video path as Path object
    video_file = Path(video_path)
    
    # Check if file exists
    if not video_file.exists():
        print(f"Error: Video file {video_path} does not exist")
        return None
    
    # Create output path if not specified
    if output_path is None:
        output_path = video_file.with_name(f"{video_file.stem}_thumbnail.{format.lower()}")
    else:
        output_path = Path(output_path)
        # If output is a directory, create filename in that directory
        if output_path.is_dir():
            output_path = output_path / f"{video_file.stem}_thumbnail.{format.lower()}"
    
    try:
        # Open the video file
        video = cv2.VideoCapture(str(video_file))
        
        # Check if video opened successfully
        if not video.isOpened():
            print(f"Error: Could not open video {video_path}")
            return None
        
        # Get video properties
        fps = video.get(cv2.CAP_PROP_FPS)
        total_frames = int(video.get(cv2.CAP_PROP_FRAME_COUNT))
        duration = total_frames / fps if fps > 0 else 0
        
        # If timestamp is beyond video duration, use middle of video
        if timestamp > duration:
            print(f"Warning: Timestamp {timestamp}s exceeds video duration {duration:.2f}s, using middle frame")
            timestamp = duration / 2
        
        # Convert timestamp to frame number
        frame_number = int(timestamp * fps)
        
        # Set video position to the specified frame
        video.set(cv2.CAP_PROP_POS_FRAMES, frame_number)
        
        # Read the frame
        success, frame = video.read()
        
        # Close the video file
        video.release()
        
        if not success:
            print(f"Error: Could not read frame at {timestamp}s from {video_path}")
            return None
        
        # Convert BGR to RGB (OpenCV uses BGR, PIL uses RGB)
        frame_rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        
        # Convert to PIL Image
        img = Image.fromarray(frame_rgb)
        
        # Resize if width is specified
        if width is not None:
            aspect_ratio = img.width / img.height
            new_height = int(width / aspect_ratio)
            img = img.resize((width, new_height), Image.LANCZOS)
        
        # Enhance image if requested
        if enhance:
            # Brightness
            if brightness != 1.0:
                enhancer = ImageEnhance.Brightness(img)
                img = enhancer.enhance(brightness)
            
            # Contrast
            if contrast != 1.0:
                enhancer = ImageEnhance.Contrast(img)
                img = enhancer.enhance(contrast)
            
            # Saturation
            if saturation != 1.0:
                enhancer = ImageEnhance.Color(img)
                img = enhancer.enhance(saturation)
        
        # Save the image
        if format.lower() == 'webp':
            img.save(str(output_path), 'WEBP', quality=quality)
        elif format.lower() == 'jpg' or format.lower() == 'jpeg':
            img.save(str(output_path), 'JPEG', quality=quality)
        elif format.lower() == 'png':
            img.save(str(output_path), 'PNG')
        else:
            print(f"Error: Unsupported format {format}")
            return None
        
        print(f"Thumbnail saved to {output_path}")
        return str(output_path)
    
    except Exception as e:
        print(f"Error processing {video_path}: {e}")
        return None


def process_videos(directory, output_dir=None, timestamp=1.0, quality=85, format='webp', 
                  enhance=False, width=None, recursive=True, 
                  brightness=1.0, contrast=1.0, saturation=1.2):
    """
    Process all videos in a directory
    
    Args:
        directory (str): Directory containing videos
        output_dir (str): Directory to save thumbnails
        timestamp (float): Time in seconds to extract frames
        quality (int): Image quality (0-100)
        format (str): Output format ('webp', 'jpg', 'png')
        enhance (bool): Whether to enhance thumbnails
        width (int): Resize width (keeps aspect ratio if set)
        recursive (bool): Whether to process subdirectories
        brightness (float): Brightness factor (1.0 = original)
        contrast (float): Contrast factor (1.0 = original)
        saturation (float): Saturation factor (1.0 = original)
    """
    # Get directory as Path object
    dir_path = Path(directory)
    
    # Check if directory exists
    if not dir_path.exists():
        print(f"Error: Directory {directory} does not exist")
        return
    
    # Create output directory if specified
    if output_dir is not None:
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)
    else:
        output_path = None
    
    # Video extensions to process
    video_extensions = {'.mp4', '.avi', '.mov', '.mkv', '.webm', '.flv', '.wmv'}
    
    # Get all files in directory
    if recursive:
        all_files = list(dir_path.glob('**/*.*'))
    else:
        all_files = list(dir_path.glob('*.*'))
    
    # Filter video files
    video_files = [f for f in all_files if f.suffix.lower() in video_extensions]
    
    if not video_files:
        print(f"No videos found in {directory}")
        return
    
    print(f"Found {len(video_files)} videos to process")
    
    # Process all videos
    processed_count = 0
    for video_file in video_files:
        # Create output path for this video
        if output_path is not None:
            # Preserve directory structure if recursive
            if recursive:
                rel_path = video_file.relative_to(dir_path)
                # Just keep the filename, not subdirectories
                video_output = output_path / f"{rel_path.stem}_thumbnail.{format.lower()}"
            else:
                video_output = output_path / f"{video_file.stem}_thumbnail.{format.lower()}"
        else:
            video_output = None
        
        if extract_thumbnail(
            video_file, video_output, timestamp, quality, format, 
            enhance, width, brightness, contrast, saturation
        ):
            processed_count += 1
    
    print(f"Processing complete. Generated {processed_count} thumbnails.")


def main():
    parser = argparse.ArgumentParser(description="Generate thumbnails from video files")
    
    # Input options
    parser.add_argument('--dir', default='static/assets/videos',
                      help="Directory containing videos (default: static/assets/videos)")
    parser.add_argument('--output', default='static/assets/thumbnails',
                      help="Directory to save thumbnails (default: static/assets/thumbnails)")
    
    # Thumbnail options
    parser.add_argument('--timestamp', type=float, default=1.0,
                      help="Time in seconds to extract frame (default: 1.0)")
    parser.add_argument('--quality', type=int, default=85,
                      help="Image quality from 0-100 (default: 85)")
    parser.add_argument('--format', choices=['webp', 'jpg', 'png'], default='webp',
                      help="Output format: webp, jpg, or png (default: webp)")
    parser.add_argument('--width', type=int, default=640,
                      help="Resize width in pixels, preserves aspect ratio (default: 640)")
    
    # Enhancement options
    parser.add_argument('--enhance', action='store_true',
                      help="Enhance thumbnail appearance")
    parser.add_argument('--brightness', type=float, default=1.0,
                      help="Brightness adjustment factor (default: 1.0)")
    parser.add_argument('--contrast', type=float, default=1.1,
                      help="Contrast adjustment factor (default: 1.1)")
    parser.add_argument('--saturation', type=float, default=1.2,
                      help="Saturation adjustment factor (default: 1.2)")
    
    # Other options
    parser.add_argument('--no-recursive', action='store_true',
                      help="Don't process subdirectories")
    
    args = parser.parse_args()
    
    # Create output directory if it doesn't exist
    os.makedirs(args.output, exist_ok=True)
    
    # Process videos
    print(f"Generating thumbnails from videos in '{args.dir}'")
    print(f"Saving thumbnails to '{args.output}'")
    process_videos(
        args.dir, args.output, args.timestamp, args.quality, args.format,
        args.enhance, args.width, not args.no_recursive,
        args.brightness, args.contrast, args.saturation
    )
    
    return 0


if __name__ == "__main__":
    sys.exit(main()) 