from django.shortcuts import render
from .forms import *
from django.http import HttpResponseRedirect
from .models import *
from django.db.models import Count


# TODO Rest of project:
#  -> Clean up HTML / CSS. Make it look nice.
#  -> Finish adding dummy data

def login_signup(request):
	# Upon start, store locations. Don't do this again unless db is dropped
	# If you drop all tables, you need to change constants.STORE_LOCATIONS back to True
	# if constants.STORE_LOCATIONS is True:
	# constants.store_locations()
	# if constants.STORE_ARTISTS is True:
	# constants.store_artists()
	# if constants.STORE_EVENTS is True:
	# constants.store_events()
	q = Location.objects.all().values()
	print(q)
	q = list(Artist.objects.all().values())
	print(q)
	q = list(Event.objects.all().values())
	print(q)
	context = {}
	return render(request, 'project/login_signup.html', context)


# Handle the login page. Creates the form and handles the input.
def login(request):
	if request.method == 'POST':
		# create a form instance and populate it with data from the request
		form = LoginForm(request.POST)
		# check if the request is valid. this just checks if the fields are filled out
		if form.is_valid():
			try:
				user = User.objects.get(username=form.cleaned_data['username'])
			except User.DoesNotExist:
				return HttpResponseRedirect('/login/')
			if user.password == form.cleaned_data['password']:
				username = form.cleaned_data['username']
				return HttpResponseRedirect('/home/' + username + '/')
			else:
				return HttpResponseRedirect('/login/')
	else:
		form = LoginForm()
	return render(request, 'project/login.html', {'form': form})


# Build the signup screen. This will also add the user to the database if they are approved.
def signup(request):
	if request.method == 'POST':
		# create a form instance and populate it with data from the request
		form = UserForm(request.POST)
		# check whether it's valid. this just checks if the fields are filled out
		if form.is_valid():
			try:
				user = User.objects.get(username=form.cleaned_data['username'])
			except User.DoesNotExist:
				new_user = form.save(commit=False)  # save the information from the form
				new_user.password = form.cleaned_data['confirm_password']  # add other non form information to the user
				selected_city = request.POST['selectedCity']
				user_loc = Location.objects.get(city=selected_city)
				# Set the users FOREIGN KEY to the location they selected
				new_user.location = user_loc
				new_user.save()
				return HttpResponseRedirect('/login/')
	else:
		form = UserForm()
	context = {
		'form': form,
		'states': states,
		'cities': cities,
	}
	return render(request, 'project/signup.html', context)


# The home screen. User name will be passed from login and is the currently logged in user.
def home(request, username=None):
	# Get the tuples for the currently logged in user.
	user = User.objects.get(username=username)
	# Default to artists being shown to none
	add_artists = None
	try:
		users_artists = user.artist_set.values('artist_name')
	except User.DoesNotExist:
		users_artists = None
	# Get the events from artists a user is tracking
	events = get_tracked_artists_events(user)

	# This AJAX call is for building the add artist widget
	if request.method == 'POST' and request.is_ajax:
		artist_id = request.POST.get('artist_id', None)
		search_res = request.POST.get('search_bar', None)
		# Add the clicked artist to the user
		if artist_id is not None:
			# TODO example of UPDATE
			artist = Artist.objects.get(artist_id=artist_id)  # get the artists that the user clicked
			artist.users.add(user)  # add (UPDATE) the users artists and artists num fans
			artist.num_fans += 1
			artist.save()
		# Update the clicked page
		if search_res is not None:
			# TODO Group 3 Query [subquery = users_artists, overall query = add_artists
			# SELECT artist_name
			#       FROM Artist
			#       WHERE artist_name LIKE "{search_res} %" AND NOT IN
			#          (SELECT ArtistName
			#           FROM User JOIN Tracks JOIN Artist On User.UserId = Tracks.UserId AND Artist.ArtistId = Tracks.ArtistId)
			#       ORDER BY artist_name
			# Get the users currently tracked artists (This is the subquery)
			users_artists = user.artist_set.values('artist_name')
			# Get the artists not in users_artists
			add_artists = Artist.objects.filter(artist_name__startswith=search_res).exclude(artist_name__in=users_artists).order_by('artist_name')
			print(f'non user artists {add_artists.values("artist_name")}\nuser artists {users_artists}')
	print(f'Username: {username}\nUser State: {user.location.state}\nUser City: {user.location.city}')
	context = {
		'user': user,
		'add_artists': add_artists,
		'users_artists': users_artists.order_by('artist_name'),
		'events': events,
	}
	return render(request, 'project/home.html', context)


