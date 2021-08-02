from django.conf import settings
from django.conf.urls import static
from main.services import project, crawl_job, scrapy, elasticsearch
from django.contrib import admin
from django.urls import path

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/project/create', project.project_create, name='create_project'),
    path('api/project/jobs', scrapy.get_jobs_by_project, name='get_jobs_by_project'),
    path('api/projects', project.get_projects, name='get_project'),
    path('api/jobs', scrapy.get_jobs, name='get_jobs'),
    path('api/job', crawl_job.get_job_data, name='get_job'),

    path('api/job/crawl_data', crawl_job.get_crawl_data, name='get_crawl_data'),
    path('api/crawl/disable_job', crawl_job.disable_schedule_job, name='disable_schedule_job'),
    path('api/crawl/delete_job/<job_id>', crawl_job.delete_crawl_job, name='delete_crawl_job'),
    path('api/crawl/delete_task/<task_id>', crawl_job.delete_crawl_task, name='delete_crawl_task'),
    path('api/crawl/execute_job', crawl_job.crawl_new_job, name='run_crawl_job'),

    path('api/elasticdata', elasticsearch.get_elasticsearch_data, name='get_elastic_data'),
]

if settings.DEBUG:
    urlpatterns += static.static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
