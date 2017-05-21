from django.shortcuts import render

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

def empresa(request):

	template = "sistema/form_empresa.html"
	return render(request,template)

def form_cobro(request):

	template = "sistema/form_cobro.html"
	return render(request,template)

def tramitesvarios(request):

	template = "sistema/tramitesvarios.html"
	return render(request,template)

def form_asignar_cobro(request):

	template = "sistema/form_asignar_cobro.html"
	return render(request,template)



def error_404(request):

	template = "sistema/404.html"
	return render(request,template)


