import shutil
import os
from django.shortcuts import render
from .forms import UploadFileForm
from django.conf import settings
from django.core.files.storage import FileSystemStorage
from django.http import HttpResponseRedirect
from .fontRealTest import getFontInfo
import cv2
from .img_preprocessing import getTextImages


def index(request):
	return render(request, 'gungseo/index.html', {})

def post_image(request):
	try:
		shutil.rmtree('media/')
	except:
		pass
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
			uploaded_file_url = '/media/'+filename
			
			cropped_img = cv2.imread(uploaded_file_url[1:])
			cropped_img = cropped_img[y1:y2, x1:x2]	
			
			cv2.imwrite(uploaded_file_url[1:],cropped_img)
			
			gfi = getFontInfo(cropped_img)

			analysis_result= gfi.decision()

			#결과값 reshape 
			#(ex) from [[0.1, 0.1, 0.1, 0.1, 0.1]] to [[0.1],[0.1],[0.1],[0.1],[0.1]]
			analysis_result = analysis_result.reshape((8))
			#reshape한 결과값 리스트화
			analysis_result = [ round(i * 100, 2) for i in analysis_result.tolist()] 
			font_name = ['궁서체' , '나눔손글씨붓', '맑은고딕', '바탕', '썸타임', '포천오성과한음', '한나는열한살', '훈화양연화']
			#두 개의 리스트 각각 키와 밸류로 딕셔너리 만들기 => 폰트이름 , 확률값 쌍 생성
			font_dict = dict(zip(font_name, analysis_result)) 
			
			#밸류기준 내림차순 정렬
			font_dict = sorted(font_dict.items(), key=lambda kv: kv[1], reverse=True)
			#가능성이 가장 큰 탑 쓰리의 키값(폰트이름) 저장
			top_three =[] 
			for key in font_dict[:3]:
				top_three.append(key)

			#가장확률이 높은 클래스의 인덱스
			# one_hot = analysis_result.argmax(axis=-1)	

			shutil.rmtree('newmedia/new/')

			return render(request, 'gungseo/result.html', {'uploaded_file_url':uploaded_file_url, 'top_three':top_three})
	else:
		return HttpResponseRedirect(request.META.get('HTTP_REFERER','/'))
