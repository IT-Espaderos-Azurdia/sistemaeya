from django.shortcuts import render, redirect, HttpResponse
from sistema.forms import CobroForm, EmpresaForm, CobroEmpresaForm, ExpedienteForm, PagoForm
from sistema.models import Cobro, Empresa, CobroEmpresa, Expediente, OperacionMes, CobroEmpresa, Abono
import datetime, os.path
from django.conf import settings
from wsgiref.util import FileWrapper

def home(request):

	template = "sistema/home.html"
	return render(request,template)

def login(request):

	template = "sistema/login.html"
	return render(request,template)

def sistema(request):
	template = "sistema/sistema_home.html"
	empresas = Empresa.objects.all()
	if request.method == 'POST':
		id_empresa = request.POST.get("empresa","")
		str_fecha = request.POST.get("fecha","")
		fecha = str_fecha.split('-',1)
		nombre = request.POST.get("nombre","")
		listado = Expediente.objects.all().filter(cliente__contains=nombre,operacionmes__empresa__id=id_empresa,operacionmes__anio=fecha[0],operacionmes__mes=fecha[1])
		listprecio = []
		for ex in listado:
			empresa = ex.operacionmes.empresa.id
			cobros = ex.cobro.all()
			precio = 0
			for c in cobros:
				temp = CobroEmpresa.objects.all().filter(empresa__id=empresa).filter(cobro__id=c.id)
				precio += temp.first().precio
			listprecio.append([ex,precio])
		context = {'listado':listado,'listp':listprecio,'empresas':empresas}
		return render(request,template,context)
	else:
		context = {'empresas':empresas}
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
	response ['Content-Disposition'] = 'attachment; filename='+os.path.basename(archivo)
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
				print("HOLA ENTRE HAHAHAHAHA")
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
			empresa = request.POST.get("empresa","")
			str_fecha = request.POST.get("fecha_operacion","")
			fecha = str_fecha.split('-',1)
			pago = form.save(commit=False)
			pago.operacionmes = OperacionMes.objects.get(empresa=empresa,mes=fecha[1],anio=fecha[0])
			pago.save()
		return redirect('sistema_pago')
	template = "sistema/forms/pago.html"
	empresas = Empresa.objects.all()
	context = {'form':form,'empresas':empresas}
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

