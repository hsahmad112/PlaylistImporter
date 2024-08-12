from SpotSecrets import token_headers, token_data
import requests

class Refresh:


    def refresh(self):
        r = requests.post("https://accounts.spotify.com/api/token", data=token_data, headers=token_headers)
        r_json = r.json()
        return r_json["access_token"]
