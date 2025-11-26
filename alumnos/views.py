from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from reportlab.pdfgen import canvas
from reportlab.lib.pagesizes import letter
from django.core.mail import EmailMessage
from .forms import AlumnoForm
from .models import Alumno
import io
from django.contrib import messages

@login_required
def dashboard(request):
    alumnos = Alumno.objects.all()
    return render(request, "dashboard.html", {"alumnos": alumnos})


@login_required
def crear_alumno(request):
    if request.method == "POST":
        form = AlumnoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("dashboard")
        else:
            return render(request, "crear.html", {"form": form})
    
    form = AlumnoForm()
    return render(request, "crear.html", {"form": form})

@login_required
def borrar_alumno(request, id):
    alumno = get_object_or_404(Alumno, id=id)
    alumno.delete()
    return redirect('dashboard')

@login_required
def alumno_pdf(request, alumno_id):
    alumno = get_object_or_404(Alumno, id=alumno_id)

    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=letter)

    p.setFont("Helvetica", 14)
    p.drawString(100, 750, f"Datos del Alumno")
    p.drawString(100, 720, f"Nombre: {alumno.nombre}")
    p.drawString(100, 700, f"Edad: {alumno.edad}")
    p.drawString(100, 680, f"Curso: {alumno.curso}")

    p.showPage()
    p.save()

    pdf_data = buffer.getvalue()
    buffer.close()

    email = EmailMessage(
        subject=f"PDF del alumno {alumno.nombre}",
        body=f"Hola {request.user.username}, aquí tienes el PDF del alumno {alumno.nombre}.",
        from_email="tu_correo@example.com",
        to=[request.user.email],
    )
    email.attach(f"{alumno.nombre}.pdf", pdf_data, "application/pdf")

    messages.success(request, "📧 PDF enviado correctamente a tu correo")
    return redirect('dashboard')