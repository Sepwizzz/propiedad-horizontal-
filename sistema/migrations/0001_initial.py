# Generated by Django 5.0.2 on 2024-11-05 04:25

import django.db.models.deletion
import django.utils.timezone
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('auth', '0012_alter_user_first_name_max_length'),
    ]

    operations = [
        migrations.CreateModel(
            name='Conjunto',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('nombre', models.CharField(max_length=100)),
                ('direccion', models.CharField(max_length=150)),
                ('fraccion_hora', models.DecimalField(decimal_places=2, max_digits=5)),
            ],
        ),
        migrations.CreateModel(
            name='Usuario',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('password', models.CharField(max_length=128, verbose_name='password')),
                ('last_login', models.DateTimeField(blank=True, null=True, verbose_name='last login')),
                ('is_superuser', models.BooleanField(default=False, help_text='Designates that this user has all permissions without explicitly assigning them.', verbose_name='superuser status')),
                ('email', models.EmailField(max_length=254, unique=True)),
                ('nombre', models.CharField(max_length=100)),
                ('apellido', models.CharField(max_length=100)),
                ('telefono', models.CharField(blank=True, max_length=20, null=True)),
                ('direccion', models.CharField(blank=True, max_length=150, null=True)),
                ('rol', models.CharField(choices=[('Administrador', 'Administrador'), ('Guarda', 'Guarda')], max_length=20)),
                ('is_active', models.BooleanField(default=True)),
                ('is_staff', models.BooleanField(default=False)),
                ('groups', models.ManyToManyField(blank=True, help_text='The groups this user belongs to. A user will get all permissions granted to each of their groups.', related_name='user_set', related_query_name='user', to='auth.group', verbose_name='groups')),
                ('user_permissions', models.ManyToManyField(blank=True, help_text='Specific permissions for this user.', related_name='user_set', related_query_name='user', to='auth.permission', verbose_name='user permissions')),
            ],
            options={
                'abstract': False,
            },
        ),
        migrations.CreateModel(
            name='AdministradoresConjuntos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_administrador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conjuntos_asignados', to=settings.AUTH_USER_MODEL)),
                ('id_conjunto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sistema.conjunto')),
            ],
        ),
        migrations.CreateModel(
            name='GuardasConjuntos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('id_conjunto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sistema.conjunto')),
                ('id_guarda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='conjuntos_guardados', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='HistorialAdministradores',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha_registro', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_cambio', models.DateTimeField(blank=True, null=True)),
                ('id_administrador', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('id_conjunto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sistema.conjunto')),
            ],
        ),
        migrations.CreateModel(
            name='Parqueadero',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('tipo', models.CharField(choices=[('moto', 'moto'), ('carro', 'carro')], max_length=15)),
                ('placa_vehiculo', models.CharField(max_length=10)),
                ('fecha_ingreso', models.DateTimeField(default=django.utils.timezone.now)),
                ('fecha_salida', models.DateTimeField(blank=True, null=True)),
                ('total_calculado', models.DecimalField(blank=True, decimal_places=2, max_digits=8, null=True)),
                ('estado', models.CharField(choices=[('Activo', 'Activo'), ('Finalizado', 'Finalizado')], default='Activo', max_length=10)),
                ('id_conjunto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sistema.conjunto')),
                ('id_guarda', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='parqueaderos_registrados', to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Propiedad',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('numero', models.CharField(max_length=10)),
                ('contacto_1', models.CharField(max_length=20)),
                ('contacto_2', models.CharField(blank=True, max_length=20, null=True)),
                ('contacto_3', models.CharField(blank=True, max_length=20, null=True)),
                ('id_conjunto', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='sistema.conjunto')),
            ],
        ),
    ]
