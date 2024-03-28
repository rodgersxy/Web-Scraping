import os
import csv
from instagrapi import Client

# Define the path to store Instagram session settings
IG_CREDENTIAL_PATH = "./ig_settings.json"

# Define a class named Bot
class Bot:
    _cl = None  # Class-level variable to hold the instagrapi Client instance

    # Constructor method to initialize the Bot class
    def __init__(self):
        self._cl = Client()  # Create a new instagrapi Client instance
        # Read Instagram credentials from a CSV file named 'acc.csv'
        ig_username, ig_password = self.read_credentials_from_csv('acc.csv')
        # Check if the Instagram session settings file exists
        if os.path.exists(IG_CREDENTIAL_PATH):
            try:
                # Load existing Instagram session settings
                self._cl.load_settings(IG_CREDENTIAL_PATH)
                # Attempt to log in using the loaded session
                self._cl.login(ig_username, ig_password)
                print("Logged in using existing session.")
            except Exception as e:
                # If loading session fails or session is invalid, log in with credentials
                print(f"Failed to use existing session: {e}. Logging in with credentials.")
                self.login_with_credentials(ig_username, ig_password)
        else:
            # If the session settings file doesn't exist, log in with credentials directly
            self.login_with_credentials(ig_username, ig_password)

    # Method to log in with provided credentials and save session settings
    def login_with_credentials(self, username, password):
        self._cl.login(username, password)  # Log in using provided credentials
        self._cl.dump_settings(IG_CREDENTIAL_PATH)  # Save the new session settings
        print("Logged in with credentials and saved new session.")

    # Static method to read Instagram credentials from a CSV file
    @staticmethod
    def read_credentials_from_csv(csv_file):
        with open(csv_file, mode='r') as file:
            csv_reader = csv.reader(file)  # Create a CSV reader object
            next(csv_reader)  # Skip the header row if present
            for row in csv_reader:  # Iterate through each row in the CSV file
                ig_username, ig_password = row  # Assign values from the row to username and password
                return ig_username, ig_password  # Return the username and password
        return None, None  # Return None if no credentials are found in the CSV file

# Main entry point of the script
if __name__ == "__main__":
    bot = Bot()  # Create an instance of the Bot class
