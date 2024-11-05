from django.shortcuts import render,redirect
from django.urls import path,include
from django.contrib.auth import authenticate, login
from .models import *
from django.contrib import messages

from .forms import UsuarioForm, LoginForm,ParqueaderoForm

from sistema import views    

# Create your views here.
def home(request):
    return render(request ,'index.html')
def error(request):
    return render(request ,'error.html')

def crear_usuario(request):
    if request.method == "POST":
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()  # Guarda el usuario con la contraseña encriptada
            return redirect('/sistema/users/tipouser/')  # Redirige a la vista deseada
    else:
        form = UsuarioForm()
    return render(request, 'crear_usuario.html', {'form': form})


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            contrasena = form.cleaned_data['contrasena']
            usuario = authenticate(request, username=email, password=contrasena)
            if usuario is not None:
                login(request, usuario)
                return redirect('error')  # Cambia esto por tu vista principal
            else:
                form.add_error(None, 'Email o contraseña incorrectos.')
    else:
        form = LoginForm()
    
    return render(request, 'login.html', {'form': form})


# --tipo_user

def irtipo_user(request):
    # Verifica si el usuario está autenticado
    if request.user.is_authenticated:
        try:
            # Filtra por el correo electrónico del usuario autenticado
            usuario_obj = Usuario.objects.get(email=request.user.email)
            
            # Verifica el rol del usuario
            if usuario_obj.rol.strip()  == 'Administrador':
                # Si es administrador, obtiene todos los usuarios y los pasa al template
                dato = Usuario.objects.filter(is_active=True)
                return render(request, 'administra/tipouser/Tipouser.html', {"dato": dato})
            else:
                # Si el usuario no tiene el rol adecuado, muestra un mensaje de error
                messages.error(request, "No tienes permiso para acceder a esta página.")
                return render(request, 'error.html', {"message": "Usted no tiene permisos para estar acá."})
        
        except Usuario.DoesNotExist:
            # Si no se encuentra un usuario con el correo dado, redirige a la página de login
            messages.error(request, "Usuario no encontrado.")
            return redirect("/sistema/login/")
    
    else:
        # Si el usuario no está autenticado, redirige al login
        return redirect("/sistema/login/")

    
    
def registartipo_user(request):
    if request.user.is_authenticated:
        empleado = Usuario.objects.get(email=request.user.email)
       

        if empleado.rol.strip() == 'Administrador':
            
            tipo_E=request.POST["tipo"]
            
        
            servio =Usuario.objects.create(
                tipo_empleado=tipo_E)
            
            return redirect("/administrador/users/tipouser/")
            
        else:
            # Si el usuario no tiene el tipo de usuario adecuado, mostrar un mensaje de alerta
            messages.error(request, "No tienes permiso para acceder a esta página.")
            return render(request, 'error.html', {"message": "usted no tiene permisos para esatr aca ."})    
    else:
        return redirect("/formularios/login/")
    

def eliminartipo_user(request, tipo):
    # Verifica si el usuario está autenticado
    if request.user.is_authenticated:
        try:
            # Obtiene el empleado autenticado
            empleado = Usuario.objects.get(email=request.user.email)
            
            # Verifica el rol del empleado
            if empleado.rol.strip() == 'Administrador':
                # Obtiene el tipo de empleado a desactivar
                tipo_E = Usuario.objects.get(email=tipo)
                
                # Cambia el estado a inactivo
                tipo_E.is_active = False
                tipo_E.save()  # Guarda los cambios en la base de datos
                
                # Redirige a la lista de tipos de usuarios
                messages.success(request, "El tipo de empleado ha sido desactivado.")
                return redirect("/sistema/users/tipouser/")
            else:
                # Si el usuario no tiene el rol adecuado, muestra un mensaje de error
                messages.error(request, "No tienes permiso para acceder a esta página.")
                return render(request, 'error.html', {"message": "Usted no tiene permisos para estar acá."})
        
        except Usuario.DoesNotExist:
            messages.error(request, "Usuario no encontrado.")
            return redirect("/administrador/users/tipouser/")
        except Exception as e:
            messages.error(request, f"Ocurrió un error: {str(e)}")
            return redirect("/administrador/users/tipouser/")
    else:
        return redirect("/formularios/login/")

    

