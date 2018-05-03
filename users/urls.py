from django.conf.urls import  url
from  django.contrib.auth.views import login
from . import views
urlpatterns=[
    url(r'^login/$',login,{'template_name':'login.html'},name='login'),
    url(r'^loginout/$',views.logout_view,name='logout'),
    url(r'^register/$',views.register,name='register'),
]
app_name = 'users'