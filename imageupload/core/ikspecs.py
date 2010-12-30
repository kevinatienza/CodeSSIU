from imagekit.specs import ImageSpec
from imagekit import processors
import Image as PILImage

class ResizeThumb(processors.Resize):
	width = 150
	height = 150
	crop = True

class BAWer(processors.ImageProcessor):
	@classmethod
	def process(cls, img, fmt, obj):
		img = PILImage.blend(img.convert('L').convert(img.mode), img, 0.0)
		return img, fmt

class BlackAndWhite(ImageSpec):
	processors = [BAWer]

class Thumbnail(ImageSpec):
	processors = [ResizeThumb]
