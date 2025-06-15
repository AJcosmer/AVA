from django.urls import path
from .views import *

urlpatterns = [
    path('hello/', HelloFromCookieView.as_view()),
    path('register/', RegisterView.as_view()),
    path('login/', CookieLoginView.as_view()),
    path('logout/', LogoutView.as_view()),
    path('usuarios/', UsuarioListView.as_view()),
    path('usuarios/<int:pk>/', UsuarioRetrieveUpdateDestroyView.as_view()),
    path('roles/', RolListCreateView.as_view()),
    path('roles/<int:pk>/', RolRetrieveUpdateDestroyView.as_view()),
    path('roles/asignar/', UsuarioRolCreateView.as_view()),
]
