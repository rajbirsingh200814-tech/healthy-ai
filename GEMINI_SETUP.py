"""
QUICK START GUIDE - Google Gemini FREE API

1. Get Your Free API Key:
   - Go to: https://makersuite.google.com/app/apikey
   - Click "Get API key"
   - Click "Create API key in new project"
   - Copy your API key

2. Add to .env file:
   - Edit .env in the project root
   - Replace "your_gemini_api_key_here" with your actual key
   - Save the file

3. Test the CLI:
   python main.py recommend --dietary-needs vegetarian --calories 2000

4. Free Tier Limits:
   - 60 API calls per minute
   - Perfect for testing and CV projects
   - No payment method required

5. Done! Your project is now using free AI!
"""

if __name__ == "__main__":
    import sys
    import os
    from pathlib import Path
    
    print(__doc__)
    
    # Check if API key is set
    env_path = Path(__file__).parent / ".env"
    if env_path.exists():
        with open(env_path) as f:
            content = f.read()
            if "your_gemini_api_key_here" in content:
                print("\n[!] NEXT STEP: Update your .env file with your Gemini API key")
            elif "GEMINI_API_KEY=" in content:
                print("\n[OK] API key appears to be configured in .env")
    else:
        print("\n[!] .env file not found. Create it from .env.example")
