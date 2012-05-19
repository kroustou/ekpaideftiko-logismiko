from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout

import views

urlpatterns = patterns('',
    #url(r'^$', login_required(views.main), name='first-screen'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout,{'next_page': '/'}, name='logout'),
    url(r'^register/$',views.RegistrationView.as_view(), name='register'),
    url(r'^$',views.main , name='first-page'),
)
