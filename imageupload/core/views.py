from django.contrib.auth.decorators import login_required
from django.core.urlresolvers import reverse
from django.shortcuts import render_to_response
from django.http import HttpResponse
from django.core.files import File
from models import Image, UploadBatch
from io import BufferedReader, BufferedWriter, BytesIO, FileIO
import Image as PILImage
import settings
import json
import time
import os

def get_clients(request):

	if request.method == 'GET':
		if 'term' in request.GET:
			term = request.GET.get('term')

			limit = 5	
			client_list = [
				{'id':'1','name':'aardvark','value':'aardvark'},
				{'id':'2','name':'anteater','value':'anteater'},
				{'id':'3','name':'argali','value':'argali'},
				{'id':'4','name':'badger','value':'badger'},
				{'id':'5','name':'beaver','value':'beaver'},
				{'id':'6','name':'budgerigar','value':'budgerigar'},
				{'id':'7','name':'burro','value':'burro'},
				{'id':'8','name':'cat','value':'cat'},
				{'id':'9','name':'chimpanzee','value':'chimpanzee'},
				{'id':'10','name':'coati','value':'coati'},
				{'id':'11','name':'cow','value':'cow'},
				{'id':'12','name':'deer','value':'deer'},
				{'id':'13','name':'donkey','value':'donkey'},
				{'id':'14','name':'dugong','value':'dugong'},
				{'id':'15','name':'ermine','value':'ermine'},
				{'id':'16','name':'finch','value':'finch'},
				{'id':'17','name':'gazelle','value':'gazelle'},
				{'id':'18','name':'grizzly bear','value':'grizzly bear'},
				{'id':'19','name':'hamster','value':'hamster'},
				{'id':'20','name':'hippopotamus','value':'hippopotamus'},
				{'id':'21','name':'ibex','value':'ibex'},
				{'id':'22','name':'jaguar','value':'jaguar'},
				{'id':'23','name':'kinkajou','value':'kinkajou'},
				{'id':'24','name':'lamb','value':'lamb'},
				{'id':'25','name':'lizard','value':'lizard'},
				{'id':'26','name':'mandrill','value':'mandrill'},
				{'id':'27','name':'mink','value':'mink'},
				{'id':'28','name':'moose','value':'moose'},
				{'id':'29','name':'musk deer','value':'musk deer'},
				{'id':'30','name':'mynah bird','value':'mynah bird'},
				{'id':'31','name':'opossum','value':'opossum'},
				{'id':'32','name':'parrot','value':'parrot'},
				{'id':'33','name':'polar bear','value':'polar bear'},
				{'id':'34','name':'prairie dog','value':'prairie dog'},
				{'id':'35','name':'quagga','value':'quagga'},
				{'id':'36','name':'iguana','value':'iguana'},
				{'id':'37','name':'jerboa','value':'jerboa'},
				{'id':'38','name':'mountain goat','value':'mountain goat'},
				{'id':'39','name':'instart','value':'instart'},
				{'id':'40','name':'start','value':'start'},
				{'id':'41','name':'astar','value':'astar'},
				{'id':'42','name':'starr','value':'starr'},
				{'id':'43','name':'insttar','value':'insttar'},
				{'id':'44','name':'instary','value':'instary'},
				{'id':'45','name':'stara','value':'stara'},
				{'id':'46','name':'starus','value':'starus'}
			]

			

			primary_results = []
			primary_counter = 0
			secondary_results = []
			output_results = []	

			for client in client_list:
				if client['name'].startswith(term):
					primary_results.append(client)
					primary_counter += 1
					if primary_counter >= limit:
						break
				elif term in client['name']:
					secondary_results.append(client)

			output_results = primary_results

			if primary_counter < limit and len(secondary_results)>=limit-primary_counter:
				output_results = primary_results + secondary_results[0:limit-primary_counter]		
			
			return HttpResponse(json.dumps(output_results))
	return HttpResponse("")

@login_required
def list(request):
	images = Image.objects.filter(upload_batch__user = request.user, upload_batch__saved = True).order_by('-upload_batch__creation_time', 'id')
	
	return render_to_response('list.html', locals())

@login_required
def upload(request):
	if request.method == 'POST':
		if 'qqfile' in request.GET: # upload is via XMLHttpRequest
			upload_batch_id = request.GET.get('upload_batch_id')
			temp_filename = '%s-%s' % (time.time(), request.GET.get('qqfile'))
			abs_temp_filename = os.path.join('/tmp', temp_filename)
			
			with BufferedReader( BytesIO( request.raw_post_data ) ) as stream:
				with BufferedWriter( FileIO( abs_temp_filename , "wb" ) ) as destination:
					foo = stream.read( 1024 )
					while foo:
						destination.write( foo )
						foo = stream.read( 1024 )
					destination.flush()
			
			file_size = os.path.getsize(abs_temp_filename)
			if file_size > 5242880L:
				return HttpResponse(json.dumps({'error': 'File size must not exceed 5MB'}))
			
			try:
				pil_image = PILImage.open(abs_temp_filename)
				pil_image.verify()
			except IOError:
				return HttpResponse(json.dumps({'error': 'Image failed to validate'}))
				
			pil_image = PILImage.open(abs_temp_filename)
			pil_image.thumbnail((1200, 1200,), PILImage.ANTIALIAS)
			
			abs_resized_filename = os.path.join('/tmp', '%s-%s' % ('resized', temp_filename))
			pil_image.save(abs_resized_filename)
			
			img = open(abs_resized_filename, 'rb+')
			
			image = Image.objects.create(original_image = File(img), upload_batch = UploadBatch.objects.get(id = upload_batch_id))
			# Create original filter image
			image.original_filter.url

			minHeight = 250
			minWidth = 250
			toSmall = 'false'
			if minHeight > image.original_image.height or minWidth > image.original_image.width:
				toSmall = 'true'
			
			return HttpResponse(json.dumps({'success':'true', 'id':image.id, 'thumbnail_url':image.thumbnail.url, 'toSmall': toSmall,
											'edit_url':reverse('edit', args=[image.id]), 'image_url':image.original_image.url, 
											'get_filters_url':reverse('get_filters', args=[image.id]), 
											'height':image.original_image.height, 'width':image.original_image.width }))
		elif 'qqfile' in request.FILES:
			Image.objects.create(original_image = request.FILES.get('qqfile'))
			return HttpResponse(json.dumps({'success':'true'}))
	
	return render_to_response('upload.html')

