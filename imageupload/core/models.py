from django.db import models
from imagekit import models as ik_models

class Image(ik_models.ImageModel):
	original_image = models.ImageField(upload_to = 'uploads')
	
	class IKOptions:
		spec_module = 'core.ikspecs'
		cache_dir = 'ikcache'
		image_field = 'original_image'
