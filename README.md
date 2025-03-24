# ExplaVision

A sophisticated web-based face recognition system built with Django, YOLOv8, and DeepFace that provides real-time face detection and recognition capabilities with a modern, responsive interface.

## Features

- 👤 User Authentication System
  - Secure registration and login
  - Password reset functionality with email verification
  - Password change for logged-in users

- 🎯 Face Recognition Capabilities
  - Real-time face detection using YOLOv8
  - Advanced face recognition using DeepFace
  - Support for multiple faces in a single image
  - Confidence scoring for matches

- 📊 Face Management
  - Create, Read, Update, Delete (CRUD) operations for face records
  - Image upload with validation
  - Detailed view of stored faces
  - List view of all registered faces

- 🎨 Modern UI/UX
  - Responsive design using Tailwind CSS
  - Clean and intuitive interface
  - Real-time feedback and notifications
  - Mobile-friendly layout

## Technical Stack

### Backend
- **Framework**: Django 5.1.7
- **Authentication**: Django's built-in authentication system
- **Database**: SQLite3 (easily configurable for other databases)
- **Face Detection**: YOLOv8 (ultralytics)
- **Face Recognition**: DeepFace
- **Image Processing**: OpenCV (cv2)
- **File Storage**: Django's file storage system

### Frontend
- **CSS Framework**: Tailwind CSS
- **JavaScript**: Vanilla JS for real-time interactions
- **Templates**: Django Template Language (DTL)

### Additional Libraries
- NumPy: For numerical operations and array handling
- Pillow: For image processing
- python-dotenv: For environment variable management

## Installation

1. Clone the repository
```bash
git clone <repository-url>
cd tttt
```

2. Create and activate a virtual environment
```bash
python -m venv env
source env/bin/activate  # On Windows: env\Scripts\activate
```

3. Install required packages
```bash
pip install -r requirements.txt
```

4. Set up environment variables
- Create a .env file in the project root
- Add the following variables:
  ```
  DEBUG=True
  SECRET_KEY=your-secret-key
  EMAIL_BACKEND=django.core.mail.backends.smtp.EmailBackend
  EMAIL_HOST=smtp.gmail.com
  EMAIL_PORT=587
  EMAIL_USE_TLS=True
  EMAIL_HOST_USER=your-email@gmail.com
  EMAIL_HOST_PASSWORD=your-app-password
  PASSWORD_RESET_TIMEOUT=3600
  ```

5. Initialize the database
```bash
python manage.py migrate
```

6. Create a superuser (admin)
```bash
python manage.py createsuperuser
```

7. Download the YOLOv8 model
```bash
wget https://github.com/ultralytics/assets/releases/download/v0.0.0/yolov8n.pt
```

8. Run the development server
```bash
python manage.py runserver
```

## Usage

### Face Registration
1. Log in to the system
2. Navigate to "Manage Faces"
3. Click "Add New Face"
4. Enter the person's name and upload a clear face image
5. Submit to add the face to the database

### Face Recognition
1. Access the main dashboard
2. Use the camera or upload an image
3. The system will:
   - Detect faces using YOLOv8
   - Compare detected faces with the database using DeepFace
   - Display results with confidence scores

### User Management
- New users can register with email and password
- Password reset available via email
- Users can change their password when logged in
- Admin interface available at /admin for superusers

## Project Structure

```
tttt/
├── core/                   # Main application
│   ├── models.py          # Database models
│   ├── views.py           # View logic
│   ├── forms.py           # Form definitions
│   └── urls.py            # URL routing
├── templates/             # HTML templates
│   ├── faces/            # Face management templates
│   └── registration/     # Auth templates
├── media/                # Uploaded files
│   └── faces/           # Stored face images
├── frecog/              # Project settings
└── manage.py           # Django management script
```

## Security Features

- Password hashing using Django's auth system
- CSRF protection
- Secure password reset tokens
- Protected file uploads
- Login required middleware
- Environment variable configuration

## Performance Considerations

- YOLOv8n model used for faster detection
- Image processing optimizations
- Efficient database queries
- Caching capabilities

## Limitations and Considerations

- YOLOv8n is the smallest model - consider YOLOv8m for better accuracy
- Face recognition accuracy depends on image quality
- Local storage of face images - consider cloud storage for production
- SQLite database - consider PostgreSQL/MongoDB for production
