from django.db import models
from django.contrib.auth.models import AbstractUser
from django import forms
from django.forms import PasswordInput


class User(models.Model):
	user_id = models.AutoField(primary_key=True)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	username = models.CharField(max_length=100)
	password = models.CharField(max_length=100)
	num_artists = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		print(f'id: {User.user_id}\n name: {User.first_name} {User.last_name}\n created at: {User.created_at}\n')


class Artist(models.Model):
	users = models.ManyToManyField(User)
	artist_id = models.AutoField(primary_key=True)
	genre = models.CharField(max_length=50)
	num_fans = models.IntegerField()
	# bio_link = models.CharField(max_)
	artist_name = models.CharField(max_length=200)

	def __str__(self):
		print(f'id: {Artist.artist_id}\ngenre: {Artist.genre}\nnum fans: {Artist.num_fans} artist_name: {Artist.artist_name}')


class Location(models.Model):
	location_id = models.AutoField(primary_key=True)
	user_id = models.ForeignKey(User, on_delete=models.CASCADE)

	def __str__(self):
		print(f'id: {Location.location_id}\ncity {Location.city}\n')


class Event(models.Model):
	event_id = models.AutoField(primary_key=True)
	date = models.DateTimeField()
	event_name = models.CharField(max_length=200)
	ticket_price = models.IntegerField()
	artist_id = models.ForeignKey(Artist, on_delete=models.CASCADE)
	location_id = models.ForeignKey(Location, on_delete=models.CASCADE)
