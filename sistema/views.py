from django.shortcuts import render, redirect, HttpResponse
from django.core.files.storage import FileSystemStorage
from django.template.loader import render_to_string
from sistema.forms import CobroForm, EmpresaForm, CobroEmpresaForm, ExpedienteForm, PagoForm
from sistema.models import Cobro, Empresa, CobroEmpresa, Expediente, OperacionMes, CobroEmpresa, Abono
import datetime, os.path, csv
from weasyprint import HTML
from django.conf import settings
from wsgiref.util import FileWrapper
from django.db.models import Sum

def home(request):

	template = "sistema/home.html"
	return render(request,template)

def HomeWebSite(request):

	template = "sistema/home_presentacion.html"
	return render(request,template)

def login(request):

	template = "sistema/login.html"
	return render(request,template)

def sistema_reporte(request):
	if request.method == 'POST':
		reporte = request.POST.get("reporte","")
		empresa = request.POST.get("empresa","")
		str_fecha = request.POST.get("fecha","")
		fecha = str_fecha.split('-',1)
		Nombre_empresa = Empresa.objects.only('nombre').get(id=empresa)
		op_mes = OperacionMes.objects.filter(empresa=empresa,mes=fecha[1],anio=fecha[0])
		Precio_Total = 0
		Total_Pago = 0
		Listado_Pagos = None
		if reporte == '0':
			if op_mes.first() is not None:
				listado = Expediente.objects.all().filter(operacionmes__empresa__id=empresa,operacionmes__anio=fecha[0],operacionmes__mes=fecha[1])
				listprecio = []

				for ex in listado:
					empresa = ex.operacionmes.empresa.id
					cobros = ex.cobro.all()
					precio = 0
					for c in cobros:
						temp = CobroEmpresa.objects.all().filter(empresa__id=empresa).filter(cobro__id=c.id)
						if temp.first() is not None:
							if 'tenencia' in c.nombre.lower():
								precio += temp.first().precio * ex.tenencias
							else:
								precio += temp.first().precio
					Precio_Total += precio
					listprecio.append([ex,precio])
					Listado_Pagos = Abono.objects.filter(operacionmes__empresa__id=empresa,operacionmes__anio=fecha[0],operacionmes__mes=fecha[1])
					Total_Pago = Abono.objects.filter(operacionmes__empresa__id=empresa,operacionmes__anio=fecha[0],operacionmes__mes=fecha[1]).aggregate(Sum('monto'))

				context2 = {'fecha':str_fecha,'Empresa':Nombre_empresa,'key_reporte_uno':True,'key_reporte_dos':False,'listado':listado,'precio':listprecio,'Precio_Total':Precio_Total,'Listado_Pagos':Listado_Pagos,'Total_Pago':Total_Pago}
				
			else:
				context2 = {'key_reporte_uno':False,'key_reporte_dos':False}
		else:
			Total_Ingresos = 0
			Total_Ingresos_Acutal = 0
			Saldo_General = 0
			Listado_empresas = Empresa.objects.all()
			listgeneral = []
			for Emp in Listado_empresas:
				listado = Expediente.objects.all().filter(operacionmes__empresa__id=Emp.id,operacionmes__anio=fecha[0],operacionmes__mes=fecha[1])
				precio = 0
				Precio_Total = 0
				saldo = 0
				for ex in listado:
					empresa = ex.operacionmes.empresa.id
					cobros = ex.cobro.all()
					precio = 0
					saldo = 0
					for c in cobros:
						temp = CobroEmpresa.objects.all().filter(empresa__id=empresa).filter(cobro__id=c.id)
						if temp.first() is not None:
							if 'tenencia' in c.nombre.lower():
								precio += temp.first().precio * ex.tenencias
							else:
								precio += temp.first().precio
					Precio_Total += precio
					T_P = Abono.objects.filter(operacionmes__empresa__id=Emp.id,operacionmes__anio=fecha[0],operacionmes__mes=fecha[1]).aggregate(Sum('monto'))
					if T_P['monto__sum'] is None:
						Total_Pago = 0
					else:
						Total_Pago = T_P['monto__sum']
					saldo = Precio_Total - Total_Pago
				Total_Ingresos += Precio_Total
				if Total_Pago is None:
						Total_Pago = 0
				Total_Ingresos_Acutal += Total_Pago
				Saldo_General += saldo
				
				listgeneral.append([Emp.nombre,Precio_Total,Total_Pago,saldo])
				Precio_Total = 0
				Total_Pago = None
			context2 = {'Saldo_General':Saldo_General,'Ingresos':Total_Ingresos,'TIA':Total_Ingresos_Acutal,'fecha':str_fecha,'Listageneral':listgeneral,'key_reporte_uno':False,'key_reporte_dos':True}

		html_string = render_to_string('sistema/reportes/reporte_uno.html',context2)

		html = HTML(string=html_string)
		namefile = "reporte_uno.pdf"
		html.write_pdf(target=settings.MEDIA_ROOT+'/'+namefile)

		f = open(settings.MEDIA_ROOT+'/'+namefile,"rb")
		response = HttpResponse(FileWrapper(f), content_type='application/pdf')
		response ['Content-Disposition'] = 'inline; filename='+os.path.basename(namefile)
		f.close()
		return response

	else:
		template = 'sistema/reportes.html'
		reportes = ['Reporte detalle','Reporte general de estado']
		empresas = Empresa.objects.all()
		context = {'empresas':empresas,'reportes':reportes}
		return render(request,template,context)

