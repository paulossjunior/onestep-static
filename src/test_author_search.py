import os
import json
import requests
from dotenv import load_dotenv

def test_author_search():
    load_dotenv()
    api_key = os.getenv('SEARCHAPI_KEY')
    
    if not api_key:
        print("Error: SEARCHAPI_KEY not found")
        return

    # Try searching for a known researcher
    name = "Paulo Sérgio Dos Santos Júnior"
    query = f"{name} @ifes.edu.br"
    
    params = {
        'engine': 'google_scholar_profiles',
        'q': query,
        'api_key': api_key
    }
    
    print(f"Searching for: {query}")
    try:
        response = requests.get("https://www.searchapi.io/api/v1/search", params=params)
        response.raise_for_status()
        data = response.json()
        
        print(json.dumps(data, indent=2))
        
        profiles = data.get('profiles', [])
        if profiles:
            print(f"\nFound {len(profiles)} profiles:")
            for p in profiles:
                print(f"Name: {p.get('name')}")
                print(f"ID: {p.get('author_id')}")
                print(f"Affiliation: {p.get('affiliations')}")
        else:
            print("No profiles found.")
            
    except Exception as e:
        print(f"Error: {e}")

if __name__ == "__main__":
    test_author_search()