# --parqueadero

def listar_parqueaderos(request):
    if request.user.is_authenticated:
        try:
            usuario_obj = Usuario.objects.get(email=request.user.email)
            if usuario_obj.rol.strip() == 'Administrador'or 'Guarda':
                # Obtiene todos los parqueaderos activos
                parqueaderos = Parqueadero.objects.filter(estado='Activo')
                return render(request, 'administra/parqueadero/parqueadero.html', {'parqueaderos': parqueaderos})
            else:
                messages.error(request, "No tienes permiso para acceder a esta página.")
                return render(request, 'error.html', {"message": "Usted no tiene permisos para estar acá."})
        
        except Usuario.DoesNotExist:
            messages.error(request, "Usuario no encontrado.")
            return redirect("/sistema/login/")
    else:
        return redirect("/sistema/login/")


    

def registrar_parqueadero(request):
    if request.user.is_authenticated:
        try:
            usuario_obj = Usuario.objects.get(email=request.user.email)
            if usuario_obj.rol.strip() == 'Administrador'or 'Guarda':
                if request.method == "POST":
                    form = ParqueaderoForm(request.POST)
                    if form.is_valid():
                        parqueadero = form.save(commit=False)  # No guarda inmediatamente
                        parqueadero.fecha_ingreso = timezone.now()  # Establece la fecha de ingreso actual
                        parqueadero.id_guarda = usuario_obj  # Asigna la instancia de Usuario
                        parqueadero.save()  # Ahora guarda el objeto con la fecha de ingreso
                        messages.success(request, "Parqueadero registrado exitosamente.")
                        return redirect('/sistema/parqueadero/')
                else:
                    form = ParqueaderoForm()  # Crea un nuevo formulario si no es POST
                
                return render(request, 'administra/parqueadero/registrar_parqueadero.html', {'form': form})
            else:
                messages.error(request, "No tienes permiso para acceder a esta página.")
                return render(request, 'error.html', {"message": "Usted no tiene permisos para estar acá."})
        
        except Usuario.DoesNotExist:
            messages.error(request, "Usuario no encontrado.")
            return redirect("/sistema/login/")
    else:
        return redirect("/sistema/login/")

    

def salidaparqueadero(request, tipo):
    # Verifica si el usuario está autenticado
    if request.user.is_authenticated:
        try:
            # Obtiene el empleado autenticado
            empleado = Usuario.objects.get(email=request.user.email)
            
            # Verifica el rol del empleado
            if empleado.rol.strip() == 'Administrador':
                # Obtiene el tipo de empleado a desactivar
                tipo_E = Usuario.objects.get(email=tipo)
                
                # Cambia el estado a inactivo
                tipo_E.is_active = False
                tipo_E.save()  # Guarda los cambios en la base de datos
                
                # Redirige a la lista de tipos de usuarios
                messages.success(request, "El tipo de empleado ha sido desactivado.")
                return redirect("/sistema/users/tipouser/")
            else:
                # Si el usuario no tiene el rol adecuado, muestra un mensaje de error
                messages.error(request, "No tienes permiso para acceder a esta página.")
                return render(request, 'error.html', {"message": "Usted no tiene permisos para estar acá."})
        
        except Usuario.DoesNotExist:
            messages.error(request, "Usuario no encontrado.")
            return redirect("/administrador/users/tipouser/")
        except Exception as e:
            messages.error(request, f"Ocurrió un error: {str(e)}")
            return redirect("/administrador/users/tipouser/")
    else:
        return redirect("/formularios/login/")

    
