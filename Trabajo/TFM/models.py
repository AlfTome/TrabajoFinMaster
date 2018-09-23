#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import unicode_literals

from django.db import models

import webbrowser 
import os.path
import csv
import codecs
import json
import urllib2
import threading
import operator
from datetime import datetime
from calendar import timegm
from perceptron import Perceptron
from itertools import islice

class Obtener_Pacientes(models.Model):
	
	@classmethod
	def obtener_todos_pacientes(var):
		i=0
		infoDevuleta = list()
		enfermos = []
		for dirname, dirnames, filenames in os.walk(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'dataset')):
			if len(dirnames) != 0:
				enfermos = dirnames
		for enfermo in enfermos:
			infoDevuleta.append(str(enfermo))
		return enfermos

	@classmethod
	def obtener_todos_pacientes_con_filtro(var, sexo):
		infoDevuleta = list()

		dSexoEdadEpisodio = Predecir_Episodio.ObtenerSexoEdad()
		enfermos = Obtener_Pacientes.obtener_todos_pacientes()

		for enfermo in enfermos:
			if(dSexoEdadEpisodio[enfermo].split("-")[0] == sexo):
				infoDevuleta.append(str(enfermo))

		return infoDevuleta

class Predecir_Episodio:
	@classmethod
	def ObtenerSexoEdad(var):

		directorio = "datosGenerales.csv"

		DIR_DATOS_GENERALES = os.path.join(os.path.dirname(os.path.realpath(__file__)), directorio)
		file = open(DIR_DATOS_GENERALES,"r+")

		reader_file = csv.reader(file)

		dPacientesEdad = dict()

		for line in reader_file:
			if line[0] not in "Paciente":
				dPacientesEdad[line[0]] = line[1] + "-" + line[2] + "-" + line[3]

		return dPacientesEdad

