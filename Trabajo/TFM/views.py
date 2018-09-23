# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render

from django.views.generic import TemplateView

from django.http import HttpResponse, JsonResponse

from django.views.decorators.csrf import csrf_exempt

#from TFM.models import Cargar_Paciente, Obtener_Pacientes, Generar_Formulario, Predecir_Episodio, Buscador_Pacientes_Similares

from TFM.models import Obtener_Pacientes, Generar_Formulario, Predecir_Episodio, Buscador_Pacientes_Similares, HistoricoPacientes

@csrf_exempt
def dame_pacientes(request):
	html = Obtener_Pacientes.obtener_todos_pacientes()
	return JsonResponse({'resultado': html})

@csrf_exempt
def dame_pacientes_con_filtro(request):
	sexo = request.POST['sexo']
	html = Obtener_Pacientes.obtener_todos_pacientes_con_filtro(sexo)
	return JsonResponse({'resultado': html}) 

@csrf_exempt
def dame_paciente_formulario(request):
	received_json_data=request.body
	enfermo = received_json_data.split("=")[1]
	fechaIngreso, tablaEnfermedadesPaciente, valores, sexo, edad, listaEnfermedadesPaciente = Generar_Formulario.FuncionPrincipal(enfermo)
	return JsonResponse({'fechaIngreso': fechaIngreso, 'tablaEnfermedades': tablaEnfermedadesPaciente, 'valores': valores, 'sexo': sexo, 'edad': edad, 'listaEnfermedades': listaEnfermedadesPaciente})

@csrf_exempt
def predecir(request):
	received_json_data=request.body
	enfermo = received_json_data.split("=")[1]
	html = Predecir_Episodio.main(enfermo)
	print "He terminado, deberia devolver el mensaje a la aplicacion que es " + str(html)
	return JsonResponse({'resultado': html})

@csrf_exempt
def buscarSimilar(request):
	enfermo = request.POST['paciente']
	usarEdad = request.POST['usarEdad'] == "true"
	edad = request.POST['edad']
	usarSexo = request.POST['usarSexo'] == "true"
	sexo = request.POST['sexo']
	usarEnfermedades = request.POST['usarEnfermedades'] == "true"
	enfermedad = request.POST['enfermedades']
	print edad
	print sexo
	print enfermedad
	html = Buscador_Pacientes_Similares.main(enfermo, usarEdad, usarSexo, usarEnfermedades, sexo, edad, enfermedad)
	return JsonResponse({'resultado': html})

@csrf_exempt
def historicoPacientes(request):
	tablaGrafica, tablaNombreEnfermos = HistoricoPacientes.FuncionPrincipal()
	
	return JsonResponse({'grafica': tablaGrafica, 'enfermos': tablaNombreEnfermos})


# Create your views here.
class HomePageView(TemplateView):
    def get(self, request, **kwargs):
        return render(request, "formulario.php", context=None)

		
class AboutPageView(TemplateView):
    template_name = "prueba.php"
	

class Formulario(TemplateView):
    template_name = "formulario.php"

