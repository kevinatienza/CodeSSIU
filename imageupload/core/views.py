from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.files import File
from models import Image
from io import BufferedReader, BufferedWriter, BytesIO, FileIO
import settings
import json
import time
import os

def list(request):
	return render_to_response('list.html')

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
			
			img = open(abs_temp_filename, 'wb')
			Image.objects.create(original_image = File(img))
						
			return HttpResponse(json.dumps({'success':'true'}))
		elif 'qqfile' in request.FILES:
			#implement
			pass
	
	return render_to_response('upload.html')
