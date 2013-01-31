import plistlib
from collections import defaultdict
import pickle
import os
import requests

'''
Create the artist-albums database. If already exists load data file
'''
def parse():
	artist_to_albums = defaultdict(set)

	if os.path.isfile("index.p"):
		artist_to_albums = pickle.load( open( "index.p", "rb"))
	else:
		#read the file into memory
		plist = plistlib.readPlist('lib.xml')
		for meta in plist:
			if meta == u'Tracks':
				for key in plist[meta]:
					#dict for each song
					cur_song = plist[meta][key]
					if u'Album' in cur_song.keys() and u'Artist' in cur_song.keys():
						artist_to_albums[cur_song[u'Artist']].add(cur_song[u'Album'])
		pickle.dump(artist_to_albums, open("index.p", "wb"))

	"""
	# Sanity testing code

	if os.path.isfile("ArtistList.")
	for artist in artist_to_albums.keys():
		if artist == u'The Black Keys' or artist == u'The Kooks' or artist == u'Frank Ocean':
			for album in artist_to_albums[artist]:
				print artist, album
	"""

	'''
	Open the list of artists to look for. 
	Future: if no list, ask for user input to create the list
	'''
	if os.path.isfile("ArtistList.in"):
		f = open("ArtistList.in", "r")
		ch_artists = [raw.strip() for raw in f.readlines()]

	res_values = []
	for ch_artist in ch_artists:
		exist_albums = []
		if ch_artist in artist_to_albums.keys():
			exist_albums = artist_to_albums['ch_artist']

		#find the artist id to get more accurate results
		payload = {'term':ch_artist, 'attribute':"artistTerm", 'entity':"song"}
		r = requests.get("https://itunes.apple.com/search", params = payload)
		res = r.json()
		if res['resultCount'] > 0:
			ch_artist_id = res['results'][0]['artistId']

		#TODO: write a method to store the artist id's in a cache

		#get the albums that this artist has released
			#TODO: put the number of results in the config file
		payload = {'id':ch_artist_id,'entity':'album', 'sort':'recent', 'limit':'10'}
		r = requests.get("https://itunes.apple.com/lookup", params = payload)
		res = r.json()

		new_albums = []
		for album in res[u'results']:
			if album['wrapperType'] == u'artist':
				if not album['artistName'] == ch_artist:
					print "The returned artist is not what we're looking for"
			else:
				if not album['collectionName'] in artist_to_albums[ch_artist]:
					values = [ch_artist, album['collectionName'], album['releaseDate'][0:10]]
					res_values.append(values)
					#TODO : Prettify the output
#					print
#				 	for word in values:
#				 		print word+'\t',
	return res_values