class Generar_Formulario(models.Model):

	@classmethod
	def ObtenerSexoEdad(var, enfermo):

		directorio = "datosGenerales.csv"
		DIR_DATOS_GENERALES = os.path.join(os.path.dirname(os.path.realpath(__file__)), directorio)
		file = open(DIR_DATOS_GENERALES,"r+")

		reader_file = csv.reader(file)

		dPacientesEdad = dict()

		for line in reader_file:
			if line[0] not in "Paciente":
				dPacientesEdad[line[0]] = line[1] + "-" + line[2]

		return dPacientesEdad[enfermo]

	@classmethod
	def obtenerFechaIngreso(var, linea):
	    fecha = linea.replace('\t', ' ').split(" ")[1].replace("]", "")
	    dia = fecha.split("/")[0]
	    mes = fecha.split("/")[1]
	    anio = fecha.split("/")[2]

	    return anio + "-" + mes + "-" + dia

	@classmethod
	def ObtenerEnfermedades(var, fichero):

		lEnfermedades = list()
		dEnfermedadFecha = dict()
		for linea in fichero:
			if 'dd=' in linea and 'dd=V' not in linea and 'dd=E' not in linea:
				fechaDetectado = linea.split(']')[0].split(" ")[1]
				enfermedadCompleta = linea.split('dd=')[1].split('\t')[0]
				enfermedad =  enfermedadCompleta[:3]
				subenfermedad = enfermedadCompleta[3:]
				if subenfermedad != "" and subenfermedad != "0":
					enfermedadCompleta = enfermedad + '.' + subenfermedad
				else:
					enfermedadCompleta = enfermedad

				if enfermedadCompleta not in lEnfermedades:
					lEnfermedades.append(enfermedadCompleta)
					dEnfermedadFecha[enfermedadCompleta] = fechaDetectado

		lEnfermedades.sort()

		return lEnfermedades, dEnfermedadFecha

	@classmethod
	def GenerarDiccionarioConEnfermedades(var):
		directorio = 'CIE9MC.csv'
		DIR_PATIENTS_LIST = os.path.join(os.path.dirname(os.path.realpath(__file__)), directorio)
		with codecs.open(DIR_PATIENTS_LIST, "r", encoding="utf8", errors='ignore') as f:
			reader_file = csv.reader(f)
			diccionario = dict()

			for datos in reader_file:
				if datos[0] != "":
					diccionario[str(datos[0])] = datos[1]

		return diccionario

	@classmethod
	def CargarPacienteConcreto(paciente, paciente_concreto):
	
		direccion_paciente = 'dataset/' + paciente_concreto + '/' + paciente_concreto + '.csv'
		
		DIR_PATIENTS_LIST = os.path.join(os.path.dirname(os.path.realpath(__file__)), direccion_paciente)
		
		mensaje = []
		valores = []
		
		file = open(DIR_PATIENTS_LIST, "r+")
		reader_file = csv.reader(file)
		
		fmt = '%d/%m/%Y %H:%M:%S'
		
		for datos in reader_file:
			if datos[0].upper() != 'TIMESTAMP' :
				if int(float(datos[5])) != 0:
					fecha = datos[0]
					parClaveValor = [timegm(datetime.strptime(fecha, fmt).utctimetuple()), int(float(datos[5]))]
					valores.append(parClaveValor)

		return valores

	@classmethod
	def CrearTabla(var, listaEnfermedadesPaciente, dEnfermedadFecha, diccionarioEnfermedades):
		codigoHTML = "<thead><tr><th>Fecha de detección</th><th>Código</th><th>Enfermedad</th></tr></thead><tbody>"
		for enfermedad in listaEnfermedadesPaciente:
			#print str(enfermedad)
			#print str(dEnfermedadFecha[enfermedad])
			print diccionarioEnfermedades[enfermedad]
			codigoHTML += "<tr><td>" + str(dEnfermedadFecha[enfermedad]) + "</td> <td>" + str(enfermedad) + "</td> <td>" + str(diccionarioEnfermedades[enfermedad]) + "</td></tr>"
		codigoHTML += "</tbody>"

		return codigoHTML

	@classmethod
	def FuncionPrincipal(variable, enfermo):

		mensaje = []

		print enfermo

		direccion_paciente = "dataset/" + enfermo + "/" + enfermo + ".txt"

		DIR_PATIENTS_LIST = os.path.join(os.path.dirname(os.path.realpath(__file__)), direccion_paciente)

		file = open(DIR_PATIENTS_LIST)

		primeraLinea = file.readline()

		fechaIngreso = Generar_Formulario.obtenerFechaIngreso(primeraLinea)

		diccionarioEnfermedades = Generar_Formulario.GenerarDiccionarioConEnfermedades()

		listaEnfermedadesPaciente, dEnfermedadFecha = Generar_Formulario.ObtenerEnfermedades(file)

		tablaEnfermedadesPaciente = Generar_Formulario.CrearTabla(listaEnfermedadesPaciente, dEnfermedadFecha, diccionarioEnfermedades)

		valores = Generar_Formulario.CargarPacienteConcreto(enfermo)

		sexoEdad = Generar_Formulario.ObtenerSexoEdad(enfermo)

		return fechaIngreso, tablaEnfermedadesPaciente, valores, sexoEdad.split("-")[0], sexoEdad.split("-")[1], listaEnfermedadesPaciente

