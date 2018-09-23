{% load static %}

<!DOCTYPE HTML>
<html>

<head>
	{% load static %}

	<title>TFM</title> 	
	
	<script src="{% static 'js/jquery-3.2.1.slim.min.js' %}"></script>
	<script src="{% static 'js/popper.min.js' %}"></script>
	<script src="{% static 'js/bootstrap.js' %}"></script>
	
	<script src="{% static 'js/jquery-3.3.1.js' %}"></script>
	<script src="{% static 'js/jquery-ui.js' %}"></script>
	<script src="{% static 'js/js.cookie.js' %}"></script>	
	<script src="{% static 'js/i18n/datepicker-es.js' %}"></script>	
	<script src="{% static 'DataTables/datatables.js' %}"></script>
	<script src="{% static 'js/jQueryRotate.js' %}"></script>
	
	<link rel="stylesheet" type="text/css" href="{% static 'css/bootstrap.min.css' %}" >	
	<link rel="stylesheet" type="text/css" href="{% static 'DataTables/datatables.css' %}">
	<link rel="stylesheet" type="text/css" href="{% static 'css/jquery-ui.css' %}">
	<link rel="stylesheet" type="text/css" href="{% static 'css/myStyle.css' %}">
	
	
	<script src="{% static 'js/highstock.js' %}"></script>
	<script src="{% static 'js/exporting.js' %}"></script>
	<script src="{% static 'js/data.js' %}"></script>
	<script src="{% static 'js/export-data.js' %}"></script>
	
	<script>
		$(function(){
	  		var availableTags;
			$.ajax({
				method: 'POST',
				url : '/dame_pacientes/',
				dataType:'json',
				success: function(response){
					availableTags = response.resultado;
					$("#NombrePacienteValor").autocomplete({
						source: availableTags
					});
					$("#NombrePacienteValor").autocomplete({
						autoFocus: true
					});
					$("#NombrePacienteValorConfiguracion").autocomplete({
						source: availableTags
					});
				},
				error : function(xhr, status) {
  					alert('Se ha producido un error al cargar la página');
    			}
			});
		});
		
		$(function(){
	  		var availableTags;
			$.ajax({
				method: 'POST',
				url : '/historicoPacientes/',
				dataType:'json',
				success:function(response){
					$("#tablaGrafica").empty();
					$("#tablaGrafica").append(response.grafica);
					$("#tablaPacientes").empty();
					$("#tablaPacientes").append(response.enfermos);
					generarGraficaHistorico();
				}
			});
		});
		
		$( function() {
			$( "#datepicker" ).datepicker($.datepicker.regional[ "es" ]);
		});
		
		$( function() {
			var valor;
			$( "#slider-edad" ).slider({
				slide: function( event, ui ) {
					$( "#amount-edad" ).val( ui.value );
					valor = ui.value;
					if(valor == 100){
						$("#slider-edad").trigger("mouseup")
					}
				}
			});
			$( "#amount-edad" ).on( "keyup", function() {
				if(this.value > 100){
					this.value = 100
				}
				else if(this.value < 0){
					this.value = 0
				}
				valor = this.value
				$( "#slider-edad" ).slider( "value", this.value );
				$("#slider-edad").trigger("mouseup")
			});
			$( "#amount-edad" ).on( "change", function() {
				$( "#slider-edad" ).slider( "value", this.value );
			});
			
			$("#slider-edad").on("mouseup", function(){
				Cookies.set('edad',valor, { expires: 1});
				$("#pacienteSimilar").trigger("click");
			})
		} );
		
		$( function() {
			var valor;
			$( "#slider-sexo" ).slider({
				slide: function( event, ui ) {
					$( "#amount-sexo" ).val( ui.value );
					valor = ui.value;
					if(valor == 100){
						$("#slider-sexo").trigger("mouseup")
					}
				}
			});
			$( "#amount-sexo" ).on( "keyup", function() {
				if(this.value > 100){
					this.value = 100
				}
				else if(this.value < 0){
					this.value = 0
				}
				valor = this.value
				$( "#slider-sexo" ).slider( "value", this.value );
				$("#slider-sexo").trigger("mouseup")
			});
			$( "#amount-sexo" ).on( "change", function() {
				$( "#slider-sexo" ).slider( "value", this.value );
			});
			
			$("#slider-sexo").on("mouseup", function(){
				Cookies.set('sexo',valor, { expires: 1});
				$("#pacienteSimilar").trigger("click");
			})
		} );
		
		$( function() {
			var valor;
			$( "#slider-enfermedades" ).slider({
				slide: function( event, ui ) {
					$( "#amount-enfermedades" ).val( ui.value );
					valor = ui.value;
					if(valor == 100){
						$("#slider-enfermedades").trigger("mouseup")
					}
				}
			});
			$( "#amount-enfermedades" ).on( "keyup", function() {
				if(this.value > 100){
					this.value = 100
				}
				else if(this.value < 0){
					this.value = 0
				}
				valor = this.value
				$( "#slider-enfermedades" ).slider( "value", this.value );
				$("#slider-enfermedades").trigger("mouseup")
			});
			$( "#amount-enfermedades" ).on( "change", function() {
				$( "#slider-enfermedades" ).slider( "value", this.value );
			});
			$("#slider-enfermedades").on("mouseup", function(){
				Cookies.set('enfermedad',valor, { expires: 1});
				$("#pacienteSimilar").trigger("click");
			})
		} );
		
		$(function(){
			$("#cargando").hide();
			$(".btn-predecir").prop("disabled", "disabled");
			$("#pacienteSimilar").prop("disabled", "disabled");
			$("#ocultar").hide();
			$(".slider-cbr").slider("disable");
			$(".input-slider").prop("disabled", "disabled");
		});
		
		$(function(){
			$("#dialog").dialog({
				modal: true,
				autoOpen: false,
				draggable: false,
				resizable: true,
				buttons: {
					Aceptar: function() {
						$( this ).dialog( "close" );
					}
				},
				hide: {
					effect: "fade",
					duration: 300
				}
			});

		});
		
		function generarGraficaHistorico(){
			Highcharts.chart('containerHistoricoPaciente', {
				data: {
					table: 'datosNumericos'
				},
				credits: {
					enabled: false
				},
				chart: {
					type: 'column'
				},
				title: {
					text: 'Histórico de los pacientes'
				},
				yAxis: {
					allowDecimals: false,
					title: {
					text: 'Nº de pacientes'
					}
				},
				tooltip: {
					formatter: function () {
						return '<b>' + this.series.name + '</b><br/>' +
						this.point.y + ' en ' + this.key;
					}
				}
			});
		}
		
	</script>
	
