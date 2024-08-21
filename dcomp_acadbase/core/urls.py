# dcomp-acadbase/dcomp_acadbase/core/urls.py

from django.urls import path, include
from rest_framework.routers import DefaultRouter
from . import views
from django.contrib.auth import views as auth_views

router = DefaultRouter()
router.register(r'monografias-api', views.MonografiaViewSet)

urlpatterns = [
    #URLs padrão
    path('', views.index, name='index'),
    path('core/monografia/new/', views.monografia_create, name='monografia_create'),  # URL para o formulário de criação de monografia - CREATE
    path('core/monografia/list/', views.monografia_list, name='monografia_list'),  # URL para a lista de monografias - READ
    path('core/monografia/edit/<int:pk>/', views.monografia_edit, name='monografia_edit'), # URL para editar monografia - UPDATE
    path('core/monografia/delete/<int:pk>/', views.monografia_delete, name='monografia_delete'), # URL para excluir monografia - DELETE
    path('core/monografia/detail/<int:pk>/', views.monografia_detail, name='monografia_detail'),
    path('api/', include(router.urls)),

    # URLs de redefinição de senha
    path('password_reset/', auth_views.PasswordResetView.as_view(), name='password_reset'),
    path('password_reset/done/', auth_views.PasswordResetDoneView.as_view(), name='password_reset_done'),
    path('reset/<uidb64>/<token>/', auth_views.PasswordResetConfirmView.as_view(), name='password_reset_confirm'),
    path('reset/done/', auth_views.PasswordResetCompleteView.as_view(), name='password_reset_complete'),
]