class Predecir_Episodio:

	@classmethod
	def generarListasHilos(var, listaEnfermos, lPaciente, dPacientesSexoEdad, listaClavesEnfermedades):
	    for i in listaEnfermos:
	        lPaciente.append(Predecir_Episodio.generarListasHilo(i, dPacientesSexoEdad,listaClavesEnfermedades))
	   
	@classmethod
	def generarListasHilo(var, usuario, dPacientesSexoEdad, listaClavesEnfermedades, enfermoBuscado = False):
		direccion_paciente = 'dataset/' + usuario + '/' + usuario + '.csv'

		DIR_DATOS_GENERALES = os.path.join(os.path.dirname(os.path.realpath(__file__)), direccion_paciente)
		file = open(DIR_DATOS_GENERALES,"r+")
		reader_file = csv.reader(file)

		direccion_paciente_txt = "dataset/" + usuario + "/" + usuario + ".txt"
		DIR_PATIENTS_LIST_TXT = os.path.join(os.path.dirname(os.path.realpath(__file__)), direccion_paciente_txt)
		file_txt = open(DIR_PATIENTS_LIST_TXT)

		lDatosParaLista = list();
		lDatos = list();

		valores = tuple();

		for datos in reader_file:
			if datos[5] != 'SpO2' and datos[5] != 0:
				lDatos.append(float(datos[5]))

		lEnfermedadesPaciente = Predecir_Episodio.ObtenerTodasEnfermedadesParaPrediccionPaciente(file_txt)

		valores = tuple(lDatos)

		media = sum(valores)/len(valores)

		sexoEdad = dPacientesSexoEdad[usuario]

		sexo = sexoEdad.split("-")[0];

		if sexo == 'M':
			sexo = 1
		else:
			sexo = 0

		edad = sexoEdad.split("-")[1];

		if(edad == '90+'):
			edad = 90;
		else:
			edad = int(float(edad))

		lDatosParaLista.append(edad)
		lDatosParaLista.append(sexo)
		lDatosParaLista.append(media)
		lDatosParaLista.extend(Predecir_Episodio.GenerarListaConValoresPrediccionEnfermedades(lEnfermedadesPaciente, listaClavesEnfermedades))

		if not enfermoBuscado:
			lDatosParaLista.append(Predecir_Episodio.ObtenersiEpisodio(usuario, dPacientesSexoEdad))

		return lDatosParaLista

	@classmethod
	def ObtenersiEpisodio(var, paciente, datosGenerales):
		return int(float(datosGenerales[paciente].split("-")[2]))

	@classmethod   
	def ObtenerTodasEnfermedadesParaPrediccionPaciente(var, fichero):

		lEnfermedades = list()
		for linea in fichero:
			if 'dd=' in linea and 'dd=V' not in linea and 'dd=E' not in linea:
				enfermedadCompleta = linea.split('dd=')[1].split('\t')[0]
				enfermedad =  enfermedadCompleta[:3]
				subenfermedad = enfermedadCompleta[3:]
				if subenfermedad != "" and subenfermedad != "0":
					enfermedadCompleta = enfermedad + '.' + subenfermedad
				else:
					enfermedadCompleta = enfermedad

				if enfermedadCompleta not in lEnfermedades:
					lEnfermedades.append(enfermedadCompleta)

		return lEnfermedades
	 
	@classmethod          
	def GenerarListaConValoresPrediccionEnfermedades(var, lEnfermedadesPaciente, lEnfermedades):
		lAux = list()
		for enfermedad in lEnfermedades:
			if enfermedad in lEnfermedadesPaciente:
				lAux.append(1)
			else:
				lAux.append(0)

		return lAux

	@classmethod
	def ObtenerSexoEdad(var):

		directorio = "datosGenerales.csv"

		DIR_DATOS_GENERALES = os.path.join(os.path.dirname(os.path.realpath(__file__)), directorio)
		file = open(DIR_DATOS_GENERALES,"r+")

		reader_file = csv.reader(file)

		dPacientesEdad = dict()

		for line in reader_file:
			if line[0] not in "Paciente":
				dPacientesEdad[line[0]] = line[1] + "-" + line[2] + "-" + line[3]

		return dPacientesEdad

	@classmethod
	def GenerarListaConClavesDeEnfermedadesParaPrediccion(var):
	    directorio = 'CIE9MC.csv'
	    
	    DIR_PATIENTS_LIST = os.path.join(os.path.dirname(os.path.realpath(__file__)), directorio)
	    file = open(DIR_PATIENTS_LIST, "r+")

	    reader_file = csv.reader(file)
	    lista = list()
	    
	    for datos in reader_file:
	        if datos[0] != "":
	            lista.append(datos[0])
	    
	    return lista

	@classmethod
	def main(var, pacienteObjetivo):
		i=0
		enfermos = []
		for dirname, dirnames, filenames in os.walk(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'dataset')):
			if len(dirnames) != 0:
				enfermos = dirnames

		numeroPacientes =  len(enfermos) / 3

		aciertos = 0;
		numeroTotal = 0

		threads = list()

		dPacientesSexoEdad = Predecir_Episodio.ObtenerSexoEdad()

		listaClavesEnfermedades = Predecir_Episodio.GenerarListaConClavesDeEnfermedadesParaPrediccion()

		lOtrosPacientes = list();

		numeroInicio=0;
		fin = numeroPacientes;
		for i in range(3):
			lPaciente = list()
		    
			for i in range(numeroInicio, fin):
				if enfermos[i] != pacienteObjetivo:
					lPaciente.append(enfermos[i])

			t = threading.Thread(target=Predecir_Episodio.generarListasHilos, args=(lPaciente, lOtrosPacientes, dPacientesSexoEdad, listaClavesEnfermedades));
			threads.append(t);
		    
			t.start()
		    
			numeroInicio = fin
			if(i == 2):
				fin = len(enfermos)
			else:
				fin += numeroPacientes
		    
		for i in threads:
			i.join()
		    
		print "Empieza la prediccion"

		input_data = lOtrosPacientes

		pr = Perceptron(22216,0.1)
		weights = []
		errors = []

		pacienteParaPredecir = list();

		pacienteParaPredecir.append(1);

		pacienteParaPredecir.extend(Predecir_Episodio.generarListasHilo(pacienteObjetivo, dPacientesSexoEdad, listaClavesEnfermedades, True))

		for _ in range(300):
			for person in input_data:
				output = person[-1]
				inp = [1] + person[0:-1]
				weights.append(pr._w)
				err = pr.train(inp,output)
				errors.append(err)

		print "Se va a predecir el paciente objetivo"
		
		if pr.predict(pacienteParaPredecir) == 1: 
			return 1       
		else:
			return 0

