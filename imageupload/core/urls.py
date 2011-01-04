from django.conf.urls.defaults import *

urlpatterns = patterns('imageupload.core.views',
	(r'^list$', 'list'),
	(r'^upload$', 'upload'),
	url(r'^edit/(\d+)', 'edit', name="edit"),
	(r'^start_upload_batch$', 'start_upload_batch'),
	url(r'^save_upload/(\d+)$', 'save_upload', name = 'save_upload'),
	url(r'^cancel_upload/(\d+)$', 'cancel_upload', name = 'cancel_upload'),
)
