# Fatmug Django Developer Assignment

## Project Description

This project is a part of the **Fatmug Django Developer Assignment** aimed at developing, maintaining, and optimizing backend infrastructure for handling video uploads and processing. The project is a web-based platform that allows users to upload videos, process them in the background, extract subtitles using **FFmpeg**, and search within videos based on phrases.

## Features

1. **Video Upload and Processing**: 
   - Users can upload videos.
   - The system processes the videos in the background and extracts subtitles.
   - Subtitles are integrated with the video and displayed as closed captions.

2. **Search Functionality**:
   - A case-insensitive search feature allows users to search for phrases within videos.
   - Search results include timestamps, and clicking a timestamp will play the video starting at the selected time.

3. **List View for Uploaded Videos**:
   - The system provides a list view for all uploaded videos.
   - Users can select videos to view them along with the extracted subtitles.

## Requirements
- **FFmpeg**: Download the application from the trusted website and store it in the project directory.
- **Docker**: The entire application is containerized using **Docker**. A `docker-compose.yml` file is included for easy setup.
- **Backend**: The backend is developed using **Django**.
- **Storage**: Processed videos are stored in the Django media folder, while subtitles are saved in the **PostgreSQL** database.

## Technologies Used

- **Django**: Backend framework
- **PostgreSQL**: Database for storing video metadata and extracted subtitles
- **FFmpeg**: For extracting subtitles from videos
- **Docker**: For containerizing the application and services

## URL Patterns

The following URL routes are defined for this application:

```python
from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),                   # User registration
    path('accounts/login/', views.login_view, name='login'),              # User login
    path('accounts/logout/', views.logout_view, name='logout'),           # User logout
    path('upload_video/', views.upload_video, name='upload_video'),       # Video upload
    path('video/<int:video_id>/', views.display_video_with_search, name='display_video_with_search'),  # View video with search functionality
    path('', views.video_list, name='video_list'),                        # List view of all uploaded videos
]
```

### Endpoints:

1. **`/register/`**: User registration page.
2. **`/accounts/login/`**: User login page.
3. **`/accounts/logout/`**: User logout.
4. **`/upload_video/`**: Page to upload new videos.
5. **`/video/<int:video_id>/`**: Display video with integrated subtitles and search functionality.
6. **`/`**: List view for all uploaded videos.

## Setup and Installation

1. **Clone the Repository**:
   ```bash
   git clone <your-repo-url>
   cd my_project
   ```

2. **Install Dependencies**:
   Install the required Python packages:
   ```bash
   pip install -r requirements.txt
   ```

3. **Setup PostgreSQL Database**:
   Ensure that PostgreSQL is installed and running. Update the database credentials in your `settings.py` file.

4. **FFmpeg Setup**:
   Download and install **FFmpeg** from [here](https://ffmpeg.org/download.html).

5. **Run Database Migrations**:
   Apply the database migrations:
   ```bash
   python manage.py migrate
   ```

6. **Run the Application**:
   Start the Django development server:
   ```bash
   python manage.py runserver
   ```

7. **Docker Setup**:
   Alternatively, you can run the project using Docker:
   - Build and start the containers:
     ```bash
     docker-compose up --build
     ```

8. **Access the Application**:
   Open your browser and go to `http://localhost:8000/` to access the app.

## Testing

- The web application should be able to process and handle the provided sample video.
- Screenshots of the application in action should be saved in the `screenshots/` folder.
  
## Submission

- After completing the assignment, upload the project to **GitHub** and provide the repository link.
  
## Example Screenshots

Make sure to add example screenshots of the following:
1. Video upload page.
2. Video list view.
3. Video display page with subtitles and search functionality.



---
