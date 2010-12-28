from imagekit.specs import ImageSpec
from imagekit import processors

class ResizeThumb(processors.Resize):
	width = 150
	height = 150
	crop = True

class Thumbnail(ImageSpec):
	access_as = 'thumbnail_image'
	processors = [ResizeThumb]
