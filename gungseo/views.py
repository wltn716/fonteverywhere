from django.shortcuts import render


def index(request):
	return render(request, 'gungseo/index.html', {})

def post_image(request):
	return render(request, 'gungseo/post_image.html', {})

def result(request):
	return render(request, 'gungseo/result.html', {})