</head>
    
<body>
	<div class="container">
		<ul class="nav">
			<li class="nav-item">
				<a class="nav-link active" id="home-tab" data-toggle="tab" href="#home" role"tab">HIPOTENS</a>
			</li>
			<li class="nav-item">
				<a class="nav-link" id="otro-tab" data-toggle="tab" href="#otro" role"tab">Pacientes similares</a>
			</li>
			<li class="nav-item">
				<a class="nav-link"  id="historico-tab" data-toggle="tab" href="#historico" role"tab">Histórico</a>
			</li>
		</ul>
		<div class="tab-content" id="myTabContent">
			<div class="tab-pane fade show active" id="home" role="tabpanel" aria-labelledby="home-tab">
				<div class="row">
					<div class="col-md-2">
						<div class="row row-img">
							<div class="ImagenSegunSexo col-md-12">
								<img class="ImagenSegunSexoImg" src="{% static "imagen/Mujer.png" %}">
							</div>
						</div>
						<div class ="row">
							<div class = "col-md-12">
								<button type="button" class="btn btn-lg btn-block btn-predecir">Predecir</button>
							</div>
						</div>
					</div>
					<div class="col-md-3">
						<div class="row">
							<div class="col-md-12 btn-sexo">
								<label for="SexoPaciente" class="titulo label-sexo">Sexo</label>
								<div class="btn-group grupo-sexo" role="group" aria-label="Basic example">
									<button type="button" class="btn" id="hombre">Hombre</button>
									<button type="button" class="btn" id="mujer">Mujer</button>
								</div>							
							</div>
						</div>
						<div class="row">
							<div class="col-md-12">
								<div class="form-group input-nombre-paciente">
									<label for="NombrePaciente" class="titulo">Identificacion del paciente</label>
									<div class="input-group">
										<input type="text" class="form-control" id="NombrePacienteValor" aria-describedby="Nº Paciente" placeholder="Seleccione un paciente">
									</div>
								</div>
							</div>
						</div>
						<div class="row">
							<div class="col-md-12">
								<div class="form-group input-fecha-edad-paciente">
									<label for="FechaIngreso" class="titulo">Fecha de ingreso</label>
									<div class="input-group">
										<input type="text" class="form-control" id="datepicker">
									</div>	
								</div>
							</div>
						</div>
						<div class="row">
							<div class="col-md-12">
								<div class="form-group input-fecha-edad-paciente">
									<label for="FechaIngreso" class="titulo">Edad del paciente</label>
									<div class="input-group">
										<input type="text" class="form-control" id="edadPaciente">
									</div>	
								</div>
							</div>
						</div>
					</div>						
					<div class="col-md-7">
						<table id="table_id" class="display">
							
						</table>
					</div>
				</div>
				<div class="row">
					<div id="grafica" class="col-md-12">
					</div>
				</div>
				<div id="ocultar">
				</div>
				<div id = "cargando">
					<p id="texto_modal">  </p>
					<img id="imagenCargando" src="{% static 'imagen/loading.gif' %}"/>

				</div>

				<div id="dialog" title="Resultado de la predicción">
					<p id="resultado_prediccion"></p>
				</div>
			</div>
			<div class="tab-pane fade" id="otro" role="tabpanel" aria-labelledby="otro-tab">
				<div class="row">
					<div class="col-md-4" id="parteIzquierda">
						<div id="pacienteConfiguracion">
							<div class="form-group">
								<label for="NombrePaciente" class="titulo">Identificacion del paciente</label>
								<div class="input-group">
									<input type="text" class="form-control" id="NombrePacienteValorConfiguracion" aria-describedby="Nº Paciente" placeholder="Introduzca el numero del paciente">
								</div>
							</div>
						</div>
						<div class="row">
							<div class = "col-md-6">
								<div class="form-group">
									<label class="titulo" for="SexoPaciente">Sexo</label>
									<input type="text" class="form-control" id="SexoPacienteInput">
								</div>
							</div>
							<div class = "col-md-6">
								<div class="form-group">
									<label class="titulo" for="EdadPaciente">Edad</label>
									<input type="text" class="form-control" id="EdadPacienteInput">
								</div>
							</div>
						</div>
						<div class="row">
							<div class="col-md-12">
								<div class="form-group">
									<label class="titulo" for="exampleFormControlSelect1">Enfermedades</label>
									<select class="form-control" id="exampleFormControlSelect1">
										
									</select>
								</div>
							</div>
						</div>
						<div class="row">
							<div class = "col-md-12">
								<div class="card">
									<div class="card-body">
										<div class="row">
											<div class = "col-md-2">
												<img class="ImagenExclamacion" src="{% static "imagen/exclamacion.png" %}">
											</div>
											<div class="col-md-10">
												Pulsar "SI" para añadir una elemento en la búsqueda e indicar el grado de importancia.
											</div>
										</div>
									</div>
								</div>
							</div>
						</div>
						<div id="sliderConfiguracion">
							<p>
								<div class="row">
									<div class="col-md-8">
										<label for="amount-edad" class="titulo">Edad:</label>
										<input type="number" class="input-slider" id="amount-edad" max="100" min="0" value="1" style="border:0; color:#f6931f; font-weight:bold; width: 35%; background-color: #f8f8f8; color: #595959">
									</div>
									<div class="col-md-4 botoneraConfig">
										<div class="btn-group btn-group-toggle" data-toggle="buttons">
											<label class="btn btn-secondary buttonSi" target="slider-edad">
												<input type="radio" name="options" id="option1" autocomplete="off"> Si
											</label>
											<label class="btn btn-secondary active  buttonNo" target="slider-edad">
												<input type="radio" name="options" id="option2" autocomplete="off" checked> No
											</label>
										</div>
									</div>
								</div>
							</p>
							<div id="slider-edad" class="slider-cbr"></div>

							<p>
								<div class="row">
									<div class="col-md-8">
										<label for="amount-sexo" class="titulo">Sexo:</label>
										<input type="number" class="input-slider" id="amount-sexo" max="100" min="0" value="1" style="border:0; color:#f6931f; font-weight:bold; width: 35%; background-color: #f8f8f8; color: #595959">
									</div>
									<div class="col-md-4 botoneraConfig">
										<div class="btn-group btn-group-toggle" data-toggle="buttons">
											<label class="btn btn-secondary buttonSi" target="slider-sexo">
												<input type="radio" name="options" id="option1" autocomplete="off"> Si
											</label>
											<label class="btn btn-secondary active  buttonNo" target="slider-sexo">
												<input type="radio" name="options" id="option2" autocomplete="off" checked> No
											</label>
										</div>
									</div>
									
								</div>
							</p>
							<div id="slider-sexo" class="slider-cbr"></div>

							<p>
								<div class="row">
									<div class="col-md-8">
										<label for="amount-enfermedades" class="titulo">Enfermedad:</label>
										<input type="number" class="input-slider" id="amount-enfermedades" max="100" min="0" value="1" style="border:0; color:#f6931f; font-weight:bold; width: 35%; background-color: #f8f8f8; color: #595959">
									</div>
									<div class="col-md-4 botoneraConfig">
										<div class="btn-group btn-group-toggle" data-toggle="buttons">
											<label class="btn btn-secondary buttonSi" target="slider-enfermedades">
												<input type="radio" name="options" id="option1"  autocomplete="off"> Si
											</label>
											<label class="btn btn-secondary active buttonNo" target="slider-enfermedades">
												<input type="radio" name="options" id="option2" autocomplete="off" checked> No
											</label>
										</div>
									</div>
									
								</div>
							</p>
							<div id="slider-enfermedades" class="slider-cbr"></div>	
						</div>
						<div class="row">
							<div class="col-md-12">
								<button type="button" class="btn btn-primary btn-lg btn-block" id="pacienteSimilar">Buscar paciente similar</button>
							</div>
						</div>
					</div>
					<div class="col-md-8">
						<div id="parteDerecha">
						
						</div>
					</div>
				</div>
			</div>					
			<div class="tab-pane fade" id="historico" role="tabpanel" aria-labelledby="profile-tab">
				<div id="containerHistoricoPaciente" style="min-width: 310px; height: 400px; margin: 0 auto"></div>
				<div id="tablaGrafica" style="display: none"></div>
				<div id="tablaPacientes"></div>
			</div>
		</div>
	</div>
