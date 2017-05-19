from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views
from django.contrib import admin
from django.contrib.auth.views import login, logout_then_login, password_reset, password_reset_done, \
	password_reset_confirm, password_reset_complete


urlpatterns = [

	url(r'^$', views.home, name='home'),
	url(r'^sistema/$', login_required(views.sistema), name='sistema'),
	url(r'^accounts/login/$', login, {'template_name':'sistema/login.html'}, name='login'),
	url(r'^logout/$', logout_then_login, name='logout'),
	url(r'^reset/password_reset$', password_reset, {'template_name':'sistema/reset_password_form.html', 
		'email_template_name':'sistema/password_reset_email.html'},name='password_reset'),
	url(r'^reset/password_reset_done$', password_reset_done, {'template_name':'sistema/correoenviado.html'}, name='password_reset_done'),
	url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', password_reset_confirm, {'template_name':'sistema/password_reset_confirm.html'}, name='password_reset_confirm'),
	url(r'^reset/done$', password_reset_complete, {'template_name':'sistema/passwordcambiado.html'}, name='password_reset_complete'),
]

