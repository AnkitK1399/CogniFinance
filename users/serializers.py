from rest_framework import serializers
from .models import User

class RegisterSerializer(serializers.ModelSerializer):
     
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'email', 'first_name', 
            'last_name', 'gender', 'role', 'occupation', 
            'dob', 'current_balance']
    
    def validate(self, data):
        if not data.get('first_name'):
            raise serializers.ValidationError({"first_name": "Please provide a first name."})
        if not data.get('last_name'):
            raise serializers.ValidationError({"last_name": "Please provide a last name."})
        return data
    def validate_email(self,value):
        if User.objects.filter(email=value).exists():
            raise serializers.ValidationError("Email already exists.")
        return value
    def validate_initial_balance(self, value):
        if value < 0:
            raise serializers.ValidationError("Initial balance cannot be negative.")
        return value
    def create(self, validated_data):
        password = validated_data.pop("password")
        user = User.objects.create(**validated_data)
        user.set_password(password)  
        user.save()
        return user

class AdminUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = [
            'id', 'username', 'email', 'first_name', 'last_name', 
            'gender', 'role', 'occupation', 'city', 
            'initial_balance','current_balance', 'is_staff', 'is_active', 'date_joined'
        ]
        read_only_fields = ['id', 'date_joined']

class AnalystUserSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = User
        fields = [
            'username', 'email', 'gender', 'occupation', 
            'city', 'initial_balance'
        ]
        read_only_fields = fields
