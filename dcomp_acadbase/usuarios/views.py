from django.shortcuts import render, redirect
from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth import authenticate, login, logout
from .serializers import RegisterUserSerializer, LoginUserSerializer

# Create your views here.
class UserRegistrationView(generics.CreateAPIView):
    serializer_class = RegisterUserSerializer

class LoginView(generics.GenericAPIView):
    serializer_class = LoginUserSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        username = serializer.validated_data['username']
        password = serializer.validated_data['password']
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            #redirect('index') 
            return Response({'msg': 'Login feito com sucesso'}, status=status.HTTP_200_OK)
        return Response({'msg': 'Login mal sucedido, tente novamente'}, status=status.HTTP_400_BAD_REQUEST)

class LogoutView(generics.GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, *args, **kwargs):

        if (IsAuthenticated):
            logout(request)
            return Response({'msg': 'Você saiu com sucesso'}, status=status.HTTP_200_OK)
        return Response({'msg': 'Você não está autenticado'}, status=status.HTTP_401_UNAUTHORIZED)    
    
    
