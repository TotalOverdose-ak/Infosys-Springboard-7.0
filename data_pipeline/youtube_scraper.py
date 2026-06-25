import subprocess
import json

def fetch_youtube_data(query, max_results=3):
    print(f"🔍 Searching YouTube for: {query}")
    # Using yt-dlp to search and fetch video metadata
    command = [
        'yt-dlp',
        f'ytsearch{max_results}:{query}',
        '--dump-json',
        '--no-playlist',
        '--quiet'
    ]
    
    try:
        result = subprocess.run(command, capture_output=True, text=True, check=True)
        videos = []
        for line in result.stdout.strip().split('\n'):
            if line:
                data = json.loads(line)
                videos.append({
                    'title': data.get('title', ''),
                    'description': data.get('description', ''),
                    'channel': data.get('uploader', '')
                })
        return videos
    except subprocess.CalledProcessError as e:
        print(f"❌ Error fetching data: {e}")
        return []

def get_marathi_corner_videos():
    # Specific channel search
    return fetch_youtube_data("MarathiCorner new scheme maharashtra", max_results=2)

def get_all_states_videos():
    states = ["Uttar Pradesh", "Madhya Pradesh", "Karnataka", "Telangana", "Rajasthan", "West Bengal"]
    all_videos = []
    for state in states:
        all_videos.extend(fetch_youtube_data(f"new government scheme subsidy {state} 2026", max_results=2))
    return all_videos
