from django.conf import settings
from django.conf.urls import url, static
from main.services import project, crawl_job, scrapy, elasticsearch

urlpatterns = [
    url(r'^api/project/create', project.project_create, name='create_project'),
    url(r'^api/jobs', scrapy.get_jobs, name='get_jobs'),
    url(r'^api/project/jobs', scrapy.get_jobs_by_project, name='get_jobs_by_project'),
    url(r'^api/projects', project.get_projects, name='get_project'),
    url(r'^api/crawl/new', crawl_job.crawl_new_job, name='crawl'),
    url(r'^api/job/crawldata', crawl_job.get_crawl_data, name='get_job'),
    url(r'^api/job', crawl_job.get_job_data, name='get_job'),
    url(r'^api/elasticdata', elasticsearch.get_elasticsearch_data, name='get_elastic_data'),
]

if settings.DEBUG:
    urlpatterns += static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
