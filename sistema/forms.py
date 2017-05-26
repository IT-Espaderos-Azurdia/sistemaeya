from django import forms
from sistema.models import Cobro, Empresa, CobroEmpresa

class CobroEmpresaForm(forms.ModelForm):
	
	class Meta:
		
		model = CobroEmpresa

		fields = [
			'precio',
			'empresa',
			'cobro',
		]

		labels = {
			'precio': 'Precio',
			'empresa': 'Empresa',
			'cobro': 'Cobro'
		}

		widgets = {
			'precio': forms.NumberInput(attrs={'class':'validate'}),
			'cobro': forms.Select(attrs={'class': 'validate'}),
			'empresa': forms.Select(attrs={'class': 'validate'}),
			
		}

class CobroForm(forms.ModelForm):
	
	class Meta:
		model = Cobro

		fields = [
			'nombre',
		]

		labels = {
			'nombre':'Nombre Del Cobro'
		}

		widgets = {
			'nombre':forms.TextInput(attrs={'class':'validate'}),
		}


class EmpresaForm(forms.ModelForm):

	class Meta:
		model = Empresa

		fields = [
			'nombre',
			'telefono',
			'correo',
		]

		labels = {
			'nombre': 'Nombre Empresa',
			'telefono': 'Telefono',
			'correo': 'Email',
		}

		widgets = {
			'nombre':forms.TextInput(attrs={'class':'validate'}),
			'telefono':forms.NumberInput(attrs={'class':'validate'}),	
			'correo':forms.EmailInput(attrs={'class':'validate'}),
		}