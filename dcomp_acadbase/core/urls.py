# dcomp-acadbase/dcomp_acadbase/core/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'monografias', views.MonografiaViewSet)

urlpatterns = [
    #URLs padrão
    path('', views.index, name='index'),
    # path('core/painel', views.painel, name='painel')
    path('core/monografia/', views.monografia_form, name='monografia_form'),  # URL para o formulário de criação de monografia
    path('monografia/<int:pk>/', views.monografia_form, name='monografia_edit'), # URL para editar monografia
    # path('', monografia_delete, name='monografia_delete)
    # path('', monografia_edit)
    path('core/monografia/list/', views.monografia_list, name='monografia_list'),  # URL para a lista de monografias
    path('api/', include(router.urls)),

    # URLs de redefinição de senha
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]