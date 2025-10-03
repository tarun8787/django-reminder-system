from django.shortcuts import redirect, render # type: ignore

# Create your views here.
from jobtracker.core.models import User
from rest_framework.views import APIView
from rest_framework.authentication import authenticate
from jobtracker.core.serializers import LoginSerializer, UserSerializer, RegisterSerializer
from rest_framework.response import Response
from rest_framework_simplejwt.tokens import RefreshToken, TokenError
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework import status
import logging

logger = logging.getLogger(__name__)

class LoginView(APIView):
    serializer_class = LoginSerializer
    permission_classes=[AllowAny]

    def get(self, request, *args, **kwargs):
        return render(request, 'login.html')

    def post(self, request, *args, **kwargs):
        email = request.data.get('email', '').strip()
        password = request.data.get('password', '').strip()

        user = authenticate(email=email, password=password)
        if user is not None:
            refresh = RefreshToken.for_user(user)
            user_serializer = self.serializer_class(user)
            response = redirect('/home/')
            response.set_cookie('access_token', str(refresh.access_token), httponly=True)
            response.set_cookie('refresh_token', str(refresh), httponly=True)
            return response
        else:
            return render(request, 'login.html', {'error': 'Invalid credentials'})
        

class LogoutView(APIView):
    permission_classes = (AllowAny,)

    def get(self, request):
        return render(request, 'logout.html')

    def post(self, request, *args, **kwargs):
        try:
            refresh_token = request.COOKIES.get("refresh_token")
            if not refresh_token:
                return render(request, 'logout.html', {"error": "Refresh token not found."})

            token = RefreshToken(refresh_token)
            token.blacklist()

            response = redirect('/login/')
            response.delete_cookie('access_token')
            response.delete_cookie('refresh_token')
            return response

        except TokenError as e:
            return render(request, 'logout.html', {'error': str(e)})
        

class DashboardView(APIView):
    permission_classes = (IsAuthenticated,)
    
    def get(self, request, *args, **kwargs):
        user = request.user
        user_serializer = UserSerializer(user)
        return Response({
                'user': user_serializer.data
            },
            status=status.HTTP_200_OK
        )
    

class RegistrationView(APIView):
    model = User
    permission_classes = (AllowAny,)
    serializer_class = RegisterSerializer

    def get(self, request):
        return render(request, 'register.html', {'form': self.serializer_class()})

    def post(self, request):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            refresh = RefreshToken.for_user(user)

            response = redirect('/home/')
            response.set_cookie('access_token', str(refresh.access_token), httponly=True)
            response.set_cookie('refresh_token', str(refresh), httponly=True)
            return response
        
        else:
            errors = []
            for field_errors in serializer.errors.values():
                if isinstance(field_errors, list):
                    errors.extend(field_errors)
                else:
                    errors.append(field_errors)
            return render(request, "register.html", {"errors": errors})



class DeleteUserView(APIView):
    permission_classes = (IsAuthenticated,)

    def delete(self, request):
        user = request.user
        try:
            refresh_token = request.data.get('refresh_token')
            token = RefreshToken(refresh_token)
            token.blacklist()
        except:
            return Response({
                    'message': 'Error Occurred While Deleting the User'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        
        user.delete()
        return Response({
            'detail': 'User and token deleted'
            }, 
            status=status.HTTP_204_NO_CONTENT)


class HomeView(APIView):
    def get(self, request):
        return render(request, 'home.html')
    

class TokenRefreshView(APIView):
    permission_classes= (AllowAny,)

    def post(self, request):
        refresh_token = request.COOKIES.get('refresh_token')
        if not refresh_token:
            return Response({'detail': 'Refresh token missing.'}, status=status.HTTP_400_BAD_REQUEST)

        try:
            token = RefreshToken(refresh_token)
            access_token = str(token.access_token)

            response = Response({'access': access_token}, status=status.HTTP_200_OK)

            response.set_cookie(
                key='access_token',
                value=access_token,
                httponly=True,
            )
            return response

        except TokenError as e:
            return Response({'detail': 'Invalid refresh token.', 'error': str(e)}, status=status.HTTP_401_UNAUTHORIZED)