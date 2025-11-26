from django.shortcuts import render, redirect
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import authenticate, login, logout
from django.core.mail import send_mail
from django.db import IntegrityError
from .forms import CustomUserCreationForm

# Create your views here.

def home(request):
    return render(request, 'home.html')

def signup(request):
    if request.method == 'GET':
        return render(request, 'registro.html', {'form': CustomUserCreationForm()})

    else:
        form = CustomUserCreationForm(request.POST)

        if form.is_valid():
            try:
                user = form.save(commit=False)
                user.email = form.cleaned_data['email']
                user.save()
                login(request, user)

                send_mail(
                    subject='¡Bienvenido al listado!',
                    message=f'Hola {user.username}, gracias por registrarte.',
                    from_email=None,
                    recipient_list=[user.email],
                    fail_silently=False
                )

                return redirect('dashboard')
            except IntegrityError:
                return render(request, 'registro.html', {
                    'form': CustomUserCreationForm(),
                    'error': 'El usuario ya existe'
                })
        else:
            return render(request, 'registro.html', {
                'form': form,
                'error': 'Datos inválidos'
            })


def signout(request):
    logout(request)
    return redirect('home')

def signin(request):

    if request.method == 'GET':
        return render(request, 'signin.html',
            {'form': AuthenticationForm()})
    else:
        user = authenticate(request, username=request.POST['username'],
            password=request.POST['password'])
        if user is None:
            return render(request, 'signin.html',
            {'form': AuthenticationForm(),
            'error': 'El usuario o la contraseña son incorrectos'})
        else:
            login(request, user)
            return redirect('dashboard')