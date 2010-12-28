from django.conf.urls.defaults import *
import settings

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Example:
    # (r'^imageupload/', include('imageupload.foo.urls')),

    # Uncomment the admin/doc line below to enable admin documentation:
    # (r'^admin/doc/', include('django.contrib.admindocs.urls')),

    (r'^admin/', include(admin.site.urls)),
    (r'^', include('imageupload.core.urls')),
)

urlpatterns += patterns('',
	(r'(?:.*/)?(?P<path>(ikcache)/.+)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
	(r'(?:.*?/)?(?P<path>(ikcache|css|img|js|uploads)/.+)$', 'django.views.static.serve', {'document_root': settings.MEDIA_ROOT }),
)
