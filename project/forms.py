from django import forms
from localflavor.us.forms import USStateSelect
from localflavor.us.us_states import STATE_CHOICES

states_else = ["AL", "AK", "AZ", "AR", "CA", "CO", "CT", "DC", "DE", "FL", "GA",
               "HI", "ID", "IL", "IN", "IA", "KS", "KY", "LA", "ME", "MD",
               "MA", "MI", "MN", "MS", "MO", "MT", "NE", "NV", "NH", "NJ",
               "NM", "NY", "NC", "ND", "OH", "OK", "OR", "PA", "RI", "SC",
               "SD", "TN", "TX", "UT", "VT", "VA", "WA", "WV", "WI", "WY"]

states = [("AL", "AL"), ("AK", "AK"), ("AZ", "AZ"), ("AR", "AR"), ("CA", "CA"), ("CO", "CO"), ("CT", "CT"),
          ("DC", "DC"),
          ("DE", "DE"), ("FL", "FL"), ("GA", "GA"), ("HI", "HI"), ("ID", "ID"), ("IL", "IL"), ("IN", "IN"),
          ("IA", "IA"),
          ("KS", "KS"), ("KY", "KY"), ("LA", "LA"), ("ME", "ME"), ("MD", "MD"), ("MA", "MA"), ("MI", "MI"),
          ("MN", "MN"),
          ("MS", "MS"), ("MO", "MO"), ("MT", "MT"), ("NE", "NE"), ("NV", "NV"), ("NH", "NH"), ("NJ", "MI"),
          ("NM", "NM"),
          ("NY", "NY"), ("NC", "NC"), ("ND", "ND"), ("OH", "OH"), ("OK", "NV"), ("OR", "OR"), ("PA", "PA"),
          ("RI", "RI"),
          ("SC", "SC"), ("SD", "SD"), ("TN", "TN"), ("TX", "TX"), ("UT", "UT"), ("VT", "VT"), ("VA", "VA"),
          ("WA", "WA"),
          ("WV", "WV"), ("WI", "WI"), ("WY", "WY")]


class NameForm(forms.Form):
	# Setting these names here is equivalent to name in <input>
	firstname = forms.CharField(max_length=50)
	lastname = forms.CharField(max_length=50)
	states = forms.ChoiceField(choices=states)
