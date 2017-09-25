from django.conf.urls import url
from django.contrib.auth.decorators import login_required
from . import views
from django.contrib import admin
from django.contrib.auth.views import login, logout_then_login, password_reset, password_reset_done, \
	password_reset_confirm, password_reset_complete
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [

	url(r'^$', views.home, name='home'),
	url(r'^sistema/$', login_required(views.sistema), name='sistema'),
	url(r'^sistema/pago/$', login_required(views.sistema_pago), name='sistema_pago'),

	url(r'^test/$', views.HomeWebSite, name='HomeWebSite'),

	url(r'^empresa/reporte/$', views.ReporteEmpresa, name='ReporteEmpresa'),
	url(r'^empresa/expediente/$', views.ExpedienteEmpresa, name='ExpedienteEmpresa'),

	url(r'^sistema/reportes/$', login_required(views.sistema_reporte), name='sistema_reporte'),
	url(r'^reporte/$', login_required(views.reporte_uno), name='reporte_uno'),

	url(r'^pdf/(?P<id_expediente>\d+)/$', login_required(views.dowload_File), name='dowload_File'),	

	url(r'^form_pago/$', login_required(views.form_pago), name='form_pago'),
	url(r'^editar_pago/(?P<id_pago>\d+)/$', login_required(views.update_pago), name='update_pago'),

	url(r'^form_expediente/$', login_required(views.form_expediente), name='form_expediente'),
	url(r'^editar_expediente/(?P<id_expediente>\d+)/$', login_required(views.update_expediente), name='update_expediente'),

	url(r'^form_precio_cobro/$', login_required(views.form_precio_cobro), name='form_precio_cobro'),
	url(r'^editar_precio_cobro/(?P<id_cobro_precio>\d+)/$', login_required(views.update_precio_cobro), name='update_precio_cobro'),
	url(r'^eliminar_precio_cobro/(?P<id_cobro_precio>\d+)/$', login_required(views.eliminar_precio_cobro), name='eliminar_precio_cobro'),

	url(r'^form_empresa/$', login_required(views.form_empresa), name='form_empresa'),
	url(r'^editar_empresa/(?P<id_empresa>\d+)/$', login_required(views.update_empresa), name='update_empresa'),
	url(r'^eliminar_empresa/(?P<id_empresa>\d+)/$', login_required(views.eliminar_empresa), name='eliminar_empresa'),

	url(r'^form_cobro/$', login_required(views.form_cobro), name='form_cobro'),
	url(r'^eliminar_cobro/(?P<id_cobro>\d+)/$', login_required(views.eliminar_cobro), name='eliminar_cobro'),
	
	url(r'^login/$', login, {'template_name':'sistema/login.html'}, name='login'),
	url(r'^logout/$', logout_then_login, name='logout'),
	url(r'^restaurar_password$', password_reset, {'template_name':'sistema/reset_password_form.html', 
		'email_template_name':'sistema/password_reset_email.html'},name='password_reset'),
	url(r'^reset/password_reset_done$', password_reset_done, {'template_name':'sistema/correoenviado.html'}, name='password_reset_done'),
	url(r'^reset/(?P<uidb64>[0-9A-Za-z_\-]+)/(?P<token>.+)/$', password_reset_confirm, {'template_name':'sistema/password_reset_confirm.html'}, name='password_reset_confirm'),
	url(r'^reset/done$', password_reset_complete, {'template_name':'sistema/passwordcambiado.html'}, name='password_reset_complete'),
]

if settings.DEBUG:
	urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
	urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_URL)