def ReporteEmpresa(request):
	if request.method == 'POST':
		

		str_fecha = request.POST.get("fecha","")
		usuario = request.POST.get("username","")
		password = request.POST.get("password","")

		fecha = str_fecha.split('-',1)

		try:
			EmpresaUsuario = Empresa.objects.get(usuario=usuario,password=password)
			empresa = EmpresaUsuario.id
			Nombre_empresa = Empresa.objects.only('nombre').get(id=empresa)
		except Empresa.DoesNotExist:
			empresa = -1

		if empresa == -1:
			template = 'sistema/ReporteEmpresa.html'
			Error = 1
			ErrorTipo = "Credenciales invalidas! Verifique su contraseña y usuario."
			context = {'ErrorTipo':ErrorTipo,'Error':Error,'username':usuario,'password':password}
			return render(request,template,context)
		else:
			response = HttpResponse(content_type='text/csv')
			NombreReporte = "["+EmpresaUsuario.nombre+"]Gestion Operativa "+str_fecha+".csv"
			response['Content-Disposition'] = 'attachment; filename='+NombreReporte
			writer = csv.writer(response)

			op_mes = OperacionMes.objects.filter(empresa=empresa,mes=fecha[1],anio=fecha[0])
			Precio_Total = 0
			Total_Pago = 0
			Listado_Pagos = None
			if op_mes.first() is not None:
				#writer.writerow(['Nombre', 'Numero Expediente','No. Tenencias','Total a Pagar Q','Fecha Ingreso Oficina','Fecha Ingreso Digecam','Fecha Cita','Fecha Pago','Fecha Entrega','Quien Entrego','Quien Recibio','Estatus','cobros','Descripcion Estado'])
				writer.writerow(['Numero Expediente','Nombre','Fecha Ingreso Oficina','Fecha Entrega','Estatus','cobros','Total a Pagar Q'])
				listado = Expediente.objects.all().filter(operacionmes__empresa__id=empresa,operacionmes__anio=fecha[0],operacionmes__mes=fecha[1])
				listprecio = []
				for ex in listado:
					empresa = ex.operacionmes.empresa.id
					cobros = ex.cobro.all()
					precio = 0
					CobroDescripcion = "-"
					for c in cobros:
						CobroDescripcion += c.nombre+"-"
						temp = CobroEmpresa.objects.all().filter(empresa__id=empresa).filter(cobro__id=c.id)
						if temp.first() is not None:
							if 'tenencia' in c.nombre.lower():
								precio += temp.first().precio * ex.tenencias
							else:
								precio += temp.first().precio
					#writer.writerow([ex.cliente, ex.numeroexpe,ex.tenencias,precio,ex.fecha_ingreso_oficina,ex.fecha_ingreso_digecam,ex.fecha_cita,ex.fecha_pago,ex.fecha_entrega,ex.entrego,ex.recibio,ex.estatus,CobroDescripcion,ex.descripcion_estatus])
					writer.writerow([ex.numeroexpe,ex.cliente,ex.fecha_ingreso_oficina,ex.fecha_entrega,ex.estatus,CobroDescripcion,precio])
					#Precio_Total += precio
					#listprecio.append([ex,precio])
					#Listado_Pagos = Abono.objects.filter(operacionmes__empresa__id=empresa,operacionmes__anio=fecha[0],operacionmes__mes=fecha[1])
					#Total_Pago = Abono.objects.filter(operacionmes__empresa__id=empresa,operacionmes__anio=fecha[0],operacionmes__mes=fecha[1]).aggregate(Sum('monto'))
				#context2 = {'fecha':str_fecha,'Empresa':Nombre_empresa,'key_reporte_uno':True,'key_reporte_dos':False,'listado':listado,'precio':listprecio,'Precio_Total':Precio_Total,'Listado_Pagos':Listado_Pagos,'Total_Pago':Total_Pago}	
				return response
			else:
				template = 'sistema/ReporteEmpresa.html'
				Error = 1
				ErrorTipo = "Mes operativo sin gestiones."
				context = {'ErrorTipo':ErrorTipo,'Error':Error,'username':usuario,'password':password}
				return render(request,template,context)
			"""
			html_string = render_to_string('sistema/reportes/reporte_uno.html',context2)

			html = HTML(string=html_string)
			namefile = "reporte_uno.pdf"
			html.write_pdf(target=settings.MEDIA_ROOT+'/'+namefile)

			f = open(settings.MEDIA_ROOT+'/'+namefile,"rb")
			response = HttpResponse(FileWrapper(f), content_type='application/pdf')
			response ['Content-Disposition'] = 'attachment; filename='+os.path.basename(namefile)
			f.close()

			return response"""

	else:
		template = 'sistema/ReporteEmpresa.html'
		reportes = ['Reporte detalle','Reporte general de estado']
		empresas = Empresa.objects.all()
		Error = 0
		context = {'empresas':empresas,'reportes':reportes,'Error':Error}
		return render(request,template,context)

