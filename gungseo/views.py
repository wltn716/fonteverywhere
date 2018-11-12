from django.shortcuts import render
from .forms import UploadFileForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from .fontRealTest import getFontInfo
import cv2


from .img_preprocessing import getTextImages
import cv2

def index(request):
	return render(request, 'gungseo/index.html', {})

def post_image(request):
	form = UploadFileForm()
	return render(request, 'gungseo/post_image.html', {'form': form})

def result(request):
	if request.method == 'POST':
		form = UploadFileForm(request.POST, request.FILES)
		if form.is_valid():
			x1 = int(request.POST['x1'])
			y1 = int(request.POST['y1'])
			x2 = int(request.POST['x2'])
			y2 = int(request.POST['y2'])

			file = request.FILES['file']

			fs = FileSystemStorage()
			filename = fs.save(file.name, file)
			uploaded_file_url = fs.url(filename)

			cropped_img = cv2.imread(uploaded_file_url[1:])
			cropped_img = cropped_img[y1:y2, x1:x2]
			cv2.imwrite(uploaded_file_url[1:],cropped_img)
			
			gfi = getFontInfo(cropped_img)
			analysis_result, class_indices = gfi.decision()

			return render(request, 'gungseo/result.html', {'uploaded_file_url':uploaded_file_url, 'analysis_result':analysis_result, 'class_indices':class_indices})
	
	else:
		return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