class Buscador_Pacientes_Similares:

	@classmethod
	def ObtenerPacientesSimilares(var, listaPacientes, sexoSeleccionado, edadSeleccionado, sufreEpisodioSeleccionado, dPacientesSimilares, sexoPeso, edadPeso, usarEdad, usarSexo):
		for paciente in listaPacientes:
			sexo, edad, sufreEpisodio = Buscador_Pacientes_Similares.GenerarDatosPaciente(paciente[1])
			if edad < 10:
				rangoInferior = 0
			else:
				rangoInferior = edadSeleccionado - 10

			rangoSuperior = edadSeleccionado + 10

			if usarSexo:
				if sexo == sexoSeleccionado:
					dPacientesSimilares[paciente[0]] = sexoPeso
			else:
				dPacientesSimilares[paciente[0]] = 0

			if usarEdad:
				if rangoInferior < edad < rangoSuperior:
					if paciente[0] in dPacientesSimilares.keys():
						pesos = dPacientesSimilares[paciente[0]]
						pesos += (10 - abs(edadSeleccionado - edad)) * edadPeso
						dPacientesSimilares[paciente[0]] = pesos
				elif paciente[0] in dPacientesSimilares.keys():
					del dPacientesSimilares[paciente[0]]


	@classmethod
	def GenerarDatosPaciente(var, pacienteSeleccionado):
	    sexoPacienteSeleccionado = pacienteSeleccionado.split("-")[0]
	    edadPacienteSeleccionado = pacienteSeleccionado.split("-")[1]
	    
	    if(edadPacienteSeleccionado == '90+'):
	        edadPacienteSeleccionado = '90'
	        
	    edadPacienteSeleccionado = int(float(edadPacienteSeleccionado))
	    
	    sufreEpisodioPacienteSeleccionado = pacienteSeleccionado.split("-")[2]
	    
	    return sexoPacienteSeleccionado, edadPacienteSeleccionado, sufreEpisodioPacienteSeleccionado


	@classmethod
	def ObtenerEnfermedadesPaciente(var, enfermo):
	    direccion_paciente = "dataset/" + enfermo + "/" + enfermo + ".txt"
	    
	    DIR_PATIENTS_LIST = os.path.join(os.path.dirname(os.path.realpath(__file__)), direccion_paciente)
	    
	    file = open(DIR_PATIENTS_LIST)
	    
	    lista, diccionario = Generar_Formulario.ObtenerEnfermedades(file)

	    return lista


	@classmethod
	def GenerarCabecera(var, pacienteObjetivo, lPacientesSimilares, dPacientesSexoEdad):
		cabecera = '<table id="tabla_enfermedades_similares"> <thead> <tr> <th id="cabeceraEnfermedades"> Enfermedades <img id="arrowTurn" src="../static/imagen/arrow.png"> </th>'
		inforPacientes = '<tr id="filaDatosPaciente"> <td> Datos de los pacientes </td>'
	     
		for enfermo in lPacientesSimilares:
			sexo, edad, sufre = Buscador_Pacientes_Similares.GenerarDatosPaciente(dPacientesSexoEdad[enfermo])
			if sexo == "M":
				sexo = "Hombre"
			else:
				sexo = "Mujer"

			print sufre

			if sufre == '1':
				sufre = "Sufre episodio"
			else:
				sufre = "No sufre episodio"

			inforPacientes += "<td>" + sexo + " (" + str(edad) + ") <br/>" + sufre + "</td>"
			cabecera += '<th>' + enfermo + '</th>'

		cabecera += '</thead> </tr>'
	    
		inforPacientes += '</tr>'

		return cabecera + inforPacientes

	@classmethod
	def generarVista(var, pacienteObjetivo, lEnfermedadesPacienteObjetivo, lPacientesSimilares, dPacienteEnfermedades, dPacientesSexoEdad, usarEnfermedades):
	    codigoHTML = Buscador_Pacientes_Similares.GenerarCabecera(pacienteObjetivo, lPacientesSimilares, dPacientesSexoEdad)
	    if usarEnfermedades:
		    for enfermedad in lEnfermedadesPacienteObjetivo:
		        codigoHTML += '<tr>'
		        codigoHTML += '<td id="' + enfermedad + '"class="idEnfermedad">' + enfermedad + '</td>'
		        for enfermo in lPacientesSimilares: 
		            if enfermedad in dPacienteEnfermedades[enfermo]:
		                codigoHTML += '<td> <img class="imgTick" src="../static/imagen/tick.png"></img> </td>'
		            else:
		                codigoHTML += '<td> - </td>'
		        codigoHTML += '</tr>'
	    codigoHTML += '</table>'  
	    
	    return codigoHTML

	@classmethod
	def ObtenerNumeroEnfermedadesComunes(var, lEnfermedadesPacienteObjetivo, enfermedades):
	    enfermedadesComunes = 0
	    for enfermedadPacienteObjetivo in lEnfermedadesPacienteObjetivo:
	        if enfermedadPacienteObjetivo in enfermedades:
	            enfermedadesComunes += 1
	            
	    return enfermedadesComunes

	@classmethod
	def main(var, pacienteObjetivo, usarEdad, usarSexo, usarEnfermedades, sexoPeso, edadPeso, enfermedadPeso):
		sexoPeso = float(sexoPeso)
		edadPeso = float(edadPeso)
		enfermedadPeso = float(enfermedadPeso)

		threads = list()

		dPacientesSimilares = dict()

		lPacientesSimilares = list()

		numeroHilos = 3

		dPacientesSexoEdad = Predecir_Episodio.ObtenerSexoEdad()

		pacienteSeleccionado = dPacientesSexoEdad[pacienteObjetivo]

		sexo, edad, sufreEpisodio = Buscador_Pacientes_Similares.GenerarDatosPaciente(pacienteSeleccionado)

		del dPacientesSexoEdad[pacienteObjetivo]

		numeroPacientesPorHilo = len(dPacientesSexoEdad)/ 3

		inicio = 0
		fin = numeroPacientesPorHilo

		iterador = dPacientesSexoEdad.iteritems()

		for i in range(numeroHilos):
		    listaPorHilo = list()
		    
		    listaPorHilo = list(islice(iterador, fin))
		    
		    t = threading.Thread(target=Buscador_Pacientes_Similares.ObtenerPacientesSimilares, args=(listaPorHilo, sexo, edad, sufreEpisodio, dPacientesSimilares, sexoPeso, edadPeso, usarEdad, usarSexo));
		    threads.append(t);
		    
		    t.start()
		        
		    if(i == numeroHilos - 2):
		        fin = len(dPacientesSexoEdad)
		        
		    for i in threads:
		        i.join()

		lEnfermedadesPacienteObjetivo = Buscador_Pacientes_Similares.ObtenerEnfermedadesPaciente(pacienteObjetivo)

		dPacienteEnfermedades = dict()

		for enfermo, peso in dPacientesSimilares.items():
			enfermedades = Buscador_Pacientes_Similares.ObtenerEnfermedadesPaciente(enfermo)
			numeroEnfermedadesComunes = Buscador_Pacientes_Similares.ObtenerNumeroEnfermedadesComunes(lEnfermedadesPacienteObjetivo, enfermedades)
			if usarEnfermedades:
				dPacientesSimilares[enfermo] = dPacientesSimilares[enfermo] + numeroEnfermedadesComunes * enfermedadPeso
				dPacienteEnfermedades[enfermo] = enfermedades

		lTupla = dPacientesSimilares.items()

		lTupla.sort(key=lambda x: x[1], reverse = True)

		for paciente in lTupla:
		    lPacientesSimilares.append(paciente[0])

		codigoHTML = Buscador_Pacientes_Similares.generarVista(pacienteObjetivo, lEnfermedadesPacienteObjetivo, lPacientesSimilares, dPacienteEnfermedades, dPacientesSexoEdad, usarEnfermedades)

		return codigoHTML

