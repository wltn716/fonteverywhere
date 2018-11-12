from django import forms

class UploadFileForm(forms.Form):
	file = forms.FileField(
		label="", 
		help_text="",
		widget=forms.FileInput(attrs={'class': "input_img"}))