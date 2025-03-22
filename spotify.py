import toml

from pathlib import Path
 
import requests

import spotipy
from spotipy.oauth2 import SpotifyPKCE


def load_config():
    return toml.load(Path('config.toml'))



class SpotifyClient():
    def __init__(self):
        self.config = load_config()
        self.client = self.create_client()



    def create_client(self):
        config = self.config['spotify']

        auth_manager = SpotifyPKCE(
        client_id=config['client_id'],
        redirect_uri=config['redirect_uri'],
        scope=config['scope']
        )
        return spotipy.Spotify(auth_manager=auth_manager)



    def find(self,query):
        result = self.client.search(query,type='track',limit=10,market='from_token')

        return result



    def get_user_id(self):
        result = self.client.me()

        user_id = result['id']

        return user_id



    def create_playlist(self,setlist_dict,tracks):
        #define paramater variables. Current user's user ID, the list of track IDs, playlist description and name
        result = self.client.me()
        user_id = result['id']

        track_ids = []
        for track in tracks:
            if track['id']:
                track_ids.append(track['id'])

        playlist_name = setlist_dict['artist_name'] + ' - ' + setlist_dict['tour_name']
        playlist_description = f"Setlist performed by {setlist_dict['artist_name']} for this tour. Venue: {setlist_dict['venue']}, Location: {setlist_dict['venue_location']}, date: {setlist_dict['event_date']}"

        #create the playlist, add playlist name and description
        result = self.client.user_playlist_create(user=user_id,name=playlist_name,
         public=True, collaborative=False, description=playlist_description)

        #get the newly created playlist's ID
        playlist_id = result['id']

        #add tracks to the playlist
        result = self.client.user_playlist_add_tracks(user=user_id,playlist_id=playlist_id,
         tracks=track_ids,position=None)

        print("Playlist Created")



    def convert_setlist_to_spotify_data(self,setlist_dict):
        tracks = []

        converting = True

        while converting:

            n = 1

            for track in setlist_dict['tracks']:
                print(f'converting track {n}')
                n+=1

                #The original artist if the track is a cover, else the artist of the setlist
                #I use replace function on any artist or track name to get rid of any apostrophes.
                #Spotify search doesn't seem to like apostrophes in the query string
                artist_name = track['cover']['name'].replace("'"," ") if track['cover'] else setlist_dict['artist_name'].replace("'"," ")

                print(f"artist_name = {artist_name}")
           
                track_name = track['name'].replace("'"," ")
                
                print(f"track_name = {track_name}")


                #THIS NEEDS REVIEWING. SEE RESULTS FOR "Another Brick in the Wall, Part 3". 
                #IT RETURNS 'Another Brick In The Wall, Pt. 2 - 2011 Remastered Version'
                result = self.find(f"artist:{artist_name} track:{track_name}")
 
                if result['tracks']['total']==0:#means the self.find function did not return a result based on the artist and track value
                    result = self.find(f"{track_name}")#search again with just the track name
                    if result['tracks']['total']==0:#means the self.find function did not return any results 
                        tracks.append({'name': None, 'id': None})
                    else:#self.find function did return a result based on just the track name and now we need to filter the results
                        matching_artist_tracks = []#If any of the results match the artist name, add it to a list of matching results
                        for track in result['tracks']['items']:
                            if track['album']['artists'][0]['name'].replace("'"," ")==artist_name:
                                matching_artist_tracks.append(track)
                        
                        try:#then use the first matching result (as it's likely the most popular, if multiple matching results exist)
                            tracks.append({'name': matching_artist_tracks[0]['name'], 'id': matching_artist_tracks[0]['id']})
                        except IndexError:#or there were not matching results and therefore no results
                            tracks.append({'name': None, 'id': None})


                else:#means the self.find function did return a result based on the artist and track value
                    tracks.append({'name': result['tracks']['items'][0]['name'], 'id': result['tracks']['items'][0]['id']})


                
            converting = False

        print("Conversion Complete")

        return tracks
