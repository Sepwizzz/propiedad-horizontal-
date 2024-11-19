from django.urls import path,include
from sistema import views    
from .views import *
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('error/',views.error,name='error'),
     path('crear_usuario/', crear_usuario, name='crear_usuario'),
     path('login/', login_view, name='login'),

    path('users/tipouser/',views.irtipo_user),
    path('users/tipouser/registrtipouser/',views.registartipo_user),
    path('users/tipouser/EliminarTipoE/<tipo>',views.eliminartipo_user),
    path('users/editar/<int:usuario_id>/', views.editar_usuario, name='editar_usuario'),


    path('parqueadero/', views.listar_parqueaderos),
    path('parqueadero/registrparqueadero/', views.registrar_parqueadero),
    path('parqueadero/salida/<int:parqueadero_id>/', views.salida_parqueadero),  
    path('parqueadero/salida/<int:parqueadero_id>/confirmar/', views.confirmar_salida_parqueadero, name='confirmar_salida_parqueadero'),


    path('citofonia/',views.listar_citofonia,name='listar_citofonia'),
    path('citofonia/citofoniagregar/',views.registrar_parqueadero),
    path('citofonia/citofoniaelimiar/<tipo>',views.eliminartipo_user),
    

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]