# Get the user's input as the artist's name.
# Return the artist's albums.

import urllib2
import json

print "Find the albums of the artists you love on Spotify!"

Continue = "y"
while Continue == "yes" or Continue == "y":
	artist = raw_input("Enter the name of an artist: ").title()

	while True: 
		try: 
			apiCall = urllib2.urlopen("https://api.spotify.com/v1/search?q=" + artist.replace(" ", "%20") + "&type=artist")
			apiRead = apiCall.read()
			artistData = json.loads(apiRead)
			apiCall.close()

			artistID = artistData["artists"]["items"][0]["id"]

			while True:
				try:
					apiCall = urllib2.urlopen("https://api.spotify.com/v1/artists/" + artistID + "/albums")
					apiRead = apiCall.read()
					artistAlbumData = json.loads(apiRead)
					apiCall.close()

					artistAlbums = []

					for x in artistAlbumData["items"]:
						if x["name"] not in artistAlbums:
							if "US" in x["available_markets"]:
								artistAlbums.append(x["name"])
								print x["name"]
					break
				except:
					print ("This artist does not have a catalog of albums on Spotify.")
					break
			break
		except IndexError:
			print ("This artist cannot be found.")
			break

	Continue = raw_input("Would you like to see another artist's albums? ").lower()

print "Thanks for utilizing our app! Goodbye!"



