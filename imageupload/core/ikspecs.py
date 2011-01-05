from imagekit.specs import ImageSpec
from imagekit import processors
from PIL import ImageOps
import Image as PILImage

# Helper functions
def make_linear_ramp(white):
	# putpalette expects [r,g,b,r,g,b,...]
	ramp = []
	r, g, b = white
	for i in range(255):
		ramp.extend((r*i/255, g*i/255, b*i/255))
	return ramp

# Processors

class ResizeThumb(processors.Resize):
	width = 150
	height = 150
	crop = True

class BAWer(processors.ImageProcessor):
	@classmethod
	def process(cls, img, fmt, obj):
		img = PILImage.blend(img.convert('L').convert(img.mode), img, 0.0)
		return img, fmt

class Sepiaer(processors.ImageProcessor):
	@classmethod
	def process(cls, img, fmt, obj):
		sepia = make_linear_ramp((255, 240, 192))
		if img.mode != "L":
			img = img.convert("L")
		img = ImageOps.autocontrast(img)
		img.putpalette(sepia)
		img = img.convert("RGB")
		return img, fmt

# Image Specs

class BlackAndWhite(ImageSpec):
	access_as = 'black_and_white'
	processors = [BAWer]
	
class Sepia(ImageSpec):
	access_as = 'sepia'
	processors = [Sepiaer]

class Thumbnail(ImageSpec):
	processors = [ResizeThumb]
