# -*- coding: utf-8 -*-
# <nbformat>2</nbformat>
# <codecell>

from bs4 import BeautifulSoup
import requests as rq
import csv
import re


# <codecell>
res = rq.get("http://us7.campaign-archive1.com/?u=f9266ff654b2757279615e242&id=523d2251ab&e=73eaaeff42")

# <codecell>
soup = BeautifulSoup(res.text)

# <codecell>
text = soup.get_text()

# <codecell>

rxWeek= re.compile(r"Shows For The Week Ahead", re.I)

# <codecell>

data = rxWeek.split(text)[1]

# <codecell>

data = data.splitlines()

# <codecell>

container = []
for l in data:
    try:
        temp = l.split(' - ')
        theDate = temp[0]
        theArtist = temp[1].split(' @ ')[0]
        theVenue = temp[1].split(' @ ')[1]
        container.append((theDate, theArtist, theVenue))
    except:
        pass
    
# <codecell>

trackContainer = []
for i,a in enumerate(container):
    try:
        tracks = rq.get("http://ws.spotify.com/search/1/track.json",params={"q":a[1]})
        track = tracks.json()['tracks'][0]['href']
        trackContainer.append((i,track))
    except:
        print('error: ')
        print(i,a)
        pass

# <codecell>

results = []
for t in trackContainer:
    try:
        temp = list(container[t[0]])
        temp.append(t[1])
        results.append(temp)
    except:
        pass
    
# <codecell>
with open("music.csv","wb") as outfile:
    wr = csv.writer(outfile)
    for row in results:
        temp = map(lambda x: x.encode('utf8'), row)
        wr.writerow(temp)

uri_list = ""
with open("music.csv","rb") as infile:
    reader = csv.reader(infile)
    for row in reader:
        uri_list += row[3].split(':')[2]+","

# <codecell>
html = """<iframe src="https://embed.spotify.com/?
uri=spotify:trackset:NYC_LIVE:{}" frameborder="0" allowtransparency="true"></iframe>"""

#uri list can't be too long so only taking first 50 songs
uri_list = uri_list.split(',')[:50]
uri_list = ",".join(uri_list)
with open("player.html","wb") as outfile:
    outfile.write(html.format(uri_list))

