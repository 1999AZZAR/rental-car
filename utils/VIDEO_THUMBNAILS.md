# Video Thumbnail Generator

This utility helps you generate thumbnail images from video files for web display.

## Features

- **Automatic frame extraction**: Extract frames at specified timestamps
- **Batch processing**: Process multiple videos at once
- **Image enhancement**: Automatically enhance thumbnails for better appearance
- **WebP support**: Generate thumbnails in optimized WebP format
- **Customizable quality**: Control the quality and size of generated thumbnails

## Usage

### Basic Usage

To generate thumbnails for all videos in the default directory (`static/assets/videos`):

```bash
python generate_thumbnails.py
```

This will create thumbnail images in the `static/assets/thumbnails` directory.

### Advanced Options

```bash
python generate_thumbnails.py --dir path/to/videos --output path/to/save --timestamp 2.5 --enhance
```

Parameters:

#### Input/Output Options
- `--dir`: Directory containing videos (default: `static/assets/videos`)
- `--output`: Directory to save thumbnails (default: `static/assets/thumbnails`)

#### Thumbnail Options
- `--timestamp`: Time in seconds to extract frame (default: 1.0)
- `--quality`: Image quality from 0-100 (default: 85)
- `--format`: Output format: webp, jpg, or png (default: webp)
- `--width`: Resize width in pixels, preserves aspect ratio (default: 640)

#### Enhancement Options
- `--enhance`: Enhance thumbnail appearance (improves contrast and saturation)
- `--brightness`: Brightness adjustment factor (default: 1.0)
- `--contrast`: Contrast adjustment factor (default: 1.1)
- `--saturation`: Saturation adjustment factor (default: 1.2)

## Installation

Before using this tool, ensure you have the required libraries installed:

```bash
pip install -r requirements.txt
```

This will install:
- Pillow: For image processing
- OpenCV: For video processing

## Usage in HTML

After generating thumbnails, you can use them in your HTML to display video previews:

```html
<div class="video-thumbnail">
  <a href="/static/assets/videos/video.mp4">
    <img src="/static/assets/thumbnails/video_thumbnail.webp" alt="Video Thumbnail">
    <div class="play-button"></div>
  </a>
</div>
```

You can style the thumbnail with CSS to add a play button overlay:

```css
.video-thumbnail {
  position: relative;
}

.play-button {
  position: absolute;
  top: 50%;
  left: 50%;
  transform: translate(-50%, -50%);
  width: 0;
  height: 0;
  border-top: 20px solid transparent;
  border-bottom: 20px solid transparent;
  border-left: 30px solid rgba(255, 255, 255, 0.8);
}

.video-thumbnail:hover .play-button {
  border-left-color: rgba(255, 255, 255, 1);
}
``` 