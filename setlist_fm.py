import toml

from pathlib import Path

import requests


def load_config():
	return toml.load(Path('test_config.toml'))



class SetlistClient():
	def __init__(self):
		self.config = load_config()
		self.setlist_dict = {}


	def get_setlist(self, setlist_id):

		setlist_config = self.config['setlist']

		url = f'https://api.setlist.fm/rest/1.0/setlist/{setlist_id}'
		#url = 'https://api.setlist.fm/rest/1.0/artist/b10bbbfc-cf9e-42e0-be17-e2c3e1d2600d/setlists?p=1'
		#url = 'https://api.setlist.fm/rest/1.0/artist/32301b5a-a2eb-4575-a070-cc661feb003c'
		headers = {'Accept': 'application/json', 'x-api-key': setlist_config['api_key']}

		result = requests.get(url, headers=headers)

		result = result.json()

		# print(result)
		# print('\n\n')

		self.setlist_dict['artist_name']=result['artist']['name']
		self.setlist_dict['artist_mbid']=result['artist']['mbid']
		self.setlist_dict['venue']=result['venue']['name']
		self.setlist_dict['venue_location']=result['venue']['city']['name'] + ', ' + result['venue']['city']['country']['name']
		try:
			self.setlist_dict['tour_name']=result['tour']['name']
		except KeyError:#'tour' key doesn't exist for setlists with an unknown tour name, so use venue name instead
			self.setlist_dict['tour_name']=result['venue']['name']
		self.setlist_dict['event_date']=result['eventDate']

		tracks = []
		for sets in result['sets']['set']:#get track info dict for each song in the setlist
			for song in sets['song']:
				#before adding track info dict, check if the song is a cover by indexing its 'cover' key.
				#If this key exists then the song is a cover. 
				try:
					song['cover']
					tracks.append(song)
				#if the key does not exist then an error will be thrown. Create a 'cover' key with value 'False'.
				#This is to keep each track info dict consistent and will be helpful later on when indexing them.
				except KeyError:
					song['cover']=False
					tracks.append(song)



		self.setlist_dict['tracks']=tracks

		print(self.setlist_dict)



		# for sets in result['sets']['set']:
		# 	print(sets)
		# 	print('\n')


 
