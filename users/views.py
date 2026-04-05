from rest_framework import generics, status
from rest_framework.response import Response
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser
from .serializers import RegisterSerializer, AdminUserSerializer, AnalystUserSerializer
from django.contrib.auth import authenticate
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from .permissions import IsAdminRole, IsAnalystRole, IsOwnerAdminOrAnalystReadOnly
from django.shortcuts import get_object_or_404
from .models import User
from rest_framework.pagination import PageNumberPagination

class StandardPagination(PageNumberPagination):
    page_size = 10
    page_size_query_param = 'page_size'
    max_page_size = 100


class RegisterUserView(generics.CreateAPIView):
    serializer_class = RegisterSerializer
    permission_classes = [AllowAny]

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid():
            user = serializer.save()  
            return Response({
                'message': 'User registered successfully!',
                'user': {
                    'username': user.username,
                    'email': user.email,
                    'user_role': user.role 
                }
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    
class LoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')
        user = authenticate(username=username,password=password)

        if user is None:
            return Response(
                {'error':'Invalid username or password'},
                status=status.HTTP_401_UNAUTHORIZED
            )
        refresh = RefreshToken.for_user(user)
        access = str(refresh.access_token)
        return Response(
            {
                'message':'LogIn Successful',
                'access': access,
                'refresh': str(refresh),
                'user':{
                    'id':user.pk,
                    'username':user.username,
                    'email':user.email,

                }

            }
        )

class LogoutView(APIView):
    permission_classes = [IsAuthenticated]
    def post(self,request):
        try:
            refresh_token = request.data.get('refresh')
            if refresh_token is None:
                return Response(
                    {'error': 'Refresh token is required'},
                    status=status.HTTP_400_BAD_REQUEST
                )

            token = RefreshToken(refresh_token)
            token.blacklist() 
            return Response({'message': 'Logout successful'}, status=200)
        except Exception as e:
           return Response({'error': 'Invalid refresh token'}, status=400)

class RefreshTokenView(APIView):
    def post(self, request):
        try:
            refresh_string = request.data.get('refresh')
            refresh = RefreshToken(refresh_string)
            return Response({
                'access': str(refresh.access_token), 
            }, status=200)
        except Exception:
            return Response({'error': 'Token is invalid or expired'}, status=401)


class ProtectedView(APIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        return Response({
            'user_id': request.user.id,
            'Name' : f'welcome {request.user.first_name} {request.user.last_name}',
            'Email' : request.user.email,
            'Gender' : request.user.gender,         
        })
    
class UserListView(APIView):
    permission_classes = [IsAuthenticated, (IsAdminRole | IsAnalystRole)]

    def get(self, request):
        users = User.objects.all()
        record_pagination = StandardPagination()
        paginated_data = record_pagination.paginate_queryset(users,request=request) 
        if request.user.role == 'ADMIN':
            serializer = AdminUserSerializer(paginated_data, many=True)
        else:
            serializer = AnalystUserSerializer(paginated_data, many=True)
        response = record_pagination.get_paginated_response(serializer.data).data
        return Response(response, status=200)


class UserProfileDetailView(APIView):
    permission_classes = [IsAuthenticated, IsOwnerAdminOrAnalystReadOnly]

    def get_user(self, pk):
        user_obj = get_object_or_404(User, pk=pk)
        self.check_object_permissions(self.request, user_obj)
        return user_obj

    def get(self, request, pk):
        target_user = self.get_user(pk)
        if request.user.role == 'ANALYST':
            serializer = AnalystUserSerializer(target_user)
        else:
            serializer = AdminUserSerializer(target_user)
        return Response(serializer.data)

    def put(self, request, pk):
        target_user = self.get_user(pk)
        if request.user.role != 'ADMIN':
            request.data.pop('is_staff', None)
            request.data.pop('is_active', None)
            request.data.pop('role', None)
            request.data.pop('id', None)
        serializer = AdminUserSerializer(target_user, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response({"message":"update successful"},serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        target_user = self.get_user(pk)
        target_user.delete()
        return Response({"message": "Profile deleted successfully"}, status=status.HTTP_204_NO_CONTENT)