def sistema(request):
	template = "sistema/sistema_home.html"
	empresas = Empresa.objects.all()
	if request.method == 'POST':
		id_empresa = request.POST.get("empresa","")
		str_fecha = request.POST.get("fecha","")
		fecha = str_fecha.split('-',1)
		nombre = request.POST.get("nombre","")
		listado = Expediente.objects.all().filter(cliente__icontains=nombre,operacionmes__empresa__id=id_empresa,operacionmes__anio=fecha[0],operacionmes__mes=fecha[1]).order_by('-operacionmes')#,operacionmes__anio=fecha[0],operacionmes__mes=fecha[1])
		listprecio = []
		for ex in listado:
			empresa = ex.operacionmes.empresa.id
			cobros = ex.cobro.all()
			precio = 0
			for c in cobros:
				temp = CobroEmpresa.objects.all().filter(empresa__id=empresa).filter(cobro__id=c.id)
				if temp.first() is not None:
					if 'tenencia' in c.nombre.lower():
						precio += temp.first().precio * ex.tenencias
				#	elif 'firma' in c.nombre.lower():
				#		precio += temp.first().precio * ex.autenticafirma
				#	elif 'dpi' in c.nombre.lower():
				#		precio += temp.first().precio * ex.autenticadpi
				#	elif 'ingresos' in c.nombre.lower():
				#		precio += temp.first().precio * ex.constanciaingresos
				#	elif 'venta' in c.nombre.lower():
				#		precio += temp.first().precio * ex.formularios
					else:
						precio += temp.first().precio
			listprecio.append([ex,precio])
		context = {'listado':listado,'listp':listprecio,'empresas':empresas}
		return render(request,template,context)
	else:
		context = {'empresas':empresas}
		return render(request,template, context)		

