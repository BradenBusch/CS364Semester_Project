# Helper methods for templates. Any manipulation needed in a template, put that def here
from django import template
import locale

register = template.Library()


def to_thousands(value):
	return '{:,}'.format(value)


register.filter('to_thousands', to_thousands)

