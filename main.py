import requests
from urllib.parse import urlencode
import pandas as pd
from refresh import Refresh


class GetSongsForEachPlaylist:
    client_id = ""
    client_secret = ""


    def call_refresh(self):
        print("Refreshing token")
        refresh_Caller = Refresh()
        self.refresh_token = refresh_Caller.refresh()


    def get_playlists(self):  
        self.user_headers = {
            "Authorization": "Bearer " + self.refresh_token,
            "Content-Type": "application/x-www-form-urlencoded"
        }
        
        self.user_params = {
        "limit": 50
        #write backoff-retry strategy
    }
        self.playlist_result = requests.get( "https://api.spotify.com/v1/me/playlists?items", params=self.user_params, headers=self.user_headers).json()
        return self.playlist_result
    

    def get_playlist_id(self):
        #interate over list to get each individual spotify playlist ID and name put into a DF
        temp_list_playlists = []

        for i in range(len(self.playlist_result['items'])):
            #print(s['items'][i]['name'] + ": " + s['items'][i]['id'])
            temp_list_playlists.append({
                'num' : i,
                'name' : self.playlist_result['items'][i]['name'],
                'id' : self.playlist_result['items'][i]['id']
            })

        self.playlist_df_raw = pd.DataFrame(temp_list_playlists)
        return self.playlist_df_raw

    def get_song_info(self):
        #method to filter the df for each individual ID - 
        temp_id = self.playlist_df_raw._get_value(2, 'id')

        #use this to get playlist info
        result = requests.get("https://api.spotify.com/v1/playlists/" + temp_id, params = self.user_params, headers = self.user_headers).json()

        #Sort through output to get the data you need, i.e. Tracks>Items>Track>Name and Tracks>Items>Track>Artist>Name and Tracks>Items>track>Album>ReleaseDate
            #perhaps get more data from data.json later - for now onto google api.

        for i in range(len(result['tracks']['items'])):
            #print(result['tracks']['items'][i]['track']['name'])
            #print(result['tracks']['items'][i]['track']['artists'][0]['name'])
            #print(result['tracks']['items'][i]['track']['album']['release_date'])
            temp_list_searchterms = []
            
            temp_list_searchterms.append({
                'track_name' : result['tracks']['items'][i]['track']['name'],
                'artist_name' : result['tracks']['items'][i]['track']['artists'][0]['name'],
                'release_date' : result['tracks']['items'][i]['track']['album']['release_date']

            })
            self.searchterms_df_raw = pd.DataFrame(temp_list_searchterms)
            print(self.searchterms_df_raw.head())



    #use below to save to .json file
    #with open('data.json', 'w', encoding='utf-8') as f:
    #   json.dump(result, f, ensure_ascii=False, indent=4)


a = GetSongsForEachPlaylist()
a.call_refresh()
a.get_playlists()
a.get_playlist_id()
a.get_song_info()
