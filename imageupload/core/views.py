from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.files import File
from models import Image
from io import BufferedReader, BufferedWriter, BytesIO, FileIO
import Image as PILImage
import settings
import json
import time
import os

def list(request):
	images = Image.objects.all()
	
	return render_to_response('list.html', locals())

def upload(request):
	if request.method == 'POST':
		if 'qqfile' in request.GET: # upload is via XMLHttpRequest
			temp_filename = '%s-%s' % (time.time(), request.GET.get('qqfile'))
			abs_temp_filename = os.path.join('/tmp', temp_filename)
			
			with BufferedReader( BytesIO( request.raw_post_data ) ) as stream:
				with BufferedWriter( FileIO( abs_temp_filename , "wb" ) ) as destination:
					foo = stream.read( 1024 )
					while foo:
						destination.write( foo )
						foo = stream.read( 1024 )
			
			img = open(abs_temp_filename, 'rb+')
			image = Image.objects.create(original_image = File(img))
						
			return HttpResponse(json.dumps({'success':'true', 'thumbnail_url':image.thumbnail.url}))
		elif 'qqfile' in request.FILES:
			Image.objects.create(original_image = request.FILES.get('qqfile'))
			return HttpResponse(json.dumps({'success':'true'}))
	
	return render_to_response('upload.html')

def edit(request, image_id):
	image = Image.objects.get(id = image_id)
	
	if request.method == 'POST':
		rotate_cw = int(request.POST.get('imageRotate'))
		rotate = 360 - rotate_cw
		
		crop_x1 = int(request.POST.get('selectorX'))
		crop_y1 = int(request.POST.get('selectorY'))
		crop_x2 = crop_x1 + int(request.POST.get('selectorW'))
		crop_y2 = crop_y1 + int(request.POST.get('selectorH'))
		
		pil_image = PILImage.open(image.original_image.path)
		pil_image = pil_image.rotate(rotate)
		pil_image = pil_image.crop((crop_x1, crop_y1, crop_x2, crop_y2,))
		pil_image.save(image.original_image.path)
		
		return HttpResponse(json.dumps('ok'))
	
	return render_to_response('edit.html', locals())
