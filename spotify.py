# Get the user's input as the artist's name.
# Return the artist's albums.

import sys
import urllib2
import json
import pprint

reload(sys)
sys.setdefaultencoding('utf-8')

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
					apiCall = urllib2.urlopen("https://api.spotify.com/v1/artists/" + artistID + "/albums?market=US&album_type=album&limit=50")
					apiRead = apiCall.read()
					artistAlbumData = json.loads(apiRead)
					apiCall.close()

					artistAlbums = []
					albumSelectCounter = 1
					albumNumber = 0 
					previousAlbum = ""

					for x in artistAlbumData["items"]:
						if x["name"] != previousAlbum:
							albumNumber += 1
							artistAlbums.append([{"ourID": albumSelectCounter}, {"name": x["name"]}, {"spotifyID": x["id"]}])
							previousAlbum = x["name"]
							albumSelectCounter += 1

					print("This artist has %s albums available on Spotify for the U.S. market. \n" %albumNumber)

					if albumNumber >= 1: 
						for albums in artistAlbums:
							print str(albums[0]["ourID"]) + ". " + str(albums[1]["name"])

						while True: 
							try: 
								albumSection = input("Enter the number that corresponds with the album track list you'd like to view: ")
								for albums in artistAlbums:
									if albumSection == albums[0]["ourID"]:
										spotifyID = albums[2]["spotifyID"]
										chosenAlbum = albums[1]["name"]
										apiCall = urllib2.urlopen("https://api.spotify.com/v1/albums/" + spotifyID + "/tracks")
										apiRead = apiCall.read()
										albumTrackData = json.loads(apiRead)
										apiCall.close()

										print("%s Track List" %chosenAlbum)

										for track in albumTrackData["items"]:
											print str(track["track_number"]) + ". " + str(track["name"])
								break
									
							except (TypeError, NameError):
								print "Invalid entry."

					break
				except IndexError:
					print ("This artist does not have a catalog of albums on Spotify.")

			break
		except IndexError:
			print ("This artist cannot be found.")
			break

	Continue = raw_input("Would you like to see another artist's albums? ").lower()

print "Thanks for utilizing our app! Goodbye!"



