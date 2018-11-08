from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^post_image$', views.post_image, name='post_image'),
    url(r'^result$', views.result, name='result'),
]