def ExpedienteEmpresa(request):
	template = "sistema/EmpresaExpedientes.html"
	empresas = Empresa.objects.all()
	usuario = ""
	password = ""
	Error = 0
	if request.method == 'POST':

		usuario = request.POST.get("username","")
		password = request.POST.get("password","")
		str_fecha = request.POST.get("fecha","")
		fecha = str_fecha.split('-',1)

		try:
			EmpresaUsuario = Empresa.objects.get(usuario=usuario,password=password)
			id_empresa = EmpresaUsuario.id
			usuario = EmpresaUsuario.usuario
			password = EmpresaUsuario.password
		except Empresa.DoesNotExist:
			id_empresa = -1
			Error = 1

		nombre = request.POST.get("nombre","")
		listado = Expediente.objects.all().filter(cliente__icontains=nombre,operacionmes__empresa__id=id_empresa,operacionmes__anio=fecha[0],operacionmes__mes=fecha[1]).order_by('-operacionmes')
		listprecio = []
		for ex in listado:
			empresa = ex.operacionmes.empresa.id
			cobros = ex.cobro.all()
			precio = 0
			for c in cobros:
				temp = CobroEmpresa.objects.all().filter(empresa__id=empresa).filter(cobro__id=c.id)
				if temp.first() is not None:
					if 'tenencia' in c.nombre.lower():
						precio += temp.first().precio * ex.tenencias
				#	elif 'firma' in c.nombre.lower():
				#		precio += temp.first().precio * ex.autenticafirma
				#	elif 'dpi' in c.nombre.lower():
				#		precio += temp.first().precio * ex.autenticadpi
				#	elif 'ingresos' in c.nombre.lower():
				#		precio += temp.first().precio * ex.constanciaingresos
				#	elif 'venta' in c.nombre.lower():
				#		precio += temp.first().precio * ex.formularios
					else:
						precio += temp.first().precio
			listprecio.append([ex,precio])
		context = {'Error':Error,'listado':listado,'listp':listprecio,'empresas':empresas,'username':usuario,'password':password}
		return render(request,template,context)
	else:
		context = {'Error':Error,'empresas':empresas,'username':usuario,'password':password}
		return render(request,template, context)

def sistema_pago(request):
	template = "sistema/sistema_pago.html"
	empresas = Empresa.objects.all()
	if request.method == 'POST':
		codigo = request.POST.get("codigo","")
		listado = Abono.objects.all().filter(codigo__contains=codigo)
		context = {'listado':listado}
		return render(request,template,context)
	else:
		return render(request,template)

def dowload_File(request,id_expediente):
	expediente = Expediente.objects.get(id=id_expediente)
	archivo = expediente.docfile.name
	f = open(settings.MEDIA_ROOT+'/'+archivo,"rb")
	response = HttpResponse(FileWrapper(f), content_type='application/pdf')
	response ['Content-Disposition'] = 'inline; filename='+os.path.basename(archivo)
	f.close()
	return response


def reporte_uno(request):

	html_string = render_to_string('sistema/reportes/reporte_uno.html',{'lo':'lo'})

	html = HTML(string=html_string)
	namefile = "reporte_uno.pdf"
	html.write_pdf(target=settings.MEDIA_ROOT+'/'+namefile)

	f = open(settings.MEDIA_ROOT+'/'+namefile,"rb")
	response = HttpResponse(FileWrapper(f), content_type='application/pdf')
	response ['Content-Disposition'] = 'inline; filename='+os.path.basename(namefile)
	f.close()
	return response


	

# --------------------------------------------------------------------
# ------------------ FUNCIONES CRUD EXPEDIENTE -----------------------
# --------------------------------------------------------------------

