from django import forms

class InputForm(forms.Form):
 
    hour = forms.IntegerField(help_text="Enter hour in 24 hour format",label="Hour",min_value=0,max_value=23)
    minutes = forms.IntegerField(help_text="Enter minutes",label="Minutes",min_value=0,max_value=59)
    seconds = forms.IntegerField(help_text="Enter seconds",label="Seconds",min_value=0,max_value=59)

    