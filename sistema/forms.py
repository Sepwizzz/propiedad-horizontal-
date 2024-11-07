from django import forms
from .models import Usuario ,Parqueadero

class UsuarioForm(forms.ModelForm):
    contrasena = forms.CharField(widget=forms.PasswordInput(), label="Contraseña")  # Campo para la contraseña

    class Meta:
        model = Usuario
        fields = ['email', 'nombre', 'apellido', 'telefono', 'direccion', 'contrasena', 'rol']

    # Override el método save para encriptar la contraseña
    def save(self, commit=True):
        usuario = super().save(commit=False)
        usuario.set_password(self.cleaned_data["contrasena"])  # Encriptar la contraseña
        if commit:
            usuario.save()
        return usuario


class LoginForm(forms.Form):
    email = forms.EmailField(label='Email')
    contrasena = forms.CharField(label='Contraseña', widget=forms.PasswordInput)


class ParqueaderoForm(forms.ModelForm):
    class Meta:
        model = Parqueadero
        fields = [ 'tipo', 'placa_vehiculo', 'estado','id_conjunto']  



class EditarUsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['email', 'nombre', 'apellido', 'rol'] 