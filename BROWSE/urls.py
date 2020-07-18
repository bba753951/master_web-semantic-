from django.conf.urls import  url
from django.conf.urls.static import static
from . import views



urlpatterns = [
    url(r'^$', views.browse, name='browse'),
    url(r'^upload_fun', views.uploadfile, name='upload_url'),
    url(r'^downloadList', views.downloadList, name='downloadList_url'),
    url(r'^site_link', views.site_link, name='site_link'),
    url(r'^copy_example', views.copy_example, name='copy_example'),
    url(r'^usage', views.usage, name='usage'),
    url(r'^upload_usage', views.usage_upload, name='upload_usage'),
    url(r'^confirmMail', views.confirmMail, name='confirmMail'),
    url(r'^analyse', views.analyse, name='analyse'),
    url(r'^upload_analyse', views.analyse_upload, name='analyse_upload'),
]