def explore(request, username=None):
	user = User.objects.get(username=username)
	a_filter = 'A - Z'  # Default to sorting by A-Z
	artists = Artist.objects.all().order_by("artist_name")  # Order the artists
	view_num = Artist.objects.all().count()  # Default to showing number for A-Z
	# This query uses group by to get the count() for each genre [genre_counts]
	# SELECT count(*)
	#       FROM Artist
	#       GROUP BY Genre
	genre_counts = Artist.objects.all().values('genre').annotate(total=Count('genre'))
	if request.method == 'POST' and request.is_ajax:
		# TODO Group 1 Query [artists]
		# SELECT ArtistName, NumFans
		#       FROM Artist
		#       WHERE Genre = '{Genre}'
		#       ORDER BY ArtistName ASC
		# TODO Group 2 Query [view_num]
		#  -> view_num at this point adds a HAVING to the genre_counts query from above
		# SELECT count(*)
		#       FROM Artist
		#       GROUP BY 'Genre'
		#       HAVING Genre = '{Genre}'
		a_filter = request.POST.get('filter_artists')
		if a_filter == 'A - Z':
			artists = Artist.objects.all().order_by("artist_name")
			view_num = Artist.objects.all().count()
		elif a_filter == 'Popularity':
			artists = Artist.objects.all().order_by("-num_fans")
			view_num = Artist.objects.all().count()
		elif a_filter == 'Genre - Metal':
			artists = Artist.objects.filter(genre="Metal").order_by("artist_name")
			view_num = genre_counts.filter(genre="Metal")
			view_num = view_num[0]['total']
		elif a_filter == 'Genre - Rock':
			artists = Artist.objects.filter(genre="Rock").order_by("artist_name")
			view_num = genre_counts.filter(genre="Rock")
			view_num = view_num[0]['total']
		elif a_filter == 'Genre - Rap':
			artists = Artist.objects.filter(genre="Rap").order_by("artist_name")
			view_num = genre_counts.filter(genre="Rap")
			view_num = view_num[0]['total']
		elif a_filter == 'Genre - Pop':
			artists = Artist.objects.filter(genre="Pop").order_by("artist_name")
			view_num = genre_counts.filter(genre="Pop")
			view_num = view_num[0]['total']
	# TODO Group 1 Query [top_{genre}]:
	# SELECT Artist.ArtistName, Artist.NumFans
	#       FROM Artist
	#       WHERE Genre = 'Metal'
	#       ORDER BY Artist.NumFans DESC
	#       LIMIT 5
	top_metal = Artist.objects.filter(genre="Metal").order_by("-num_fans")[:5:1]
	top_rock = Artist.objects.filter(genre="Rock").order_by("-num_fans")[:5:1]
	top_rap = Artist.objects.filter(genre="Rap").order_by("-num_fans")[:5:1]
	top_pop = Artist.objects.filter(genre="Pop").order_by("-num_fans")[:5:1]
	context = {
		'user': user,
		'artists': artists,
		'filter_val': a_filter,
		'top_metal': top_metal,
		'top_rock': top_rock,
		'top_rap': top_rap,
		'top_pop': top_pop,
		'view_num': view_num,
	}
	return render(request, 'project/explore.html', context)


# Helper function to find the events for the user based on who the user is tracking
# @param user = A User object to get the tracked events for
def get_tracked_artists_events(user):
	# TODO Group 2 Query [subquery = user_artist_ids, overall query = events]
	# SELECT EventName, Ticket Price, Date, ArtistName, City, State
	# FROM User JOIN Tracks JOIN Artist JOIN Event JOIN Location
	#   ON User.UserId = Tracks.UserId
	#   ON Artist.ArtistId = Tracks.ArtistId
	#   ON Event.ArtistId = Artist.ArtistId
	#   ON Event.LocationId = User.LocationId
	#   WHERE Artist.ArtistId IN
	#           (SELECT Artist.ArtistId
	#            FROM User JOIN Tracks JOIN Artist On User.UserId = Tracks.UserId AND Artist.ArtistId = Tracks.ArtistId)
	#   ORDER BY Event.Date ASC

	# get users artists ids (subquery)
	user_artist_ids = user.artist_set.values('artist_id')
	# get all events that are being performed by tracked artists
	events = Event.objects.filter(artist_id__in=user_artist_ids).order_by('date')
	return events


# Helper function to find the events for the user based on what city the user is in
def get_all_events_in_location(user):
	location_id = user.location.location_id
	events = Event.objects.filter(location_id=location_id).order_by('date')
	print(f'events in my location: {events}')
	return events


# Helper function to find all events
def get_all_events():
	events = Event.objects.all().order_by('date')
	print(f'all events {events}')
	return events
