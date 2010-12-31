from django.contrib.auth.models import User
from django.db import models
from imagekit import models as ik_models

class Image(ik_models.ImageModel):
	caption = models.TextField(default = '')
	client = models.TextField(default = '') # will be a many-to-many to Client model
	display = models.BooleanField(default = True)
	original_image = models.ImageField(upload_to = 'uploads')
	upload_batch = models.ForeignKey('UploadBatch', null = True)
	edit_time = models.DateTimeField(auto_now = True)
	
	class IKOptions:
		spec_module = 'core.ikspecs'
		cache_dir = 'ikcache'
		image_field = 'original_image'

class UploadBatch(models.Model):
	creation_time = models.DateTimeField(auto_now_add = True)
	saved = models.BooleanField(default = False)
	user = models.ForeignKey(User)