# Funcion agregar una expediente
def form_expediente(request):
	template = "sistema/forms/expediente.html"
	if request.method == 'POST':
		form = ExpedienteForm(request.POST)
		if form.is_valid():
			empresa = request.POST.get("empresa","")
			mes = datetime.datetime.today().month
			anio = datetime.datetime.today().year
			if not OperacionMes.objects.all().filter(empresa=empresa,mes=mes,anio=anio).exists():
				OperacionMes.objects.create(empresa=Empresa.objects.get(id=empresa),mes=mes,anio=anio)
			expediente = form.save(commit=True)
			expediente.operacionmes = OperacionMes.objects.get(empresa=empresa,mes=mes,anio=anio)
			cobros = form.cleaned_data['cobro']
			for c in cobros:
				expediente.cobro.add((Cobro.objects.get(id=c.id)))
			expediente.save()
		return redirect('form_expediente')
	else:
		form = ExpedienteForm()
	list_empresa = Empresa.objects.all()
	Key_empresa = True
	key_Form = False
	context = {'form':form,'listado': list_empresa,'key_Form':key_Form,'Key_empresa':Key_empresa}		
	return render(request,template,context)	

# Funcion actualizar empresa
def update_expediente(request,id_expediente):
	expediente = Expediente.objects.get(id=id_expediente)
	if request.method == 'GET':
		form = ExpedienteForm(instance=expediente)
	else:
		form = ExpedienteForm(request.POST,request.FILES,instance=expediente)
		if form.is_valid():
			form.save()
		return redirect('form_expediente')
	template = "sistema/forms/expediente.html"
	context = {'form':form,'key_Form':True,'Key_empresa':False}
	return render(request,template,context)

# Funcion Eliminar Expediente
def eliminar_expediente(request,id_expediente):
	if Expediente.objects.all().filter(id=id_expediente).exists():
		expediente = Expediente.objects.get(id=id_expediente)
		if request.method == 'POST':
			expediente.docfile.delete()
			expediente.delete()
			return redirect('sistema')
		template = "sistema/eliminar/expediente.html"
		context = {'expediente':expediente}
		return render(request,template,context)
	else:
		return redirect('sistema')


# --------------------------------------------------------------------
# --------------------- FUNCIONES CRUD PAGO --------------------------
# --------------------------------------------------------------------

# Funcion agregar una pago
def form_pago(request):
	template = "sistema/forms/pago.html"
	abonos = Abono.objects.all()
	if request.method == 'POST':
		form = PagoForm(request.POST)
		if form.is_valid():
			empresa = request.POST.get("empresa","")
			str_fecha = request.POST.get("fecha_operacion","")
			fecha = str_fecha.split('-',1)
			if OperacionMes.objects.all().filter(empresa=empresa,mes=fecha[1],anio=fecha[0]).exists():
				pago = form.save(commit=False)
				pago.operacionmes = OperacionMes.objects.get(empresa=empresa,mes=fecha[1],anio=fecha[0])
				pago.save()
		return redirect('form_pago')
	else:
		form = PagoForm()
	empresas = Empresa.objects.all()
	context = {'form':form,'abonos':abonos,'empresas':empresas,'key_empresa':True}		
	return render(request,template,context)	

# Funcion actualizar pago
def update_pago(request,id_pago):
	abono = Abono.objects.get(id=id_pago)
	if request.method == 'GET':
		form = PagoForm(instance=abono)
	else:
		form = PagoForm(request.POST,instance=abono)
		if form.is_valid():
			#empresa = request.POST.get("empresa","")
			#str_fecha = request.POST.get("fecha_operacion","")
			#fecha = str_fecha.split('-',1)
			pago = form.save(commit=False)
			#pago.operacionmes = OperacionMes.objects.get(empresa=empresa,mes=fecha[1],anio=fecha[0])
			pago.save()
		return redirect('sistema_pago')
	template = "sistema/forms/pago.html"
	empresas = Empresa.objects.all()
	context = {'form':form,'empresas':empresas,'key':False}
	return render(request,template,context)



# --------------------------------------------------------------------
# -------------------- FUNCIONES CRUD EMPRESA ------------------------
# --------------------------------------------------------------------

# Funcion agregar una empresa
def form_empresa(request):
	template = "sistema/forms/empresa.html"
	empresas = Empresa.objects.all()
	if request.method == 'POST':
		form = EmpresaForm(request.POST)
		if form.is_valid():
			form.save()
		return redirect('form_empresa')
	else:
		form = EmpresaForm()
	context = {'form':form,'empresas':empresas}		
	return render(request,template,context)	

