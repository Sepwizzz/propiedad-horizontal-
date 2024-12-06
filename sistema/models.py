from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.utils import timezone

# User Manager personalizado
class UsuarioManager(BaseUserManager):
    def create_user(self, email, nombre, apellido, contrasena=None, **extra_fields):
        """Crea y devuelve un usuario con un correo electrónico, nombre y apellido."""
        if not email:
            raise ValueError("El correo electrónico debe ser proporcionado")
        email = self.normalize_email(email)
        usuario = self.model(email=email, nombre=nombre, apellido=apellido, **extra_fields)
        usuario.set_password(contrasena)  # Almacenar la contraseña encriptada
        usuario.save(using=self._db)
        return usuario

    def create_superuser(self, email, nombre, apellido, contrasena=None, **extra_fields):
        """Crea y devuelve un superusuario."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        return self.create_user(email, nombre, apellido, contrasena, **extra_fields)

# Tabla unificada de usuarios (Administradores y Guardas)
class Usuario(AbstractBaseUser, PermissionsMixin):
    ROLES = [
        ('Administrador', 'Administrador'),
        ('Guarda', 'Guarda'),
    ]

    email = models.EmailField(unique=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    telefono = models.CharField(max_length=20, blank=True, null=True)
    direccion = models.CharField(max_length=150, blank=True, null=True)
    rol = models.CharField(max_length=20, choices=ROLES)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UsuarioManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nombre', 'apellido']

    def __str__(self):
        return f"{self.nombre} {self.apellido} - {self.rol}"

# Tabla de conjuntos (Cada conjunto no tiene un administrador asignado directamente)
class Conjunto(models.Model):
    nombre = models.CharField(max_length=100)
    direccion = models.CharField(max_length=150)
    fraccion_hora = models.DecimalField(max_digits=5, decimal_places=2)

    def __str__(self):
        return self.nombre

# Tabla de relación entre administradores y conjuntos
class AdministradoresConjuntos(models.Model):
    id_administrador = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="conjuntos_asignados")
    id_conjunto = models.ForeignKey(Conjunto, on_delete=models.CASCADE)

# Tabla de relación entre guardas y conjuntos
class GuardasConjuntos(models.Model):
    id_guarda = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="conjuntos_guardados")
    id_conjunto = models.ForeignKey(Conjunto, on_delete=models.CASCADE)

# Tabla de parqueaderos (Registro de parqueos con estado, placa y datos del guarda de turno)
class Parqueadero(models.Model):
    ESTADO_CHOICES = [
        ('Activo', 'Activo'),
        ('Finalizado', 'Finalizado'),
    ]
    TIPO_CHOICES = [
        ('moto', 'moto'),
        ('carro', 'carro'),
    ]

    tipo = models.CharField(max_length=15, choices=TIPO_CHOICES)
    contacto = models.CharField(max_length=254, null=True, blank=True)
    placa_vehiculo = models.CharField(max_length=10)
    fecha_ingreso = models.DateTimeField(default=timezone.now)
    fecha_salida = models.DateTimeField(null=True, blank=True)
    total_calculado = models.DecimalField(max_digits=8, decimal_places=2, null=True, blank=True)
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='Activo')
    id_conjunto = models.ForeignKey(Conjunto, on_delete=models.CASCADE)
    id_guarda = models.ForeignKey(Usuario, on_delete=models.CASCADE, related_name="parqueaderos_registrados")

    def __str__(self):
        return f"Parqueadero {self.placa_vehiculo} - {self.estado}"

    # Ejemplo de validación antes de guardar
    def save(self, *args, **kwargs):
        if self.estado == 'Finalizado' and self.fecha_salida is None:
            raise ValueError("La fecha de salida debe ser registrada cuando el estado sea 'Finalizado'.")
        super().save(*args, **kwargs)


# Tabla de propiedades en cada conjunto (Para registrar los números de contacto de citofonía)
from django.core.validators import RegexValidator

class Propiedad(models.Model):
    # Regex pattern for validating phone numbers (example for Colombia)
    phone_validator = RegexValidator(regex=r'^\+?\d{10,15}$', message="Ingrese un número de teléfono válido.")

    numero = models.CharField(max_length=10, unique=True)
    id_conjunto = models.ForeignKey(Conjunto, on_delete=models.CASCADE)
    contacto_1 = models.CharField(max_length=20, validators=[phone_validator])
    nombre_1 = models.CharField(max_length=20 , blank=True,null=True)
    contacto_2 = models.CharField(max_length=20, blank=True, null=True, validators=[phone_validator])
    nombre_2 = models.CharField(max_length=20, blank=True, null=True)
    contacto_3 = models.CharField(max_length=20, blank=True, null=True, validators=[phone_validator])
    nombre_3 = models.CharField(max_length=20, blank=True, null=True)

    def __str__(self):
        return f"Propiedad {self.numero} en {self.id_conjunto.nombre}"

# Tabla de historial de administradores
class HistorialAdministradores(models.Model):
    id_conjunto = models.ForeignKey(Conjunto, on_delete=models.CASCADE)
    id_administrador = models.ForeignKey(Usuario, on_delete=models.CASCADE)
    fecha_registro = models.DateTimeField(default=timezone.now)
    fecha_cambio = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return f"Historial {self.id_administrador} - {self.id_conjunto}"
