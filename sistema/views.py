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

def error_404(request):

	template = "sistema/404.html"
	return render(request,template)


