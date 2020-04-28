# Helper methods for templates. Any manipulation needed in a template, put that function here
from django import template

register = template.Library()


# Turn a insert commas into the thousands place of numbers (100000 -> 1,000,000
def to_thousands(value):
	return '{:,}'.format(value)


register.filter('to_thousands', to_thousands)

