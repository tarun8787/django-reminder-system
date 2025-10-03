from django.urls import path
from jobtracker.core.views import LoginView, LogoutView, RegistrationView, DashboardView, DeleteUserView, HomeView, TokenRefreshView
from rest_framework_simplejwt.views import TokenObtainPairView

urlpatterns = [
    path('login/', LoginView.as_view(), name='login_view'),
    path('logout/', LogoutView.as_view(), name='logout_view'),
    path('registration/', RegistrationView.as_view(), name='register_view'),
    path('delete/', DeleteUserView.as_view(), name='delete_user_view'),
    path('dashboard/', DashboardView.as_view(), name='dashboard_view'),
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('home/', HomeView.as_view(), name="home_view"),
]