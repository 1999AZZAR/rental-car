# CV. Enam Satu Rentalindo - Flask Web Application

A Flask web application for CV. Enam Satu Rentalindo car rental service.

## Setup Instructions

### Prerequisites
- Python 3.7 or higher
- pip (Python package installer)

### Installation

1. Clone or download this repository
2. Navigate to the project directory:
   ```
   cd rental
   ```
3. Install the required dependencies:
   ```
   pip install -r requirements.txt
   ```

### Running the Application Locally

To run the application in development mode:
```
python app.py
```
The application will be available at http://127.0.0.1:5000/

### Deployment to Production

For deploying to a production environment, it's recommended to use a WSGI server like Gunicorn:

1. Install Gunicorn:
   ```
   pip install gunicorn
   ```

2. Run the application with Gunicorn:
   ```
   gunicorn -w 4 -b 0.0.0.0:8000 app:app
   ```

   - `-w 4`: Specifies 4 worker processes
   - `-b 0.0.0.0:8000`: Binds the server to all network interfaces on port 8000

3. For a more robust setup, consider using Nginx as a reverse proxy in front of Gunicorn.

### Deployment with Docker

You can also deploy this application using Docker:

1. Build the Docker image:
   ```
   docker build -t rental-app .
   ```

2. Run the Docker container:
   ```
   docker run -p 8000:8000 rental-app
   ```

### Utilities

#### WebP Image Converter
This project includes a utility to convert images to WebP format for better performance:

```
python convert_images.py
```

For more details, see [WebP Image Converter Documentation](utils/README.md).

#### Video Thumbnail Generator
Generate thumbnail images from videos for web display:

```
python generate_thumbnails.py
```

For more details, see [Video Thumbnail Generator Documentation](utils/VIDEO_THUMBNAILS.md).

### Project Structure

```
rental/
  ├── app.py          # Main Flask application
  ├── requirements.txt # Python dependencies
  ├── static/         # Static files (CSS, JS, images)
  │   ├── css/        # CSS files
  │   ├── js/         # JavaScript files
  │   ├── images/     # Image files
  │   ├── videos/     # Video files
  │   └── thumbnails/ # Video thumbnails
  ├── templates/      # HTML templates
  │   ├── index.html  # Home page
  │   ├── all-cars.html # All cars listing
  │   └── gallery.html # Gallery page
  ├── utils/          # Utility scripts
  │   ├── image_converter.py # WebP image conversion utility
  │   └── video_thumbnails.py # Video thumbnail generator
  ├── convert_images.py # Main image conversion script
  └── generate_thumbnails.py # Main thumbnail generation script
```

## License

This project is proprietary and owned by CV. Enam Satu Rentalindo.

## Contact

For any inquiries, please contact CV. Enam Satu Rentalindo. 