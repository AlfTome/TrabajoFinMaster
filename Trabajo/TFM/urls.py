from django.conf.urls import url
from TFM import views

urlpatterns = [
    url(r'^$', views.HomePageView.as_view()),
	url(r'^about/$', views.AboutPageView.as_view()),
	url(r'^formulario/$', views.Formulario.as_view()),
	url(r'^dame_pacientes/$',views.dame_pacientes),
	url(r'^dame_pacientes_con_filtro/$',views.dame_pacientes_con_filtro),
	url(r'^dame_paciente_formulario/$',views.dame_paciente_formulario),
	url(r'^predecir/$',views.predecir),
	url(r'^buscarSimilar/$',views.buscarSimilar),
	url(r'^historicoPacientes/$',views.historicoPacientes),
	
]