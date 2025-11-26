from django.urls import path
from . import views

urlpatterns = [
    path('dashboard/', views.dashboard, name='dashboard'),
    path('crear/', views.crear_alumno, name="crear_alumno"),
    path('pdf/<int:alumno_id>/', views.alumno_pdf, name='alumno_pdf'),
    path('alumno/<int:id>/borrar/', views.borrar_alumno, name='borrar_alumno'),
]