from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms
from django.forms import PasswordInput


class Location(models.Model):
	location_id = models.AutoField(primary_key=True)
	state = models.CharField(max_length=50)
	city = models.CharField(max_length=50)

	def __str__(self):
		return f'id: {self.location_id}\ncity {self.city}\n'


class User(models.Model):
	user_id = models.AutoField(primary_key=True)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	username = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	num_artists = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)
	location = models.ForeignKey(Location, on_delete=models.CASCADE)  # Django auto adds _id to PK's

	def __str__(self):
		return f'id: {self.user_id}\n name: {self.first_name} {self.last_name}\n created at: {self.created_at}\n'


class Artist(models.Model):
	users = models.ManyToManyField(User)
	artist_id = models.AutoField(primary_key=True)
	genre = models.CharField(max_length=50)
	num_fans = models.IntegerField()
	# bio_link = models.CharField(max_)
	artist_name = models.CharField(max_length=200)

	def __str__(self):
		return f'id: {self.artist_id} genre: {self.genre} num fans: {self.num_fans} artist_name: {self.artist_name}'


class Event(models.Model):
	event_id = models.AutoField(primary_key=True)
	date = models.DateTimeField()
	event_name = models.CharField(max_length=200)
	ticket_price = models.IntegerField()
	artist = models.ForeignKey(Artist, on_delete=models.CASCADE)
	location = models.ForeignKey(Location, on_delete=models.CASCADE)

	def __str__(self):
		return f'id: {self.event_id} date: {self.date} name: {self.event_name} artist: {self.artist.artist_name} location: {self.location.city} '
