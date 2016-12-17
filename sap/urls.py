"""sap URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/1.10/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  url(r'^$', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  url(r'^$', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.conf.urls import url, include
    2. Add a URL to urlpatterns:  url(r'^blog/', include('blog.urls'))
"""
from ckeditor_uploader import views
from django.conf.urls import url, include
from django.contrib import admin
# import for the static file upload
from django.conf import settings
from django.conf.urls.static import static

from django.views.decorators.cache import never_cache

urlpatterns = [
  url(r'^admin/', admin.site.urls),
  #allow ckeditor to upload specific url
  url(r'^ckeditor/', include('ckeditor_uploader.urls')),
  # allow all the user to upload and browse their images in server
  url(r'^upload/', (views.upload), name='ckeditor_upload'),
  url(r'^browse/', never_cache((views.browse)), name='ckeditor_browse'),
  url(r'^', include('forum.urls')),
]

if settings.DEBUG:
  urlpatterns +=  static(
    settings.STATIC_URL,
    document_root=settings.STATIC_ROOT
  ) + static(settings.MEDIA_URL,
             document_root=settings.MEDIA_ROOT)
