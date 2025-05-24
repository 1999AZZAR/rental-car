# WebP Image Converter

This utility helps you convert images to WebP format, which provides superior compression and quality for web use.

## Benefits of WebP

- **Smaller file sizes**: WebP images are typically 25-34% smaller than JPEGs at equivalent visual quality
- **Faster loading times**: Smaller files load faster on your website
- **Support for transparency**: Like PNG but with better compression
- **Browser support**: Most modern browsers now support WebP

## Usage

### Basic Usage

To convert all images in the default directory (`static/assets/images`):

```bash
python convert_images.py
```

This will create WebP versions of all images without deleting the originals.

### Advanced Options

```bash
python convert_images.py --dir path/to/images --quality 85 --replace
```

Parameters:
- `--dir`: Directory containing images to convert (default: `static/assets/images`)
- `--quality`: WebP quality from 0-100 (default: 80, higher means better quality but larger files)
- `--replace`: Replace original files with WebP versions (use with caution)
- `--no-recursive`: Don't process subdirectories

## Installation

Before using this tool, ensure you have the Pillow library installed:

```bash
pip install -r requirements.txt
```

## Updating Your HTML

After converting images to WebP, update your HTML to use the new images:

```html
<!-- Before -->
<img src="/static/assets/images/photo.jpg" alt="Photo">

<!-- After -->
<img src="/static/assets/images/photo.webp" alt="Photo">
```

For browsers that don't support WebP, you can use the picture element:

```html
<picture>
  <source srcset="/static/assets/images/photo.webp" type="image/webp">
  <img src="/static/assets/images/photo.jpg" alt="Photo">
</picture>
``` 