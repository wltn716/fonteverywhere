from django.shortcuts import render
 
from .forms import UploadFileForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage

from django.http import HttpResponseRedirect

from .fontRealTest import getFontInfo

def index(request):
	return render(request, 'gungseo/index.html', {})

def post_image(request):
	form = UploadFileForm()
	return render(request, 'gungseo/post_image.html', {'form': form})

def result(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			file = request.FILES['file']
			fs = FileSystemStorage()
			filename = fs.save(file.name, file)
			uploaded_file_url = fs.url(filename)
			
			gfi = getFontInfo(uploaded_file_url)
			analysis_result = gfi.decision()

			return render(request, 'gungseo/result.html', {'uploaded_file_url':uploaded_file_url, 'analysis_result':analysis_result})
	
	else:
		return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
