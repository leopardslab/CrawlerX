from django.conf import settings
from django.conf.urls import url, static
from main.services import project, crawl_job

urlpatterns = [
    url(r'^api/project/create', project.project_create, name='create_project'),
    url(r'^api/projects', project.get_projects, name='get_project'),
    url(r'^api/crawl/new', crawl_job.crawl_new_job, name='crawl'),
]

if settings.DEBUG:
    urlpatterns += static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