</body>

<script>
	var paciente;
	var pacienteConfiguracion;
	var activo = false;
	
	var rotacion = 0;

	$(document).ready(function() {
		$('#hombre').click(function() {
			var ruta = $(".ImagenSegunSexoImg").attr("src");
			ruta = ruta.replace("Mujer", "Hombre");
			$("#mujer").css("background-color", "#E6E6E6");
			$("#hombre").css("background-color", "#5699E5");
			$(".ImagenSegunSexoImg").attr("src",ruta);
			aplicarFiltroSexo("M");
			
		});
		
		$('#mujer').click(function() {
			var ruta = $(".ImagenSegunSexoImg").attr("src");
			ruta = ruta.replace("Hombre", "Mujer");
			$("#hombre").css("background-color", "#E6E6E6");
			$("#mujer").css("background-color", "#5699E5");
			$(".ImagenSegunSexoImg").attr("src",ruta);
			aplicarFiltroSexo("F")
		});
		
		if(Cookies.get("sexo") !== undefined){                                         
			$( "#slider-sexo" ).slider( "value", Cookies.get("sexo"));
			$( "#amount-sexo" ).val(Cookies.get("sexo"));
		}
		
		if(Cookies.get("edad") !== undefined){
			$( "#slider-edad" ).slider( "value", Cookies.get("edad"));
			$( "#amount-edad" ).val(Cookies.get("edad"));
		}
		
		if(Cookies.get("enfermedad") !== undefined){
			$( "#slider-enfermedades" ).slider( "value", Cookies.get("enfermedad"));
			$( "#amount-enfermedades" ).val(Cookies.get("enfermedad"));
		}
		
		$(".buttonNo").trigger("click")
	});
		
	function aplicarFiltroSexo(sexoFiltro){
		var availableTags;
			$.ajax({
				method: 'POST',
				url : '/dame_pacientes_con_filtro/',
				data:{sexo:sexoFiltro},
				dataType:'json',
				success: function(response){
					availableTags = response.resultado;
					$("#NombrePacienteValor").autocomplete({
						source: availableTags
					});
				}
			});
	};
	
	$( "#NombrePacienteValor").autocomplete({
		select: function(event, ui){
			var elemento = ui.item.value
			paciente = elemento
			$.ajax({
				method: 'POST',
				url : '/dame_paciente_formulario/',
				data:{paciente:elemento},
				dataType:'json',
				beforeSend: function(){
					$("#texto_modal").text("Se está cargando la información del paciente seleccionado");
					$("#cargando").show();
					$("#grafica").hide();
					$("input").prop('disabled', true);
					$(".btn-predecir").prop("disabled", true);
				},
				success: function(response){
					fecha = response.fechaIngreso
					fechaSeparada = fecha.split("-")
					fechaNueva = fechaSeparada[2] + "/" + fechaSeparada[1] + "/" + fechaSeparada[0]
					datepicker.value = fechaNueva
					generarGrafica(response.valores, elemento)
					edadPaciente.value = response.edad
					cambiarSexoImagen(response.sexo)
					generarListaEnfermedades(response.tablaEnfermedades	)
					$(".btn-predecir").prop("disabled", "");
				},
				complete: function(){
					$("#grafica").show();
					$("#cargando").hide();
					$("#NombrePacienteValor").prop('disabled', false);
					$("#NombrePacienteValorConfiguracion").prop('disabled', false);
					$("#checkPesosInput").prop('disabled', false);
				}
			});
		}
	});
	
	function cambiarSexoImagen(sexoPaciente){
		var ruta = $(".ImagenSegunSexoImg").attr("src");
		if(sexoPaciente == 'M'){
			var ruta = $(".ImagenSegunSexoImg").attr("src");
			ruta = ruta.replace("Mujer", "Hombre");
			$("#mujer").css("background-color", "#E6E6E6");
			$("#hombre").css("background-color", "#5699E5");
			$(".ImagenSegunSexoImg").attr("src",ruta);
		}	
		else if(sexoPaciente == 'F'){
			var ruta = $(".ImagenSegunSexoImg").attr("src");
			ruta = ruta.replace("Hombre", "Mujer");
			$("#hombre").css("background-color", "#E6E6E6");
			$("#mujer").css("background-color", "#5699E5");
			$(".ImagenSegunSexoImg").attr("src",ruta);
		}
	};
	
	function generarGrafica(valores, paciente){
		Highcharts.stockChart('grafica', {
			rangeSelector: {
				enabled: false
			},
			credits: {
				enabled: false
			},
			title: {
				text: 'Datos del paciente ' + paciente
			},
			exporting: {
				enabled: false
			},
			plotOptions: {
				series: {
					cursor: 'pointer',
					point: {
						events: {
							click: function (e) {
								alert(e.point.x)
							}
						}
					},
					marker: {
						lineWidth: 1
					}
				}
			},
			series: [{
				name: 'AAPL',
				data: valores,
				tooltip: {
					valueDecimals: 1
				}
			}]
		}); 
	};
	
	function generarListaEnfermedades(tablaEnfermedades){
		$("#table_id").empty();
		$("#table_id").append(tablaEnfermedades);
		
		$.extend( $.fn.dataTable.defaults, {
			searching: false,
			"pageLength": 6,
			"bLengthChange": false
		} );
		
		$('#table_id').DataTable({
			destroy: true,
			"order": [[ 0]],
			"language": {
				"lengthMenu": "Mostrar _MENU_ enfermedades por página",
				"info": "Página _PAGE_ de _PAGES_",
				"infoEmpty": "No hay información disponible",
				"paginate": {
					"first":      "Primera",
					"last":       "Última",
					"next":       "Siguiente",
					"previous":   "Anterior"
				}
			}
		});
	};
	
	$(".btn-predecir").click(function(){
		$.ajax({
			method: 'POST',
			url : '/predecir/',
			data:{paciente:paciente},
			dataType:'json',
			beforeSend: function(){
				$("#texto_modal").css("color", "white");
				$("#texto_modal").text("Se está llevando a cabo la predicción, este proceso puede durar varios minutos")
				$(".highcharts-title").remove();
				$("#ocultar").show();
				$("#cargando").show();
				$("input").prop('disabled', true);
				$(".btn_prediccion").prop("disabled", "disabled");
			},
			success: function(response){
				var texto = "";
				if(response.resultado){
					texto = "Atención: el paciente SI va a sufrir un episodio de hipotensión";
				}
				else{
					texto = "El paciente NO va a sufrir un episodio de hipotensión";
				}
				$("#resultado_prediccion").text(texto);
				$( "#dialog" ).dialog( "open" );
				$("#resultado_prediccion").css("font-weight","Bold");
			},
			complete: function(){
				$("#texto_modal").css("color", "black");
				$("#ocultar").hide();
				$("#cargando").hide();
				$("#NombrePacienteValor").prop('disabled', false);
				$( "#accordion" ).accordion( "option", "active", true);
				$(".btn_prediccion").prop("disabled", "");
				$("#NombrePacienteValorConfiguracion").prop('disabled', false);
				$("#checkPesosInput").prop('disabled', false);
			}
		});
	});
	
	$( "#NombrePacienteValorConfiguracion" ).autocomplete({
		select: function(event, ui){
			var elemento = ui.item.value
			pacienteConfiguracion = elemento
			$("#pacienteSimilar").prop("disabled", "");
			
			$.ajax({
				method: 'POST',
				url : '/dame_paciente_formulario/',
				data:{paciente:elemento},
				dataType:'json',
				success: function(response){
					EdadPacienteInput.value = response.edad
					generarDesplegableEnfermedades(response.listaEnfermedades)
					if(response.sexo == "M"){
						SexoPacienteInput.value = "Hombre"
					}
					else{
						SexoPacienteInput.value = "Mujer"
					}
				},
				complete: function(){
					$("#grafica").show();
					$("#cargando").hide();
					$("#NombrePacienteValor").prop('disabled', false);
					$("#NombrePacienteValorConfiguracion").prop('disabled', false);
					$("#checkPesosInput").prop('disabled', false);
				}
			});
		}
	});
	
	$("#pacienteSimilar").click(function(){
		var emplearSexo = false;
		var sexo = 0;
		var emplearEdad = false;
		var edad = 0;
		var emplearEnfermedades = false;
		var enfermedades = 0;
		
		$(".buttonSi.active").each(function(){
			var objetivo = $(this).attr("target").split("-")[1]
			
			switch(objetivo){
				case "edad":
					emplearEdad = true;
					edad = $("#amount-edad").val()/100;
					break;
				case "sexo":
					emplearSexo = true;
					sexo = $("#amount-sexo").val()/100;
					break;
				case "enfermedades":
					emplearEnfermedades = true;
					enfermedades = $("#amount-enfermedades").val()/100;
			}
		})
		$.ajax({
			method: 'POST',
			url : '/buscarSimilar/',
			data:{paciente:pacienteConfiguracion,
				  usarEdad: emplearEdad,
				  edad: edad,
				  usarSexo: emplearSexo,
				  sexo: sexo,
				  usarEnfermedades: emplearEnfermedades,
				  enfermedades: enfermedades},
			dataType:'json',
			success: function(response){
				tablaGenerada = response.resultado
				$("#parteDerecha").empty();
				$("#parteDerecha").append(tablaGenerada);
			}
		});
	});
		
	$(document).on('click', '.buttonNo', function () {
		$(this).addClass("active")
		var objetivo = $(this).attr("target")
		$('#'+objetivo).slider("disable")
		objetivo = objetivo.split("-")[1]
		$('#amount-' + objetivo).prop('disabled', true);
		$('#'+objetivo).slider("value", 100);
		$('#amount-' + objetivo).val(100);
		$('#amount-' + objetivo).trigger("change")
	});	
	
	$(document).on('click', '.buttonSi', function () {
		$(this).addClass("active")
		var objetivo = $(this).attr("target")
		$('#'+objetivo).slider("enable")
		objetivo = objetivo.split("-")[1]
		$('#amount-' + objetivo).prop('disabled', false);
	});	
	
	$(document).on("click", "#tabla_enfermedades_similares thead tr #cabeceraEnfermedades #arrowTurn", function(){
		if(rotacion == 0){
			rotacion -=180;
			$(this).rotate({ animateTo:rotacion});
			$("#filaDatosPaciente").hide();
		}
		else{
			rotacion +=180;
			$(this).rotate({ animateTo:rotacion});
			$("#filaDatosPaciente").show();
		}
		
	})
	
	function generarDesplegableEnfermedades(lEnfermedades){
		var codigoHTML = "";
		for(i=0; i < lEnfermedades.length; i++){
			codigoHTML += '<option>' + lEnfermedades[i] + '</option>'
		}
		codigoHTML += '<option> Todas </option>'
		
		$("#exampleFormControlSelect1").empty();
		$("#exampleFormControlSelect1").append(codigoHTML);
	}
	
	$(document).on("click", "#datosPacientes tbody td p", function(){
		mostrarPacienteConcreto($(this).html())
	})
	
	function mostrarPacienteConcreto(paciente){
		$( "#NombrePacienteValor" ).autocomplete( "search", paciente );
		$(".ui-menu-item-wrapper").trigger("click");
		//$(".tab-pane.fade.active.show").hide();
		$("#historico-tab").removeClass("show");
		$("#historico-tab").removeClass("active");
		$(".tab-pane.fade.active.show").removeClass("show");
		$(".tab-pane.fade.active").removeClass("active");
		$("#home-tab").addClass("active");
		$("#home-tab").addClass("show");
		$("#home").addClass("active");
		$("#home").addClass("show");
	}
</script>
	
	