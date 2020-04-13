from django.db import models
from django import forms
from django.forms import PasswordInput


# TODO maybe do some validation with the username?
class User(models.Model):
	id = models.AutoField(primary_key=True)
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	num_events = models.IntegerField(default=0)
	num_artists = models.IntegerField(default=0)
	created_at = models.DateTimeField(auto_now_add=True)

	def __str__(self):
		print(f'id: {id}\n name: {User.first_name}')
