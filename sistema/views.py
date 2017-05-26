from django.shortcuts import render, redirect
from sistema.forms import CobroForm, EmpresaForm, CobroEmpresaForm
from sistema.models import Cobro, Empresa, CobroEmpresa


def home(request):

	template = "sistema/home.html"
	return render(request,template)

def login(request):

	template = "sistema/login.html"
	return render(request,template)

def sistema(request):

	template = "sistema/sistema_home.html"
	return render(request,template)

def tramites(request):

	template = "sistema/tramites.html"
	return render(request,template)

# --------------------------------------------------------------------
# -------------------- FUNCIONES CRUD EMPRESA ------------------------
# --------------------------------------------------------------------

# Funcion agregar una empresa
def form_empresa(request):
	template = "sistema/forms/empresa.html"
	if request.method == 'POST':
		form = EmpresaForm(request.POST)
		if form.is_valid():
			form.save()
		return redirect('form_empresa')
	else:
		form = EmpresaForm()
	list_empresa = Empresa.objects.all()
	context = {'form':form,'listado': list_empresa}		
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