@login_required
def get_filters(request, image_id):
	image = Image.objects.get(id = image_id)
	data =	{
				'original_url': image.original_filter.url,
				'black_and_white_url': image.black_and_white.url,
				'sepia_url': image.sepia.url,
				'height':image.original_image.height, 
				'width':image.original_image.width
			}
	return HttpResponse(json.dumps(data))
	
@login_required
def remove_filters(request):
	"""
	Removes all filters for a certain image.  This view is used when
	the edit edit dialog box is closed.
	"""
	image_id = request.POST.get('image_id')
	image = Image.objects.get(id = image_id)
	# Get absolute path of filter images
	black_and_white_url = settings.MEDIA_ROOT + '/' + image.black_and_white.url
	sepia_url = settings.MEDIA_ROOT + '/' + image.sepia.url
	
	# Delete filter images
	os.remove(black_and_white_url)
	os.remove(sepia_url)
	
	return HttpResponse('ok')
	
@login_required
def change_thumbnail(request):
	"""
	Must receive old_src and image_id in request
	"""
	old_src = settings.MEDIA_ROOT + '/' + request.POST.get('old_src')
	image_id = request.POST.get('image_id')
	
	image = Image.objects.get(id=image_id)
	os.remove(old_src)
	
	return HttpResponse(image.thumbnail.url)

@login_required
def apply_filter(request):
	"""
	Must receive image_id and image_filter in request.
	"""
	
	image_id = request.POST.get('image_id')
	image_filter = request.POST.get('image_filter')
	image = Image.objects.get(id=image_id)
	
	filtered_image_url = settings.MEDIA_ROOT + '/' + eval("image." + image_filter + ".url")
	pil_image = PILImage.open(filtered_image_url)
	pil_image.save(image.original_image.path)
	
	return HttpResponse('ok')

@login_required
def edit(request, image_id):
	image = Image.objects.get(id = image_id)
	
	if request.method == 'POST':
		rotate_cw = int(request.POST.get('imageRotate'))
		rotate = 360 - rotate_cw
		
		original_url = settings.MEDIA_ROOT + '/' + image.original_filter.url
		
		crop_x1 = int(request.POST.get('selectorX'))
		crop_y1 = int(request.POST.get('selectorY'))
		crop_x2 = crop_x1 + int(request.POST.get('selectorW'))
		crop_y2 = crop_y1 + int(request.POST.get('selectorH'))
		
		pil_image = PILImage.open(image.original_image.path)
		pil_image = pil_image.rotate(rotate)
		pil_image = pil_image.crop((crop_x1, crop_y1, crop_x2, crop_y2,))
		pil_image.save(image.original_image.path)
		
		# Change original_filter image
		original_filter = PILImage.open(original_url)
		original_filter = original_filter.rotate(rotate)
		original_filter = original_filter.crop((crop_x1, crop_y1, crop_x2, crop_y2,))
		original_filter.save(original_url)
		
		return HttpResponse(json.dumps('ok'))
	
	return render_to_response('edit.html', locals())

@login_required
def start_upload_batch(request):
	upload_batch = UploadBatch.objects.create(user = request.user)
	
	data =	{
				'upload_batch_id': upload_batch.id,
				'upload_save_url': reverse('save_upload', args = [upload_batch.id]),
				'upload_cancel_url': reverse('cancel_upload', args = [upload_batch.id]),
			}
	
	return HttpResponse(json.dumps(data))

@login_required
def save_upload(request, upload_batch_id):
	try:
		upload_batch = UploadBatch.objects.get(id = upload_batch_id, user = request.user)
	except UploadBatch.DoesNotExist:
		return HttpResponse(json.dumps('does not exist'))
	
	for i in range(upload_batch.image_set.count()):
		image_id = request.POST.get('id-%d' % i)
		image = Image.objects.get(id = image_id)
		image.caption = request.POST.get('caption-%d' % i)
		image.client = request.POST.get('client-%d' % i)
		image.display = request.POST.get('display-%d' % i, False) is not False
		image.save()
		
	upload_batch.saved = True
	upload_batch.save()
	
	return HttpResponse(json.dumps('ok'))

@login_required
def cancel_upload(request, upload_batch_id):
	try:
		upload_batch = UploadBatch.objects.get(id = upload_batch_id, user = request.user)
	except UploadBatch.DoesNotExist:
		return HttpResponse(json.dumps('does not exist'))
		
	upload_batch.delete()
	
	return HttpResponse(json.dumps('ok'))
