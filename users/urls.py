from django.urls import path
from .views import RegisterUserView, LoginView, LogoutView, RefreshTokenView, ProtectedView, UserListView, UserProfileDetailView
urlpatterns=[
    path('register/', RegisterUserView.as_view(), name='register_user' ),
    path('login/', LoginView.as_view(), name='Login_view' ),
    path('logout/', LogoutView.as_view(), name='logout_view'),
    path('refresh/', RefreshTokenView.as_view(), name='refreshToken_view'),
    path('protected/', ProtectedView.as_view(), name='protected_view'),
    path('userlist/', UserListView.as_view(), name='userList_view'),
    path('userdetail/<int:pk>/', UserProfileDetailView.as_view(), name='userDetail_view'),
]