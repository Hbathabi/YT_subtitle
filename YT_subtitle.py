import yt_dlp
import os

def print_available_subtitles(video_url):
    output_directory = "subtitles"
    os.makedirs(output_directory, exist_ok=True)

    # yt-dlp options with improved readability
    options = {
        'writesubtitles': True,  # Enable subtitle download
        'skip_download': True,  # Skip downloading the video
        'listsubtitles': True,  # List available subtitles
        'subtitleslangs': [],   # Initially empty, will be populated later
        'subtitlesformat': None # Initially empty, will be populated later
    }
    try:
        # Create a yt-dlp object
        ydl = yt_dlp.YoutubeDL(options)

        # Download video information
        info_dict = ydl.extract_info(video_url, download=False)

        # Check if subtitles are available
        subtitles = info_dict.get('subtitles', {})
        if not subtitles:
            print("No subtitles available for this video.")
            return

        # Print available subtitles
        print("Available subtitles:")
        available_languages = []
        for lang, subs in subtitles.items():
            available_languages.append(lang)
            print(f"Language: {lang}")
            for sub in subs:
                print(f"\tFormat: {sub['ext']}")

        # Get user input for language and format with error handling
        while True:
            selected_language = input("Enter the language code of the subtitles you want to download (or 'q' to quit): ")
            if selected_language.lower() == 'q':
                return
            if selected_language not in available_languages:
                print(f"Invalid language code: {selected_language}. Please choose from available languages: {', '.join(available_languages)}")
                continue

            selected_format = input("Enter the format of the subtitles you want to download (or leave empty for default): ")
            if not selected_format:
                # Use the first available format if none chosen
                selected_format = subtitles[selected_language][0]['ext']
                print(f"Using default format: {selected_format}")
            else:
                # Ensure selected_format is treated as string
                selected_format = selected_format
            break

        # Print options
        print("\nOptions for downloading subtitles:")
        for key, value in options.items():
            print(f"{key}: {value}")
        return selected_language, selected_format  
    except Exception as e:
        print(f"An error occurred: {e}")

        




def download_subtitles(video_url, selected_language, selected_format):
    output_directory = "subtitles"
    os.makedirs(output_directory, exist_ok=True)

    # yt-dlp options
    options = {
        'writesubtitles': True,  # Enable subtitle download
        'skip_download': True,  # Skip downloading the video
        'subtitleslangs': [selected_language],   # Language selection
        'subtitlesformat': selected_format,  # Subtitle format selection
        'outtmpl': os.path.join(output_directory, '%(title)s.%(ext)s')  # Output template for file naming
    }

    try:
        # Create a yt-dlp object
        ydl = yt_dlp.YoutubeDL(options)

        # Download subtitles
        ydl.download([video_url])

        print("Subtitles downloaded successfully!")

    except Exception as e:
        print(f"An error occurred: {e}")

     

if __name__ == "__main__":
    video_url = input("Enter the URL of the YouTube video: ").strip()
    selected_language=''
    selected_format=''
    selected_language, selected_format = print_available_subtitles(video_url)

    # selected_language = input("Enter the language code of the subtitles you want to download : ")
    # selected_format = input("Enter the format of the subtitles you want to download  : ")
    download_subtitles(video_url,selected_language ,selected_format )
