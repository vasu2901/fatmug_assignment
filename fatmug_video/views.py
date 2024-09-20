from django.shortcuts import render, redirect
from django.contrib.auth import logout as auth_logout, login as auth_login, authenticate
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from .models import Video, Subtitle
from .forms import UserRegistrationForm 
import subprocess
import os
from django.conf import settings

from django.contrib.auth import get_user_model

User = get_user_model()  # Get the custom user model

# Directory to store uploaded files
MEDIA_DIR = settings.MEDIA_ROOT


def register(request):
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password1')
            user = authenticate(username=username, password=password)
            if user:
                auth_login(request, user)
                return redirect('video_list')
    else:
        form = UserRegistrationForm()   
    return render(request, 'register.html', {'form': form})

# Login view
def login_view(request):
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                auth_login(request, user)
                return redirect('video_list')
            else:
                return redirect('upload')
    else:
        form = AuthenticationForm()
    return render(request, 'login.html', {'form': form})

# Logout view
@login_required
def logout_view(request):
    if request.method != 'POST':
        auth_logout(request)
        return redirect('login')
    else:
        return redirect('upload')

# Upload video view (only accessible to logged-in users)
@login_required
def upload_video(request):
    if request.method == 'POST':
        video_file = request.FILES['video']  # Get the uploaded video file
        title = request.POST.get('title', 'Untitled Video')

        # Save the video file and metadata
        video = Video.objects.create(
            title=title,
            file=video_file,  # This will automatically store the file in 'media/videos/'
            user=request.user
        )

        # File is now stored in media/videos/; we can now process the file
        video_path = video.file.path  # This will give the absolute file path of the uploaded video

        # Process the video to extract subtitles
        process_video(video, video_path)

        return redirect('display_video_with_search', video_id=video.id)  
    
    return render(request, 'upload_video.html')

# Helper function to process and extract subtitles
def process_video(video, video_path):
    subtitle_languages = ['en', 'es', 'fr']  # Example list of languages
    subtitles_data = {}

    for lang in subtitle_languages:
        subtitle_path_srt = os.path.join(settings.MEDIA_ROOT, 'subtitles', f"{video.user.id}-{video.title}.srt")
        subtitle_path_vtt = os.path.join(settings.MEDIA_ROOT, 'subtitles', f"{video.user.id}-{video.title}.vtt")
        
        # Ensure the directory for subtitles exists
        if not os.path.exists(os.path.dirname(subtitle_path_srt)):
            os.makedirs(os.path.dirname(subtitle_path_srt))

        try:
            # Extract subtitles using FFmpeg to SRT format
            command = [
                'ffmpeg','-y', '-i', video_path,
                '-map', '0:s:0', '-c:s', 'srt',
                subtitle_path_srt
            ]
            subprocess.run(command, check=True)
            # Read and process the generated subtitle file
            convert_srt_to_vtt(subtitle_path_srt, subtitle_path_vtt)
            with open(subtitle_path_srt, 'r', encoding='utf-8') as f:
                subtitle_lines = f.readlines()

            current_subtitle = []
            timestamp = None

            # Parse the SRT file and store each subtitle in the database
            for line in subtitle_lines:
                line = line.strip()

                if '-->' in line:
                    timestamp = line
                elif line.isdigit():
                    continue
                elif line == "":  # End of current subtitle
                    if current_subtitle:
                        text = " ".join(current_subtitle)
                        Subtitle.objects.create(
                            video=video,
                            language=lang,
                            text=text,
                            timestamp=timestamp
                        )
                        current_subtitle = []
                else:
                    current_subtitle.append(line)

            subtitles_data[lang] = os.path.join(settings.MEDIA_URL, 'subtitles', f"{video.user.id}-{video.title}-{lang}.srt")

        except Exception as e:
            print(f"Error while extracting {lang} subtitles: {e}")

    return subtitles_data

# Convert SRT file to VTT format
def convert_srt_to_vtt(srt_file_path, vtt_file_path):
    try:
        with open(srt_file_path, 'r', encoding='utf-8') as srt_file:
            srt_content = srt_file.read()

        # WebVTT files need to start with a 'WEBVTT' header
        vtt_content = 'WEBVTT\n\n'

        # Replace SRT timestamp format with VTT format
        vtt_content += srt_content.replace(',', '.')

        # Save the VTT content to the new VTT file
        with open(vtt_file_path, 'w', encoding='utf-8') as vtt_file:
            vtt_file.write(vtt_content)

    except Exception as e:
        print(f"Error while converting SRT to VTT: {e}")


@login_required
def display_video_with_search(request, video_id):
    video = Video.objects.get(id=video_id)
    subtitles = Subtitle.objects.filter(video=video)
    # print(list(set(subtitles)))
    seen_subtitles = set()
    unique_subtitles = []

    # Loop through all subtitles and add only unique ones
    for subtitle in subtitles:
        # Create a unique identifier (tuple) for each subtitle
        subtitle_key = (subtitle.text, subtitle.timestamp)
        
        # If this subtitle is not already seen, add it to the unique list
        if subtitle_key not in seen_subtitles:
            seen_subtitles.add(subtitle_key)
            unique_subtitles.append(subtitle)

    # Prepare subtitles for the template
    subtitles_data = [
        {'text': subtitle.text, 'timestamp': subtitle.timestamp} for subtitle in unique_subtitles
    ]

    # Serialize subtitles_data to JSON
    # subtitles_json = json.dumps(subtitles_data)
    return render(request, 'display_video_with_search.html', {
    'video': video, 
    'subtitle_file': f"/media/subtitles/{video.user.id}-{video.title}.vtt",
    'subtitles_data': subtitles_data,
})


@login_required
def video_list(request):
    videos = Video.objects.filter(user=request.user)
    return render(request, 'video_list.html', {'videos': videos})
