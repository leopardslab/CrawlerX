from django.conf import settings
from django.conf.urls import url, static
from main.services import project, crawl_job, scrapy, elasticsearch
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    url(r'^api/project/create', project.project_create, name='create_project'),
    url(r'^api/project/jobs', scrapy.get_jobs_by_project, name='get_jobs_by_project'),
    url(r'^api/projects', project.get_projects, name='get_project'),
    url(r'^api/jobs', scrapy.get_jobs, name='get_jobs'),
    url(r'^api/job', crawl_job.get_job_data, name='get_job'),

    url(r'^api/job/crawldata', crawl_job.get_crawl_data, name='get_job_data'),
    url(r'^api/crawl/disable_job', crawl_job.disable_schedule_job, name='disabled_crawl_job'),
    url(r'^api/crawl/delete_job', crawl_job.delete_schedule_job, name='delete_crawl_job'),
    url(r'^api/crawl/execute_job', crawl_job.crawl_new_job, name='run_crawl_job'),

    url(r'^api/elasticdata', elasticsearch.get_elasticsearch_data, name='get_elastic_data'),
]

if settings.DEBUG:
    urlpatterns += static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
