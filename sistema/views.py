from django.shortcuts import render,redirect,get_object_or_404
from django.urls import path,include
from django.contrib.auth import authenticate, login
from .models import *
from django.contrib import messages

from .forms import UsuarioForm, LoginForm,ParqueaderoForm,EditarUsuarioForm

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
                
                # Redirige según el rol del usuario
                if usuario.rol.strip() == 'Administrador':
                    return redirect('/sistema/users/tipouser/')  # Cambia 'vista_administrador' por la URL o nombre de vista de administrador
                elif usuario.rol.strip() == 'Guarda':
                    return redirect('/sistema/parqueadero/')  # Cambia 'vista_guarda' por la URL o nombre de vista para guardas

                # En caso de un rol desconocido, puedes redirigir a una página de error o principal
                return redirect('pagina_principal')  # Opcional: redirigir a una página por defecto
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



def editar_usuario(request, usuario_id):
    usuario = get_object_or_404(Usuario, id=usuario_id)
    if request.method == 'POST':
        form = EditarUsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario actualizado correctamente.')
            return redirect('/sistema/users/tipouser/')  # Cambia esto por la vista donde quieres redirigir después de la edición
    else:
        form = EditarUsuarioForm(instance=usuario)
    return render(request, 'editar_usuario.html', {'form': form})

# --parqueadero

def listar_parqueaderos(request):
    if request.user.is_authenticated:
        try:
            usuario_obj = Usuario.objects.get(email=request.user.email)
            if usuario_obj.rol.strip() in ['Administrador', 'Guarda']:
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
            
            if usuario_obj.rol.strip() in ['Administrador', 'Guarda']:  # Verifica el rol correctamente
                if request.method == "POST":
                    form = ParqueaderoForm(request.POST)
                    if form.is_valid():
                        parqueadero = form.save(commit=False)  # No guarda inmediatamente
                        parqueadero.fecha_ingreso = timezone.now()  # Establece la fecha de ingreso actual
                        parqueadero.id_guarda = usuario_obj 
                        parqueadero.estado = "Activo" 

                        # Asignamos el conjunto 'zapan' a 'id_conjunto'
                        conjunto_obj = Conjunto.objects.get(nombre="zapan")
                        parqueadero.id_conjunto = conjunto_obj

                        parqueadero.save()  # Ahora guarda el objeto con la fecha de ingreso
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


    

from decimal import Decimal

from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from decimal import Decimal
from .models import Parqueadero, Conjunto
def salida_parqueadero(request, parqueadero_id):
    if request.user.is_authenticated:
        try:
            parqueadero = Parqueadero.objects.get(id=parqueadero_id)
            
            if parqueadero.estado == 'Activo':
                fecha_salida = timezone.now()
                horas_estacionado = (fecha_salida - parqueadero.fecha_ingreso).total_seconds() / 3600
                horas_estacionado_decimal = Decimal(horas_estacionado).quantize(Decimal('0.00'))

                conjunto = Conjunto.objects.get(id=parqueadero.id_conjunto.id)
                valor_fraccion_hora = Decimal(conjunto.fraccion_hora)

                valor_total = horas_estacionado_decimal * valor_fraccion_hora
                valor_total_formateado = f"${valor_total:,.2f}"

                # Actualiza el estado del parqueadero

                # Muestra el mensaje
                messages.success(request, f"""El vehículo {parqueadero.placa_vehiculo} ha salido.<br>
                                              Tiempo estacionado: {horas_estacionado_decimal:.2f} horas.<br>
                                              Total calculado: {valor_total_formateado}.
                                          """)
                return redirect('/sistema/parqueadero/')

            else:
                messages.error(request, "El parqueadero ya está finalizado.")
                return redirect("/sistema/parqueadero/")

        except Parqueadero.DoesNotExist:
            messages.error(request, "Parqueadero no encontrado.")
            return redirect("/sistema/parqueadero/")

    else:
        return redirect("/formularios/login/")




import os
from twilio.rest import Client
from django.shortcuts import render, redirect
from django.contrib import messages
from django.utils import timezone
from decimal import Decimal
from .models import Parqueadero, Conjunto
from django.core.mail import EmailMessage
from django.conf import settings
from django.shortcuts import redirect
from django.utils import timezone
from decimal import Decimal
from django.template.loader import render_to_string

from xhtml2pdf import pisa
from io import BytesIO
from django.template.loader import render_to_string

