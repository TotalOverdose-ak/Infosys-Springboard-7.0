import time
from youtube_scraper import get_marathi_corner_videos, get_all_states_videos
from ai_parser import parse_scheme_with_ai
from db_loader import upload_to_mongodb

def process_videos(videos):
    print(f"\n🚀 Found {len(videos)} videos to process.")
    for video in videos:
        print("\n---------------------------------------------------")
        print(f"📹 Processing Video: {video['title']}")
        
        # Combine title and description for AI context
        context = f"Title: {video['title']}\nDescription: {video['description']}"
        
        # Step 2: Use AI to extract clean JSON
        parsed_data = parse_scheme_with_ai(context)
        
        # Step 3: Upload to MongoDB
        if parsed_data:
            upload_to_mongodb(parsed_data)
        
        # Sleep to avoid hitting Groq API rate limits
        time.sleep(2)

def main():
    print("==========================================================")
    print("🤖 STARTING MULTI-SOURCE AI DATA PIPELINE")
    print("==========================================================")
    
    # 1. Fetch MarathiCorner Specific Videos
    print("\n[PHASE 1] Fetching MarathiCorner YouTube Channel...")
    marathi_videos = get_marathi_corner_videos()
    process_videos(marathi_videos)
    
    # 2. Fetch Other States Automatically
    print("\n[PHASE 2] Fetching General State Schemes Automatically...")
    state_videos = get_all_states_videos()
    process_videos(state_videos)
    
    print("\n==========================================================")
    print("✅ DATA PIPELINE EXECUTION COMPLETED")
    print("==========================================================")

if __name__ == "__main__":
    main()
