from datetime import datetime
from sqlite3 import DatabaseError
from django.shortcuts import redirect, render
from django.contrib.messages import constants, add_message
from django.db import transaction

from medico.models import Consulta, DadosMedico, DatasAbertas, Especialidade

# Create your views here.
def home(request):
    if request.method == "GET":

        medico_filtrar = request.GET.get('medico')
        especialidades_filtrar = request.GET.getlist('especialidades')

        medicos = DadosMedico.objects.all()
        if medico_filtrar:
            medicos = medicos.filter(nome__icontains = medico_filtrar)

        if especialidades_filtrar:
            medicos = medicos.filter(especialidade_id__in=especialidades_filtrar)

        especialidades = Especialidade.objects.all()
        return render(request, 'home.html', {"medicos": medicos, "especialidades": especialidades})
    
def escolher_horario(request, id_dados_medicos):
    if request.method == "GET":
        medico = DadosMedico.objects.get(id=id_dados_medicos)
        datas_abertas = DatasAbertas.objects.filter(user=medico.user).filter(data__gte=datetime.now()).filter(agendado=False)
        print(datas_abertas)
        return render(request, 'escolher_horario.html', {'medico': medico, 'datas_abertas': datas_abertas})
    
# @transaction.atomic
def agendar_horario(request, id_data_aberta):
    if request.method == "GET":
        data_aberta = DatasAbertas.objects.get(id=id_data_aberta)

        horario_agendado = Consulta(
            paciente=request.user,
            data_aberta=data_aberta
        )

        try:
            with transaction.atomic():
                horario_agendado.save()
                data_aberta.agendado = True
                data_aberta.save()
        except DatabaseError:
            data_aberta.agendado = False
            data_aberta.save()

        add_message(request, constants.SUCCESS, 'Horário agendado com sucesso.')
        return redirect('/pacientes/minhas_consultas/')
    
def minhas_consultas(request):
    if request.method == "GET":
        #TODO: desenvolver filtros
        minhas_consultas = Consulta.objects.filter(paciente=request.user).filter(data_aberta__data__gte=datetime.now())
        return render(request, 'minhas_consultas.html', {'minhas_consultas': minhas_consultas})
