from google_auth_oauthlib.flow import InstalledAppFlow

# Path to the client_secret.json file you downloaded
CLIENT_SECRET_FILE = './client_secret.json'

# Scopes required for sending emails
SCOPES = ["https://www.googleapis.com/auth/gmail.send"]

def get_refresh_token():
    # Run the OAuth flow
    flow = InstalledAppFlow.from_client_secrets_file(CLIENT_SECRET_FILE, SCOPES)
    creds = flow.run_local_server(port=0)

    # Print the refresh token
    print("Refresh Token:", creds.refresh_token)

if __name__ == "__main__":
    get_refresh_token()