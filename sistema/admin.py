from django.contrib import admin
from sistema.models import Cobro, Empresa, CobroEmpresa, Expediente, OperacionMes

admin.site.register(Cobro)
admin.site.register(Empresa)
admin.site.register(CobroEmpresa)
admin.site.register(Expediente)
admin.site.register(OperacionMes)
