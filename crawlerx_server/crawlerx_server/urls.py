from django.conf import settings
from django.conf.urls import url, static
from main import views

urlpatterns = [
    url(r'^api/crawl/', views.crawl, name='crawl'),
]

if settings.DEBUG:
    urlpatterns += static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
