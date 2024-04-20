from django.contrib import admin

from .models import DatasAbertas, Especialidade, DadosMedico

# Register your models here.
admin.site.register(Especialidade)
admin.site.register(DadosMedico)
admin.site.register(DatasAbertas)