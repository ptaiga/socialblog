from django.conf.urls import url

from . import views

app_name = 'main'
urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^(?P<post_id>[0-9]+)/$', views.post, name='post'),
    url(r'^post/new/$', views.new_post, name='new_post'),
    url(r'^post/add/$', views.add_post, name='add_post'),
    url(r'^subscriptions/$', views.subscriptions, name='subscriptions'),
    url(r'^subscribe/$', views.subscribe, name='subscribe'),

    url(r'^users/$', views.users, name='users'),
    url(r'^send_mail/$', views.send_mail, name='send_mail'),
]