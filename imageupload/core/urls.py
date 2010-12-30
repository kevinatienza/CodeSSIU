from django.conf.urls.defaults import *

urlpatterns = patterns('imageupload.core.views',
	(r'^list$', 'list'),
	(r'^upload', 'upload'),
	url(r'^edit/(\d+)', 'edit', name="edit"),
)
