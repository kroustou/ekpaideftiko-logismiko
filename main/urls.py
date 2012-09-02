from django.conf.urls import patterns, url
from django.contrib.auth.decorators import login_required
from django.contrib.auth.views import login, logout
from django.contrib.admin.views.decorators import staff_member_required 

import views

urlpatterns = patterns('',
    url(r'^$', login_required(views.main), name='first-screen'),
    url(r'^login/$', login, name='login'),
    url(r'^logout/$', logout,{'next_page': '/'}, name='logout'),
    url(r'^register/$',views.RegistrationView.as_view(), name='register'),
	url(r'^$',login_required(views.main) , name='first-page'),
    
    url(r'^theory/$',login_required(views.theory) , name='theoria'),
    
    url(r'^example/$',login_required(views.example) , name='examples'),
    url(r'^exercises/$',login_required(views.test), kwargs={'test_type': 'exercise'} , name='exercises'),
    url(r'^test/$',login_required(views.test), kwargs={'test_type': 'test'} , name='tests'),
    url(r'^exam/$',login_required(views.test), kwargs={'test_type': 'exam'}, name='examination'),
    
    url(r'^new-example/$',staff_member_required(views.add), kwargs={'type': 'example'},  name='add-example'),
    url(r'^new-test/$',login_required(views.add), kwargs={'type': 'test'}, name='new-test'),
    url(r'^new-exercise/$',login_required(views.add), kwargs={'type': 'exercise'}, name='new-exercise'),
    url(r'^new-exam/$',login_required(views.add), kwargs={'type': 'exam'}, name='new-exam'),
    
    url(r'^show-students/$',staff_member_required(views.show_students) , name='students'),
    url(r'^progress/$',login_required(views.main), name='students-progress'),

    url(r'^fetch/$',views.fetch, name='fetch-exercise'),
    url(r'^save/$',views.save, name='save-exercise'),


)
