import os
import json
from groq import Groq
from dotenv import load_dotenv

load_dotenv()

# We will rely on the API key being in the .env file
client = Groq(api_key=os.environ.get("GROQ_API_KEY", "YOUR_GROQ_API_KEY_HERE"))

def parse_scheme_with_ai(video_text):
    print("🧠 AI is analyzing the video content for scheme details...")
    
    prompt = """
    You are an expert data extraction bot. Your job is to extract Indian Government Scheme (Subsidy/Yojana) details from the following YouTube video title and description.
    
    CRITICAL INSTRUCTIONS FOR MAXIMUM ACCURACY:
    1. Output ONLY a valid JSON object. No markdown, no explanations.
    2. If a specific field is not mentioned, use a logical default (e.g., amount = 0, deadline = null).
    3. The JSON must exactly match this structure:
    {
      "title": "Exact name of the scheme (String)",
      "description": "Short 1-2 sentence summary of what the scheme is (String)",
      "amount": 1500.0, // Extract the exact monetary amount, use 0 if not found (Float)
      "eligibilityCriteria": "Short criteria (String)",
      "state": "Name of the state, e.g. Maharashtra, UP, All States (String)",
      "category": "e.g. Women Empowerment, Agriculture, Education (String)",
      "isActive": true
    }
    
    Video Content to Analyze:
    """ + video_text

    try:
        chat_completion = client.chat.completions.create(
            messages=[
                {
                    "role": "user",
                    "content": prompt,
                }
            ],
            model="mixtral-8x7b-32768",
            response_format={"type": "json_object"}, # This forces 100% strict JSON output!
            temperature=0.1 # Low temperature for high factual accuracy
        )
        
        response_text = chat_completion.choices[0].message.content
        return json.loads(response_text)
    except Exception as e:
        print(f"❌ AI Parsing failed: {e}")
        return None
