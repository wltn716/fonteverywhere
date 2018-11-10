from django import forms

class UploadFileForm(forms.Form):
	file = forms.FileField(
		label="", 
		help_text="",
		widget=forms.FileInput(attrs={'class': "input_img"}))

	x = forms.IntegerField(widget=forms.HiddenInput())
	y = forms.IntegerField(widget=forms.HiddenInput())
	w = forms.IntegerField(widget=forms.HiddenInput())
	h = forms.IntegerField(widget=forms.HiddenInput())