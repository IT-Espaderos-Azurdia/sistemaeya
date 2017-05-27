from django import forms
from sistema.models import Cobro, Empresa, CobroEmpresa, Abono, Expediente

class ExpedienteForm(forms.ModelForm):

	class Meta:
		model = Expediente

		fields = [
		    'cobro',
		    'fecha_ingreso_oficina',
		    'fecha_ingreso_digecam',
		    'fecha_cita',
		    'fecha_pago',
		    'fecha_entrega',
		    'recibio',
		    'entrego',
		    'tenencias',
		    'estatus',
		    'descripcion_estatus',
		    'docfile',
		    'cliente',
		]

		labels = {
			'cobro': 'Seleccionar cobros',
		    'fecha_ingreso_oficina': 'Fecha ingreso a oficina',
		    'fecha_ingreso_digecam': 'Fecha ingreso a digecam',
		    'fecha_cita': 'Fecha de cita',
		    'fecha_pago': 'Fecha de pago',
		    'fecha_entrega': 'Fecha de entrega',
		    'recibio': 'Quien recibio',
		    'entrego': 'Quien entrego',
		    'tenencias': 'Numero de tenencias',
		    'estatus': 'Estatus',
		    'descripcion_estatus': 'Descripcion del estatus',
		    'docfile': 'Seleccione archivo',
		    'cliente': 'Nombre cliente',
		}

		widgets = {
			'cobro': forms.CheckboxSelectMultiple(),
		    'fecha_ingreso_oficina': forms.DateInput(format='%d/%m/%Y',attrs={'type':'date'}),
		    'fecha_ingreso_digecam': forms.DateInput(format='%d/%m/%Y',attrs={'type':'date'}),
		    'fecha_cita': forms.DateInput(format='%d/%m/%Y',attrs={'type':'date'}),
		    'fecha_pago': forms.DateInput(format='%d/%m/%Y',attrs={'type':'date'}),
		    'fecha_entrega': forms.DateInput(format='%d/%m/%Y',attrs={'type':'date'}),
		    'recibio': forms.TextInput(attrs={'class':'validate'}),
		    'entrego': forms.TextInput(attrs={'class':'validate'}),
		    'tenencias': forms.NumberInput(attrs={'class':'validate'}),
		    'estatus': forms.Select(attrs={'class': 'validate'},choices=(('ok','ok'),('error','error'))),
		    'descripcion_estatus': forms.TextInput(attrs={'class':'validate'}),
		    'cliente': forms.TextInput(attrs={'class':'validate'}),
		}

class PagoForm(forms.ModelForm):

	class Meta:
		model = Abono

		fields = [
			'monto',
			'fecha',
			'tipo',
			'recibio',
			'codigo',
			'fechadeposito',
			'codigodeposito',
		]

		labels = {
			'monto': 'Monto recibido',
			'fecha': 'Fecha recibido',
			'tipo': 'Forma de abono',
			'recibio': 'Quien recibio',
			'codigo': 'Codigo abono',
			'fechadeposito': 'Fecha depositado/transeferido',
			'codigodeposito': 'Codigo del deposito',
		}

		widgets = {
			'monto': forms.NumberInput(attrs={'class':'validate'}),
			'fecha': forms.DateInput(format='%d/%m/%Y',attrs={'type':'date'}),
			'tipo' : forms.TextInput(attrs={'class':'validate'}),
			'recibio': forms.TextInput(attrs={'class':'validate'}),
			'codigo': forms.TextInput(attrs={'class':'validate'}),
			'fechadeposito': forms.DateInput(format='%d/%m/%Y',attrs={'type':'date'}),
			'codigodeposito': forms.TextInput(attrs={'class':'validate'}),
		}


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