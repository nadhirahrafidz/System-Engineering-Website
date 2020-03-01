from django.conf.urls import url
from . import views
urlpatterns = [
    url(r'^$', views.get_countries, name='countries'),
    url(r'^(\d+)/', views.get_regions, name='regions'),
    url(r'^(\d+)/(\d+)', views.get_clusters, name='clusters'),
]