# authentication.py
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.exceptions import AuthenticationFailed
from rest_framework.permissions import AllowAny


class CookieJWTAuthentication(JWTAuthentication):
    def authenticate(self, request):
        token = request.COOKIES.get('access_token')
        if not token:
            return None

        try:
            validated = self.get_validated_token(token)
            return self.get_user(validated), validated

        except Exception:
            try:
                perms = getattr(getattr(request.resolver_match.func, 'view_class', None), 'permission_classes', [])
                if any(issubclass(p, AllowAny) for p in perms):
                    return None
            except Exception:
                pass
            
            raise AuthenticationFailed('Token is invalid or expired')
