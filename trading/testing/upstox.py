import requests

# Define the Upstox authorization URL
url = 'https://api.upstox.com/v2/login/authorization/token'

# Headers required for the request
headers = {
    'accept': 'application/json',
    'Content-Type': 'application/x-www-form-urlencoded',
}

# Your credentials and authorization code
data = {
    'code': 'YOUR_AUTH_CODE_HERE',  # Replace with your authorization code
    'client_id': 'YOUR_CLIENT_ID_HERE',  # Replace with your client ID
    'client_secret': 'YOUR_CLIENT_SECRET_HERE',  # Replace with your client secret
    'redirect_uri': 'YOUR_REDIRECT_URI_HERE',  # Replace with your redirect URI
    'grant_type': 'authorization_code',
}

# Send the POST request to get the access token
response = requests.post(url, headers=headers, data=data)

# Check if the request was successful
if response.status_code == 200:
    print("Access token obtained successfully!")
    print(response.json())  # This will contain the access token and other details
else:
    print(f"Failed to obtain access token. Status code: {response.status_code}")
    print(response.json())  # Print the error details