# Funcion actualizar empresa
def update_empresa(request,id_empresa):
	empresa = Empresa.objects.get(id=id_empresa)
	if request.method == 'GET':
		form = EmpresaForm(instance=empresa)
	else:
		form = EmpresaForm(request.POST,instance=empresa)
		if form.is_valid():
			form.save()
		return redirect('form_empresa')
	template = "sistema/forms/empresa.html"
	context = {'form':form}
	return render(request,template,context)

# Funcion Eliminar Empresa
def eliminar_empresa(request,id_empresa):
	if Empresa.objects.all().filter(id=id_empresa).exists():
		empresa = Empresa.objects.get(id=id_empresa)
		if request.method == 'POST':
			empresa.delete()
			return redirect('form_empresa')
		template = "sistema/eliminar/empresa.html"
		context = {'empresa':empresa}
		return render(request,template,context)
	else:
		return redirect('form_empresa')


# --------------------------------------------------------------------
# --------------------- FUNCIONES CRUD COBRO -------------------------
# --------------------------------------------------------------------

# Funcion agregar cobro
def form_cobro(request):
	template = "sistema/forms/cobro.html"
	if request.method == 'POST':
		form = CobroForm(request.POST)
		if form.is_valid():
			form.save()
		return redirect('form_cobro')
	else:
		form = CobroForm()

	list_cobro = Cobro.objects.all()
	context = {'form':form,'listado': list_cobro}		
	return render(request,template,context)

# Funcion eliminar cobro
def eliminar_cobro(request,id_cobro):
	if Cobro.objects.all().filter(id=id_cobro).exists():
		cobro = Cobro.objects.get(id=id_cobro)
		if request.method == 'POST':
			cobro.delete()
			return redirect('form_cobro')
		template = "sistema/eliminar/cobro.html"
		context = {'cobro':cobro}
		return render(request,template,context)
	else:
		return redirect('form_cobro')

# --------------------------------------------------------------------
# ----------------- FUNCIONES CRUD PRECIO COBRO ----------------------
# --------------------------------------------------------------------

# Funcion agregar Precio Cobro
def form_precio_cobro(request):
	template = "sistema/forms/precio_cobro.html"
	if request.method == 'POST':
		form = CobroEmpresaForm(request.POST)
		if form.is_valid():
			form.save()
		return redirect('form_precio_cobro')
	else:
		form = CobroEmpresaForm()
	list_precio_cobro = CobroEmpresa.objects.all().order_by('empresa')
	context = {'form':form,'listado': list_precio_cobro}		
	return render(request,template,context)	

# Funcion actualizar Precio Cobro
def update_precio_cobro(request,id_cobro_precio):
	cobroempresa = CobroEmpresa.objects.get(id=id_cobro_precio)
	if request.method == 'GET':
		form = CobroEmpresaForm(instance=cobroempresa)
	else:
		form = CobroEmpresaForm(request.POST,instance=cobroempresa)
		if form.is_valid():
			form.save()
		return redirect('form_precio_cobro')
	template = "sistema/forms/precio_cobro.html"
	context = {'form':form}
	return render(request,template,context)

# Funcion Eliminar Precio Cobro
def eliminar_precio_cobro(request,id_cobro_precio):
	if CobroEmpresa.objects.all().filter(id=id_cobro_precio).exists():
		cobroempresa = CobroEmpresa.objects.get(id=id_cobro_precio)
		if request.method == 'POST':
			cobroempresa.delete()
			return redirect('form_precio_cobro')
		template = "sistema/eliminar/precio_cobro.html"
		context = {'CobroEmpresa':cobroempresa}
		return render(request,template,context)
	else:
		return redirect('form_precio_cobro')


# --------------------------------------------------------------------
# -------------------- FUNCIONES ERRORES 404 -------------------------
# --------------------------------------------------------------------

def error_404(request):

	template = "sistema/errores/404.html"
	return render(request,template)



# --------------------------------------------------------------------
# ---------------------- FUNCIONES NO RENDER  ------------------------
# --------------------------------------------------------------------

def ErrorAcceso(request):
	template = "sistema/errores/ErrorAcceso.html"
	return render(request,template)