class HistoricoPacientes:

	@classmethod
	def ObtenerSexoEdad(var):

		directorio = "datosGenerales.csv"

		DIR_DATOS_GENERALES = os.path.join(os.path.dirname(os.path.realpath(__file__)), directorio)
		file = open(DIR_DATOS_GENERALES,"r+")

		reader_file = csv.reader(file)
	
		dPacientesEdad = dict()

		for line in reader_file:
			if line[0] not in "Paciente":
				dPacientesEdad[line[0]] = line[1] + "-" + line[2] + "-" + line[3]

		return dPacientesEdad

	@classmethod
	def GenerarTabla(var, dGeneracionTabla):
		TablaGrafico = '<table id="datosNumericos">'
		TablaPaciente = '<table id="datosPacientes">'
		Tabla = '<thead>'
		Tabla += '<tr>'
		Tabla += '<th></th>'
		Tabla += '<th>Sufre Episodio</th>'
		Tabla += '<th>No Sufre Episodio</th>'
		Tabla += '</tr>'
		Tabla += '</thead>'
		Tabla += '<tbody>'

		TablaGrafico += Tabla
		TablaPaciente += Tabla

		for clave, tupla in dGeneracionTabla.items():
			enfermosSufren = ""
			enfermosNoSufren = ""
			TablaGrafico += '<tr>'
			TablaGrafico += '<th>' + str(clave) + '</th>'
			TablaGrafico += '<td>' + str(len(tupla[0])) + '</td>'
			TablaGrafico += '<td>' + str(len(tupla[1])) + '</td>'
			TablaGrafico += '</tr>'

			for enfermo in tupla[0]:
				enfermosSufren += "<p class='enfermo'>" + enfermo + "</p> "

			for enfermo in tupla[1]:
				enfermosNoSufren += "<p class='enfermo'>" + enfermo + "</p> "

			TablaPaciente += '<tr>'
			TablaPaciente += '<th>' + str(clave) + '</th>'
			TablaPaciente += '<td>' + enfermosSufren + '</td>'
			TablaPaciente += '<td>' + enfermosNoSufren + '</td>'
			TablaPaciente += '</tr>'

		TablaGrafico += '</tbody>'
		TablaGrafico += '</table>'

		TablaPaciente += '</tbody>'
		TablaPaciente += '</table>'

		return TablaGrafico, TablaPaciente

	@classmethod
	def FuncionPrincipal(var):
		dFechasRepeticiones = dict()

		for dirname, dirnames, filenames in os.walk(os.path.join(os.path.dirname(os.path.realpath(__file__)), 'dataset')):
			if len(dirnames) != 0:
				enfermos = dirnames
			for enfermo in enfermos:
				directorio = 'dataset/' +enfermo + '/' + enfermo + '.csv'

				lEnfermos = []

				DIR_DATOS_GENERALES = os.path.join(os.path.dirname(os.path.realpath(__file__)), directorio)
				file = open(DIR_DATOS_GENERALES,"r+")

				reader_file = csv.reader(file)

				cabecera = next(reader_file)
				primeraLinea = next(reader_file)

				fecha =  datetime.strptime(primeraLinea[0].split(" ")[0], '%d/%m/%Y')

				fecha = fecha.year 

				if fecha in dFechasRepeticiones.keys():
					lEnfermosValor = dFechasRepeticiones[fecha]
					lEnfermosValor.append(enfermo)
					dFechasRepeticiones[fecha] = lEnfermosValor
				else:
					lEnfermos.append(enfermo)
					dFechasRepeticiones[fecha] = lEnfermos
			break

		dPacienteSexoEdadEpisodio = HistoricoPacientes.ObtenerSexoEdad()
		dGeneracionTabla = dict()

		for clave in dFechasRepeticiones.keys():
			sufre = list()
			noSufre = list()
			for paciente in dFechasRepeticiones[clave]:
				if dPacienteSexoEdadEpisodio[paciente].split("-")[2] == "1":
					sufre.append(paciente)
				else:
					noSufre.append(paciente)

			dGeneracionTabla[clave] = (sufre, noSufre)

		resultado = sorted(dGeneracionTabla.items(), key=operator.itemgetter(0))

		codigoGrafica, codigoPacientes = HistoricoPacientes.GenerarTabla(dGeneracionTabla)

		return codigoGrafica, codigoPacientes  