from flask import Flask, render_template, jsonify, request, url_for, Response
import os
import glob
import math
import random
import xml.etree.ElementTree as ET
from datetime import datetime

app = Flask(__name__)


@app.route("/")
@main_blueprint.route("/home")
def index():
    return render_template("index.html")


@app.route("/all-cars")
def all_cars():
    return render_template("all-cars.html")


@app.route("/gallery")
def gallery():
    return render_template("gallery.html")


@app.route("/api/gallery/images")
def gallery_images():
    """API endpoint to serve gallery images data with pagination"""
    # Get pagination parameters
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 9))  # Default to 9 images per page

    # Get all image files from static/assets/images directory
    image_dir = os.path.join(app.static_folder, "assets/images")

    # Check if directory exists
    if not os.path.exists(image_dir):
        return jsonify(
            {
                "error": "Image directory not found",
                "images": [],
                "total": 0,
                "total_pages": 0,
                "page": page,
                "per_page": per_page,
            }
        )

    # Get all webp images
    image_paths = glob.glob(os.path.join(image_dir, "*.webp"))

    # Sort images by name
    image_paths.sort()

    # Calculate pagination
    total_images = len(image_paths)
    total_pages = math.ceil(total_images / per_page)

    # Adjust page if out of range
    if page < 1:
        page = 1
    elif page > total_pages and total_pages > 0:
        page = total_pages

    # Calculate start and end indices
    start_idx = (page - 1) * per_page
    end_idx = min(start_idx + per_page, total_images)

    # Get paginated images
    paginated_paths = image_paths[start_idx:end_idx]

    # Format image data for the frontend
    images = []
    for i, path in enumerate(paginated_paths, start=start_idx + 1):
        filename = os.path.basename(path)
        images.append(
            {
                "id": i,  # Using 1-based index
                "filename": filename,
                "path": f"/static/assets/images/{filename}",
                "title": f"Armada Mobil CV. Enam Satu Rentalindo #{i}",
            }
        )

    return jsonify(
        {
            "images": images,
            "total": total_images,
            "total_pages": total_pages,
            "page": page,
            "per_page": per_page,
        }
    )


@app.route("/api/gallery/videos")
def gallery_videos():
    """API endpoint to serve gallery videos data with pagination"""
    # Get pagination parameters
    page = int(request.args.get("page", 1))
    per_page = int(request.args.get("per_page", 8))  # Default to 8 videos per page

    # Get all video files from static/assets/videos directory
    video_dir = os.path.join(app.static_folder, "assets/videos")
    thumbnails_dir = os.path.join(app.static_folder, "assets/thumbnails")

    # Check if directories exist
    if not os.path.exists(video_dir):
        return jsonify(
            {
                "error": "Video directory not found",
                "videos": [],
                "total": 0,
                "total_pages": 0,
                "page": page,
                "per_page": per_page,
            }
        )

    # Get all mp4 videos
    video_paths = glob.glob(os.path.join(video_dir, "*.mp4"))

    # Sort videos by name
    video_paths.sort()

    # Calculate pagination
    total_videos = len(video_paths)
    total_pages = math.ceil(total_videos / per_page)

    # Adjust page if out of range
    if page < 1:
        page = 1
    elif page > total_pages and total_pages > 0:
        page = total_pages

    # Calculate start and end indices
    start_idx = (page - 1) * per_page
    end_idx = min(start_idx + per_page, total_videos)

    # Get paginated videos
    paginated_paths = video_paths[start_idx:end_idx]

    # Format video data for the frontend
    videos = []
    for i, path in enumerate(paginated_paths, start=start_idx + 1):
        filename = os.path.basename(path)
        basename = os.path.splitext(filename)[0]

        # Check if a thumbnail exists for this video
        thumbnail_filename = f"{basename}.webp"
        thumbnail_path = os.path.join(thumbnails_dir, thumbnail_filename)

        if os.path.exists(thumbnail_path):
            thumbnail_url = f"/static/assets/thumbnails/{thumbnail_filename}"
        else:
            # Fallback to a placeholder image
            thumbnail_url = f"/static/assets/thumbnails/video-placeholder.webp"

        videos.append(
            {
                "id": i,  # Using 1-based index
                "filename": filename,
                "path": f"/static/assets/videos/{filename}",
                "thumbnail": thumbnail_url,
                "title": f"Video Armada #{i}",
            }
        )

    return jsonify(
        {
            "videos": videos,
            "total": total_videos,
            "total_pages": total_pages,
            "page": page,
            "per_page": per_page,
        }
    )


