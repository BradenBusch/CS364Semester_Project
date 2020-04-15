from django import forms
from project.models import *

states_else = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
               "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
               "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
               "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
               "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

states = [("Illinois", "Illinois"), ("Iowa", "Iowa"), ("Minnesota", "Minnesota"), ("Wisconsin", "Wisconsin")]

cities = [("Aurora", "Aurora"), ("Chicago", "Chicago"), ("Cedar Rapids", "Cedar Rapids"), ("Des Moines", "Des Moines"),
          ("Madison", "Madison"), ("Minneapolis", "Minneapolis"), ("Milwaukee", "Milwaukee"), ("St. Paul", "St. Paul")]


class LoginForm(forms.ModelForm):

	class Meta:
		model = User
		fields = ['username', 'password']

	def clean(self):
		cleaned_data = super(LoginForm, self).clean()
		username = cleaned_data.get('username')
		password = cleaned_data.get('password')
		if not User.objects.filter(username=username).exists():
			raise forms.ValidationError('That username does not exist!')
		if User.objects.get(username=username).password != password:
			raise forms.ValidationError('Your password is incorrect!')
		return cleaned_data


class UserForm(forms.ModelForm):
	password = forms.CharField(widget=forms.PasswordInput)
	confirm_password = forms.CharField(widget=forms.PasswordInput)

	class Meta:
		model = User
		# could change this to exclude = ['date'] or whatever
		exclude = ['num_artists', 'password']

	def clean(self):
		cleaned_data = super(UserForm, self).clean()
		password = cleaned_data.get('password')
		confirm_password = cleaned_data.get('confirm_password')
		username = cleaned_data.get('username')
		if User.objects.filter(username=username).exists():
			raise forms.ValidationError('That username is already taken')
		if password != confirm_password:
			raise forms.ValidationError('Your passwords do not match.')
		return cleaned_data


class StateForm(forms.ModelForm):
	state = forms.ChoiceField(choices=states)
	city = forms.ChoiceField(choices=cities)

	class Meta:
		model = Location
		exclude = []
