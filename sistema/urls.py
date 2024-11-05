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

    path('parqueadero/',views.listar_parqueaderos),
    path('parqueadero/registrparqueadero/',views.registrar_parqueadero),
    path('parqueadero/EliminarTipoE/<tipo>',views.eliminartipo_user),

    path('logout/', auth_views.LogoutView.as_view(), name='logout'),

]