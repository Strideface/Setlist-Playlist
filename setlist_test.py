#this file will become '__main__'

from setlist_fm import SetlistClient
from spotify import SpotifyClient


 

#setlist.fm api part

setlist_client = SetlistClient()

response = input("Copy and paste the setlist ID here:    ")
setlist_client.get_setlist(response)

# print('\n\n')
# print(setlist_client.setlist_dict)
# print('\n\n')







#spotify api part

spotify_client = SpotifyClient()

tracks = spotify_client.convert_setlist_to_spotify_data(setlist_client.setlist_dict)

print('\n\n')
for track in tracks:
	print(track)

print('\n\n')

spotify_client.create_playlist(setlist_client.setlist_dict,tracks)



# for track in result['tracks']['items']:
# 	print(f"track: {track}\n")

# result = spotify_client.find("Another Brick in the Wall, Part 3")

# print(result)
# print('\n\n')
# print('\n\n')

# matching_artist_tracks = []
# for track in result['tracks']['items']:
# 	if track['album']['artists'][0]['name']=='Pink Floyd':
# 		matching_artist_tracks.append(track)

# print(matching_artist_tracks)

	









