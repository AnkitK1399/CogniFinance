from django.urls import path
from .views import RegisterUserView, LoginView, LogoutView, RefreshTokenView, ProtectedView
urlpatterns=[
    path('register/', RegisterUserView.as_view(), name='register_user' ),
    path('login/', LoginView.as_view(), name='Login_view' ),
    path('logout/', LogoutView.as_view(), name='logout_view'),
    path('refresh/', RefreshTokenView.as_view(), name='refreshToken_view'),
    path('protected/', ProtectedView.as_view(), name='protected_view'),
]