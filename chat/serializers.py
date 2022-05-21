from dataclasses import field
from django.forms import UUIDField
from rest_framework import serializers
from chat.models import Message, Room 
from django.contrib.auth.models import User

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = '__all__'
        read_only_fields = ['date_joined','user_permissions','groups','is_active','is_staff','is_superuser','last_login']
    def create(self, validated_data):
        print('hey')        
        user = User(
            email=validated_data['email'],
            username=validated_data['username']
        )
        user.set_password(validated_data['password'])
        user.save()
        return user

class MessageSerializer(serializers.ModelSerializer):
    class Meta:
        model=Message
        fields = '__all__'
        # read_only_fields = ['room_id']
        # depth = 1

class RoomSerializer(serializers.ModelSerializer):
    # participants = serializers.ReadOnlyField(many=True)
    class Meta:
        model=Room
        fields = '__all__'
        read_only_fields = ['room_id']

        # depth=1
