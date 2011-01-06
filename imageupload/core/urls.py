from django.conf.urls.defaults import *

urlpatterns = patterns('imageupload.core.views',
	(r'^list$', 'list'),
	(r'^upload$', 'upload'),
	url(r'^edit/(\d+)', 'edit', name="edit"),
	url(r'^get_filters/(\d+)', 'get_filters', name="get_filters"),
	url(r'^remove_filters/', 'remove_filters', name="remove_filters"),
	url(r'^apply_filter/', 'apply_filter', name="apply_filter"),
	(r'^start_upload_batch$', 'start_upload_batch'),
	url(r'^save_upload/(\d+)$', 'save_upload', name = 'save_upload'),
	url(r'^cancel_upload/(\d+)$', 'cancel_upload', name = 'cancel_upload'),
)