def generar_pdf_xhtml2pdf(parqueadero, valor_total, horas_estacionado, valor_fraccion_hora):
    # Renderizar el HTML con el contexto de los datos
    html = render_to_string('factura_parqueadero.html', {
        'placa_vehiculo': parqueadero.placa_vehiculo,
        'fecha_ingreso': parqueadero.fecha_ingreso,
        'fecha_salida': parqueadero.fecha_salida,
        'horas_estacionado': horas_estacionado,
        'valor_fraccion_hora': valor_fraccion_hora,
        'valor_total': valor_total
    })
    
    # Crear un buffer de memoria para el PDF
    pdf_buffer = BytesIO()

    # Convertir el HTML a PDF usando xhtml2pdf
    pisa_status = pisa.pisaDocument(BytesIO(html.encode("UTF-8")), pdf_buffer)
    
    # Volver al principio del buffer
    pdf_buffer.seek(0)

    # Si hay un error al generar el PDF, puedes manejarlo de la siguiente manera:
    if pisa_status.err:
        return None  # o puedes manejar el error como desees
    
    return pdf_buffer




def confirmar_salida_parqueadero(request, parqueadero_id):
    # Verifica si el usuario está autenticado
    if request.user.is_authenticated:
        try:
            # Obtiene el parqueadero por su ID
            parqueadero = Parqueadero.objects.get(id=parqueadero_id)

            # Verifica si el estado es 'Activo'
            if parqueadero.estado == 'Activo':
                fecha_salida = timezone.now()

                # Calcular horas estacionadas en Decimal
                horas_estacionado = (fecha_salida - parqueadero.fecha_ingreso).total_seconds() / 3600
                horas_estacionado_decimal = Decimal(horas_estacionado).quantize(Decimal('0.00'))  # Redondear a 2 decimales

                # Obtener el valor de fraccion_hora del conjunto relacionado (en Decimal)
                conjunto = Conjunto.objects.get(id=parqueadero.id_conjunto.id)
                valor_fraccion_hora = Decimal(conjunto.fraccion_hora)  # Asegúrate de que sea Decimal

                # Calcular el total a pagar
                valor_total = horas_estacionado_decimal * valor_fraccion_hora

                # Generar el PDF de la factura
                pdf_buffer = generar_pdf_xhtml2pdf(parqueadero, valor_total, horas_estacionado, valor_fraccion_hora)

                # Enviar el correo electrónico con el PDF adjunto
                try:
                    asunto = 'Confirmación de salida del parqueadero'
                    mensaje = (
                        f"Estimado usuario, su vehículo con placa {parqueadero.placa_vehiculo} ha salido del parqueadero.\n"
                        f"Total pagado: ${valor_total:,.2f}.\n"
                        f"Gracias por utilizar nuestro servicio. ¡Vuelva pronto!"
                    )
                    destinatario = parqueadero.contacto  # Asumimos que el contacto es un correo electrónico

                    email = EmailMessage(
                        asunto,
                        mensaje,
                        settings.EMAIL_HOST_USER,  # Remitente
                        [destinatario],  # Destinatario
                    )
                    email.attach('factura_parqueadero.pdf', pdf_buffer.getvalue(), 'application/pdf')
                    email.send(fail_silently=False)

                    # Si el correo se envía correctamente, actualiza el estado del parqueadero
                    parqueadero.total_calculado = valor_total
                    parqueadero.estado = 'Finalizado'
                    parqueadero.fecha_salida = fecha_salida
                    parqueadero.save()

                except Exception as e:
                    messages.error(request, f"Error al enviar el correo: {str(e)}")
                    # No actualizamos el estado si ocurre un error al enviar el correo
                    return redirect('/sistema/parqueadero/')

                # Si todo es exitoso, redirige al usuario
                return redirect('/sistema/parqueadero/')

            else:
                messages.error(request, "El parqueadero ya está finalizado.")
                return redirect("/sistema/parqueadero/")

        except Parqueadero.DoesNotExist:
            messages.error(request, "Parqueadero no encontrado.")
            return redirect("/sistema/parqueadero/")

    else:
        return redirect("/formularios/login/")















# citofonia 
from django.db.models import Q

def listar_citofonia(request):
    if request.user.is_authenticated:
        try:
            usuario_obj = Usuario.objects.get(email=request.user.email)
            if usuario_obj.rol.strip() in ['Administrador', 'Guarda']:
                query = request.GET.get('q', '')  # Obtener el término de búsqueda
                # Ordenar las propiedades por id (de menor a mayor)
                if query:
                    propiedades = Propiedad.objects.filter(numero__icontains=query).order_by('id')
                else:
                    propiedades = Propiedad.objects.all().order_by('id')
                
                return render(request, 'administra/citofonia/citofonia.html', {'Propiedades': propiedades, 'query': query})
            else:
                messages.error(request, "No tienes permiso para acceder a esta página.")
                return render(request, 'error.html', {"message": "Usted no tiene permisos para estar acá."})
        except Usuario.DoesNotExist:
            messages.error(request, "Usuario no encontrado.")
            return redirect("/sistema/login/")
    else:
        return redirect("/sistema/login/")

