import requests
import base64

one_hour_code = ""
client_id = ""
client_secret = ""
refresh_token = ""

encoded_credentials = base64.b64encode(client_id.encode() + b':' + client_secret.encode()).decode("utf-8")

token_headers = {
    "Authorization": "Basic " + encoded_credentials,
    "Content-Type": "application/x-www-form-urlencoded"
}
token_data = {
    "grant_type": "refresh_token",
    "refresh_token": refresh_token,
    "redirect_uri" : "http://localhost:7777"
}
