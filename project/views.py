from django.shortcuts import render, get_object_or_404
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login, authenticate
from .forms import *
from django.contrib import messages
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.urls import reverse
from .models import *
from . import constants
import json
from django.core.serializers.json import DjangoJSONEncoder
from django.http import JsonResponse
from django.db.models import Count


# TODO 4/23
#   -> Another query with aggregate / having could be running a query to show how many artists of each genre
#   there are.
#   -> HAVING can be used to see the number of artists in each genre
# SELECT Num, count(*) AS Number
#     FROM Artist
#     GROUP BY Genre
#

def login_signup(request):
	# Upon start, store locations. Don't do this again unless db is dropped
	# If you drop all tables, you need to change constants.STORE_LOCATIONS back to True
	if constants.STORE_LOCATIONS is True:
		constants.store_locations()
	if constants.STORE_ARTISTS is True:
		constants.store_artists()
	if constants.STORE_EVENTS is True:
		constants.store_events()
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
		# check whether it's valid. this just checks if the fields are filled out
		if form.is_valid():
			try:
				user = User.objects.get(username=form.cleaned_data['username'])
			except User.DoesNotExist:
				return HttpResponseRedirect('/login/')
			if user.password == form.cleaned_data['password']:
				username = form.cleaned_data['username']
				return HttpResponseRedirect('/home/' + username + '/')
				# return render(request, 'project/home.html', {'user'})
			else:
				return HttpResponseRedirect('/login/')
				# return render(request, 'project/home.html', {})

	# if a GET (or any other method) we'll create a blank form
	else:
		form = LoginForm()
	return render(request, 'project/login.html', {'form': form})


# Build the signup screen. This will also add the user to the database if they are approved
def signup(request):
	if request.method == 'POST':
		# create a form instance and populate it with data from the request
		form = UserForm(request.POST)
		# check whether it's valid. this just checks if the fields are filled out
		if form.is_valid():
			try:
				user = User.objects.get(username=form.cleaned_data['username'])
			except User.DoesNotExist:
				new_user = form.save(commit=False)
				new_user.password = form.cleaned_data['confirm_password']
				selected_city = request.POST['selectedCity']
				user_loc = Location.objects.get(city=selected_city)
				# Set the users FOREIGN KEY to the location they selected
				new_user.location = user_loc
				new_user.save()
				qs = User.objects.all().values()
				print(qs)
				return HttpResponseRedirect('/login/')
				# return render(request, 'project/home.html', {})

	# if a GET (or any other method) we'll create a blank form
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
	# Default to artists and events being displayed to none
	add_artists = None
	events = get_tracked_artists_events(user)
	try:
		users_artists = user.artist_set.values('artist_name')
	except User.DoesNotExist:
		users_artists = None
	# Default to showing users events
	events = get_tracked_artists_events(user)

	# This AJAX call is for building the add artist widget
	if request.method == 'POST' and request.is_ajax:
		artist_id = request.POST.get('artist_id', None)
		search_res = request.POST.get('search_bar', None)
		# Add the clicked artist to the user
		if artist_id is not None:
			artist = Artist.objects.get(artist_id=artist_id)  # get the artists that the user clicked
			artist.users.add(user)  # add (UPDATE) the users artists and artists num fans
			artist.num_fans += 1
			artist.save()
		# Update the clicked page
		if search_res is not None:
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
	artists = Artist.objects.all().order_by("artist_name")
	view_num = Artist.objects.all().count()  # Default to showing number for A-Z
	genre_counts = Artist.objects.all().values('genre').annotate(total=Count('genre'))  # Query for
	print(f'VIEW NUM {view_num}')
	if request.method == 'POST' and request.is_ajax:
		# All these view_num queries are for Group 2:
		# 	genre_counts = Artist.objects.all().values('genre').annotate(total=Count('genre'))
		#   view_num = genre_counts.filter(genre={genre})
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
	# All these queries are for Group 1:
	# SELECT Artist.ArtistName, Artist.NumFans
	#       FROM Artist
	#       WHERE Genre = 'Metal'
	#       ORDER BY Artist.NumFans DESC
	#       LIMIT 5
	top_metal = Artist.objects.filter(genre="Metal").order_by("-num_fans")[:5:1]
	top_rock = Artist.objects.filter(genre="Rock").order_by("-num_fans")[:5:1]
	top_rap = Artist.objects.filter(genre="Rap").order_by("-num_fans")[:5:1]
	top_pop = Artist.objects.filter(genre="Pop").order_by("-num_fans")[:5:1]
	print(f'top metal {top_metal} view num {view_num}')
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
	# SELECT EventName, Ticket Price, Date, ArtistName, City, State
	# FROM User JOIN Tracks JOIN Artist JOIN Event JOIN Location
	# ON User.UserId = Tracks.UserId
	# ON Artist.ArtistId = Tracks.ArtistId
	# ON Event.ArtistId = Artist.ArtistId
	# ON Event.LocationId = User.LocationId
	# WHERE Artist.ArtistId IN
	#           (SELECT Artist.ArtistId
	#            FROM User JOIN Tracks JOIN Artist On User.UserId = Tracks.UserId AND Artist.ArtistId = Tracks.ArtistId)
	# get users artists ids
	user_artist_ids = user.artist_set.values('artist_id')
	events = Event.objects.filter(artist_id__in=user_artist_ids).order_by('date')  # Get all events from tracked artists
	print(f'events by my artists: {events}')
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
