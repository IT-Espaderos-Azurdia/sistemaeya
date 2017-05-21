from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views
from django.contrib import admin
from django.contrib.auth.views import login, logout_then_login, password_reset, password_reset_done, \
	password_reset_confirm, password_reset_complete


urlpatterns = [

	url(r'^$', views.home, name='home'),
	url(r'^sistema/$', login_required(views.sistema), name='sistema'),
	url(r'^tramites/$', login_required(views.tramites), name='tramites'),
	url(r'^form_empresa/$', login_required(views.empresa), name='empresa'),
	url(r'^form_cobro/$', login_required(views.form_cobro), name='form_cobro'),
	url(r'^form_asignar_cobro/$', login_required(views.form_asignar_cobro), name='form_asignar_cobro'),
	url(r'^tramitesvarios/$', login_required(views.tramitesvarios), name='tramitesvarios'),
	url(r'^login/$', login, {'template_name':'sistema/login.html'}, name='login'),
	url(r'^logout/$', logout_then_login, name='logout'),
	url(r'^restaurar_password$', password_reset, {'template_name':'sistema/reset_password_form.html', 
		'email_template_name':'sistema/password_reset_email.html'},name='password_reset'),
	url(r'^reset/password_reset_done$', password_reset_done, {'template_name':'sistema/correoenviado.html'}, name='password_reset_done'),
	url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', password_reset_confirm, {'template_name':'sistema/password_reset_confirm.html'}, name='password_reset_confirm'),
	url(r'^reset/done$', password_reset_complete, {'template_name':'sistema/passwordcambiado.html'}, name='password_reset_complete'),
]

