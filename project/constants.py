from .models import *
from datetime import datetime
import os

# Run the store locations UPDATE
STORE_LOCATIONS = False
# Run the artist UPDATE
STORE_ARTISTS = False
# Run the events UPDATE
STORE_EVENTS = False


# Store all information for locations
def store_locations():
	loc = Location(state='Iowa', city='Des Moines')
	loc.save()
	loc = Location(state='Iowa', city='Cedar Rapids')
	loc.save()
	loc = Location(state='Illinois', city='Chicago')
	loc.save()
	loc = Location(state='Illinois', city='Aurora')
	loc.save()
	loc = Location(state='Minnesota', city='Minneapolis')
	loc.save()
	loc = Location(state='Minnesota', city='St. Paul')
	loc.save()
	loc = Location(state='Wisconsin', city='Madison')
	loc.save()
	loc = Location(state='Wisconsin', city='Milwaukee')
	loc.save()


# Store the artists that are in the artists.txt file to the database. This method will not check for duplicates,
# so make sure you drop the database before adding more artists or recalling the method.
def store_artists():
	file = open(os.path.abspath(os.path.dirname(__file__) + '\\artists.txt'))
	while True:
		line = file.readline().strip()
		if not line:
			break
		vals = line.split(',')
		artist = Artist(artist_name=vals[0], genre=vals[1], num_fans=int(vals[2]))
		artist.save()
	file.close()


# [VenueName,TicketPrice,LocationID,ArtistID,Datetime]
def store_events():
	file = open(os.path.abspath(os.path.dirname(__file__) + '\\events.txt'))
	while True:
		line = file.readline().strip()
		if not line:
			break
		vals = line.split(',')
		time = datetime.strptime(vals[4], '%Y-%m-%d %H:%M')
		location = Location.objects.get(location_id=vals[2])
		artist = Artist.objects.get(artist_id=vals[3])
		event = Event(event_name=vals[0], ticket_price=int(vals[1]), location=location, artist=artist, date=time)
		event.save()
	file.close()