import requests

# Replace this with your TMDB API key.
API_KEY = "eyJhbGciOiJIUzI1NiJ9.eyJhdWQiOiI3OGJlZDI2ZmZkZTFkNjUyZmY4Mzg1NjY3ZmFkNDNkNSIsIm5iZiI6MTczODY5NDE3Ni4zNDUsInN1YiI6IjY3YTI1ZTIwN2ViYjA2MTRmZjI2YzQ5MCIsInNjb3BlcyI6WyJhcGlfcmVhZCJdLCJ2ZXJzaW9uIjoxfQ.fp7j1XYC78LliyhnWDkAZoH1g8Z5N0CozXTFeuLWIg8"

TMDB_BASE_URL = "https://api.themoviedb.org/3"

def get_request_token(api_key):
    """
    Step 1: Request a new token from TMDB.
    """
    url = f"{TMDB_BASE_URL}/authentication/token/new"
    params = {"api_key": api_key}
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    if data.get("success"):
        token = data.get("request_token")
        print(f"Obtained request token: {token}")
        return token
    else:
        raise Exception("Failed to obtain request token")

def prompt_user_authentication(request_token):
    """
    Step 2: Direct the user to authenticate the request token.
    The user must open the URL in their browser and log in to approve the token.
    """
    auth_url = f"https://www.themoviedb.org/authenticate/{request_token}"
    print("\n=== USER AUTHENTICATION REQUIRED ===")
    print("Please visit the following URL in your browser to authenticate your request token:")
    print(auth_url)
    input("Press Enter after you have authorized the request token...")

def get_session_id(api_key, request_token):
    """
    Step 3: Create a session using the approved request token.
    """
    url = f"{TMDB_BASE_URL}/authentication/session/new"
    params = {"api_key": api_key}
    payload = {"request_token": request_token}
    response = requests.post(url, params=params, json=payload)
    response.raise_for_status()
    data = response.json()
    if data.get("success"):
        session_id = data.get("session_id")
        print(f"Created session with ID: {session_id}")
        return session_id
    else:
        raise Exception("Failed to create session")

def get_account_details(api_key, session_id):
    """
    Step 4: Retrieve account details, which include your account_id.
    """
    url = f"{TMDB_BASE_URL}/account"
    params = {"api_key": api_key, "session_id": session_id}
    response = requests.get(url, params=params)
    response.raise_for_status()
    data = response.json()
    account_id = data.get("id")
    print(f"Retrieved account ID: {account_id}")
    return data  # Returns the full account details as a dictionary

def main():
    try:
        # 1. Get a request token
        request_token = get_request_token(API_KEY)
        
        # 2. Prompt user to authenticate the token
        prompt_user_authentication(request_token)
        
        # 3. Create a session to obtain a session_id
        session_id = get_session_id(API_KEY, request_token)
        
        # 4. Get account details to retrieve the account_id
        account_details = get_account_details(API_KEY, session_id)
        
        print("\n=== FINAL OUTPUT ===")
        print(f"Session ID: {session_id}")
        print(f"Account ID: {account_details.get('id')}")
        print("Full account details:")
        for key, value in account_details.items():
            print(f"  {key}: {value}")
            
    except requests.HTTPError as http_err:
        print(f"An HTTP error occurred: {http_err}")
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    main()

