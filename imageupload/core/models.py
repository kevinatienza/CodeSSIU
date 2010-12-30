from django.db import models
from imagekit import models as ik_models

class Image(ik_models.ImageModel):
	caption = models.TextField(default = '')
	client = models.TextField(default = '') # will be a many-to-many to Client model
	display = models.BooleanField(default = True)
	original_image = models.ImageField(upload_to = 'uploads')
	creation_time = models.DateTimeField(auto_now_add = True)
	edit_time = models.DateTimeField(auto_now = True)
	
	class IKOptions:
		spec_module = 'core.ikspecs'
		cache_dir = 'ikcache'
		image_field = 'original_image'