@app.route("/api/gallery/random")
def gallery_random():
    """API endpoint to serve a random mix of images and videos for the homepage"""
    count = int(request.args.get("count", 8))  # Default to 8 items

    # Get all image and video files
    image_dir = os.path.join(app.static_folder, "assets/images")
    video_dir = os.path.join(app.static_folder, "assets/videos")
    thumbnails_dir = os.path.join(app.static_folder, "assets/thumbnails")

    images = []
    videos = []

    # Get images if directory exists
    if os.path.exists(image_dir):
        image_paths = glob.glob(os.path.join(image_dir, "*.webp"))
        for i, path in enumerate(image_paths, start=1):
            filename = os.path.basename(path)
            images.append(
                {
                    "id": i,
                    "type": "image",
                    "filename": filename,
                    "path": f"/static/assets/images/{filename}",
                    "title": f"Armada Mobil CV. Enam Satu Rentalindo #{i}",
                }
            )

    # Get videos if directory exists
    if os.path.exists(video_dir):
        video_paths = glob.glob(os.path.join(video_dir, "*.mp4"))
        for i, path in enumerate(video_paths, start=1):
            filename = os.path.basename(path)
            basename = os.path.splitext(filename)[0]

            # Check if a thumbnail exists for this video
            thumbnail_filename = f"{basename}.webp"
            thumbnail_path = os.path.join(thumbnails_dir, thumbnail_filename)

            if os.path.exists(thumbnail_path):
                thumbnail_url = f"/static/assets/thumbnails/{thumbnail_filename}"
            else:
                # Fallback to a placeholder image
                thumbnail_url = f"/static/assets/thumbnails/video-placeholder.webp"

            videos.append(
                {
                    "id": i,
                    "type": "video",
                    "filename": filename,
                    "path": f"/static/assets/videos/{filename}",
                    "thumbnail": thumbnail_url,
                    "title": f"Video Armada #{i}",
                }
            )

    # Combine and shuffle items
    all_items = images + videos

    if not all_items:
        return jsonify({"error": "No gallery items found", "items": []})

    # Shuffle and limit to requested count
    random.shuffle(all_items)
    random_items = all_items[: min(count, len(all_items))]

    return jsonify({"items": random_items})


def add_url_to_sitemap(urlset, loc, lastmod=None, changefreq=None, priority=None):
    """Helper function to add a URL to the sitemap."""
    url = ET.SubElement(urlset, "url")
    ET.SubElement(url, "loc").text = loc

    if lastmod:
        if isinstance(lastmod, datetime):
            lastmod_str = lastmod.strftime("%Y-%m-%d")
        else:
            lastmod_str = str(lastmod)
        ET.SubElement(url, "lastmod").text = lastmod_str

    if changefreq:
        ET.SubElement(url, "changefreq").text = changefreq

    if priority is not None:
        ET.SubElement(url, "priority").text = str(priority)


@app.route("/sitemap.xml")
def sitemap():
    """Generates the sitemap.xml dynamically."""
    try:
        # Create the root <urlset> element with namespace
        urlset = ET.Element(
            "urlset", xmlns="http://www.sitemaps.org/schemas/sitemap/0.9"
        )

        # Define static pages for this rental car website
        static_endpoints = [
            ("index", "daily", 1.0),  # Homepage
            ("all_cars", "weekly", 0.8),  # All cars listing
            ("gallery", "weekly", 0.7),  # Gallery page
        ]

        # Get current date for lastmod
        today = datetime.now().strftime("%Y-%m-%d")

        # Add all static pages to sitemap
        for endpoint, changefreq, priority in static_endpoints:
            try:
                loc = url_for(endpoint, _external=True)
                add_url_to_sitemap(
                    urlset, loc, lastmod=today, changefreq=changefreq, priority=priority
                )
            except Exception as e:
                app.logger.warning(
                    f"Sitemap: Could not generate URL for static endpoint '{endpoint}': {e}"
                )

        # Convert the ElementTree to an XML string
        sitemap_xml_string = ET.tostring(urlset, encoding="unicode", method="xml")

        # Add the XML declaration
        final_xml = '<?xml version="1.0" encoding="UTF-8"?>\n' + sitemap_xml_string

        return Response(final_xml, mimetype="application/xml")

    except Exception as err:
        app.logger.error(f"Sitemap generation failed due to unexpected error: {err}")
        return Response("Error generating sitemap", status=500, mimetype="text/plain")


if __name__ == "__main__":
    app.run(debug=True, threaded=False)
