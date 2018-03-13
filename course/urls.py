from django.conf.urls import url
from . import views

app_name = 'course'

urlpatterns = [
    url('^$', views.login),
    url('^loggedin/$', views.loggedin),
    url('^auth/$', views.auth),
    url('^loggedin/addcourset/$', views.addct),
    url('^loggedin/selectcourse/$', views.selectprof),
    url('^loggedin/selectcourse/addcs/$', views.addcs),
    url('^loggedin/deletecourse/$', views.removesc),
    url('^logout/$', views.logout),
    url('^deletetc/$', views.deletetc),
    url('^addmessage/$', views.addmessage),
    url('^sendmessage/$',views.addmessage),
    url('^studentmsg/$',views.studentmessage)
]


