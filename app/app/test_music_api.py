import http.client

conn = http.client.HTTPSConnection("theaudiodb.p.rapidapi.com")

headers = {
    'x-rapidapi-key': "dd8aacaec5mshb9c48291b5a75b6p1bb1b1jsn5a445d106f45",
    'x-rapidapi-host': "theaudiodb.p.rapidapi.com"
    }

artist = "Coldplay".lower()
song = "Yellow".lower()

artist = "The+Beatles".lower()
song = "All+You+Need+Is+Love".lower()

conn.request("GET", "/searchtrack.php?s={}&t={}".format(artist, song), headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))

# strTrackThumb


conn = http.client.HTTPSConnection("coverartarchive.org")

headers = {
    'host': "coverartarchive.org",
    'accept': "application/json"
    }


conn.request("GET", "/release/b10bbbfc-cf9e-42e0-be17-e2c3e1d2600d", headers=headers)

res = conn.getresponse()
data = res.read()

print(data.decode("utf-8"))
