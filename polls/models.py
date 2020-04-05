import datetime

from django.db import models
from django.utils import timezone

# 3 steps for making model changes:
# 1) Change the models (in this file)
# 2) Run python manage.py makemigrations to create migrations for those changes
# 3) Run python manage.py migrate to apply those changes to the database

# Quick lookup for primary key
# Question.objects.get(pk=1)


class Question(models.Model):
	question_text = models.CharField(max_length=200)
	pub_date = models.DateTimeField('date published')  # optional human readable name passed

	# Magic method. it isn't needed but is useful. It will print this information instead of just [object at 0x00020sdfj]
	def __str__(self):
		return self.question_text

	def was_published_recently(self):
		return self.pub_date >= timezone.now() - datetime.timedelta(days=1)


class Choice(models.Model):
	question = models.ForeignKey(Question, on_delete=models.CASCADE)
	choice_text = models.CharField(max_length=200)
	votes = models.IntegerField(default=0)

	def __str__(self):
		return self.choice_text
