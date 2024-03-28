import os
from instagrapi import Client 
from instagrapi.exceptions import BadCredentials, ClientLoginRequired

# Initialize Client
cl = Client()

# Instagram credentials
username = os.getenv("INSTAGRAM_USERNAME")
password = os.getenv("INSTAGRAM_PASSWORD")

# Attempt to login
try:
    if not username or not password:
        raise ClientLoginRequired("Instagram credentials not provided")
    
    cl.login(username, password)
    print("Login successful")
except ClientLoginRequired:
    # If login fails due to session not loaded or missing credentials, prompt for login credentials
    print("Session not loaded or Instagram credentials not provided.")
    username = input("Enter your Instagram username: ")
    password = input("Enter your Instagram password: ")
    cl.login(username, password)
    print("Login successful")

    # Save session to a file after successful login
    cl.dump_settings("session.json")
except BadCredentials as e:
    print(f"Login failed: {e}")

# Load session from a file after updating credentials
cl.load_settings("session.json")

# You might still need to call login, but it will use the saved session
cl.login(username, password)
