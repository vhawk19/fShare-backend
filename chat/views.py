from email import message
from django.shortcuts import render
from rest_framework import viewsets, views
from chat.models import Room, Message
from django.contrib.auth.models import User
from chat.serializers import MessageSerializer, RoomSerializer, UserSerializer, ReadMessageSerializer
from rest_framework.response import Response
from rest_framework import status #/ Create your views here.
from rest_framework.authentication import SessionAuthentication, BasicAuthentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from chat.auth import CsrfExemptSessionAuthentication
# from restframework_simplejwt.tokens import AccessToken

class MessageCreateView(views.APIView):
    queryset = Message.objects.all()
    serializer_class = MessageSerializer
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # snippet = self.get_object(pk)
        print(request.data)
        print(request.user)
        data = request.data
        data['creator'] = request.user.id
        print(data)

        serializer = MessageSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class UserViewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class =UserSerializer
    

    # @action(detail=True, methods=['post'])
    # def set_password(self, request, pk=None):
    #     user = self.get_object()
    #     serializer = PasswordSerializer(data=request.data)
    #     if serializer.is_valid():
    #         user.set_password(serializer.validated_data['password'])
    #         user.save()
    #         return Response({'status': 'password set'})
    #     else:
    #         return Response(serializer.errors,
    #                         status=status.HTTP_400_BAD_REQUEST)

    # @action(detail=False)
    # def recent_users(self, request):
    #     recent_users = User.objects.all().order_by('-last_login')

    #     page = self.paginate_queryset(recent_users)
    #     if page is not None:
    #         serializer = self.get_serializer(page, many=True)
    #         return self.get_paginated_response(serializer.data)

    #     serializer = self.get_serializer(recent_users, many=True)
    #     return Response(serializer.data)
class ChatRoomViewset(viewsets.ModelViewSet):
    queryset = Room.objects.all()
    serializer_class = RoomSerializer
    # authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    
    def create(self, request, *args, **kwargs):
        data=request.data
        data['creator'] = request.user
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(self.get_serializer(obj).data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        return serializer.save()

class MessageViewset(viewsets.ModelViewSet):
    # authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Message.objects.all()
    serializer_class = MessageSerializer

    def create(self, request, *args, **kwargs):
        print(request.data)
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(self.get_serializer(obj).data, status=status.HTTP_201_CREATED, headers=headers)


class MessageViewsetRead(viewsets.ModelViewSet):
    # authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    queryset = Message.objects.all()
    serializer_class = ReadMessageSerializer

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        obj = self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(self.get_serializer(obj).data, status=status.HTTP_201_CREATED, headers=headers)

class ChatRoomViewsetByUser(viewsets.ViewSet):
    # queryset = Room.objects.all()
    # serializer_class = RoomSerializer
    # authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]
    def list(self, request):
        print(request.user)
        queryset = Room.objects.filter(participants__in=[request.user])
        serializer = RoomSerializer(queryset, many=True)
        return Response(serializer.data)

class MessageViewsetByChatRoom(viewsets.ViewSet):
    # authentication_classes = [CsrfExemptSessionAuthentication, BasicAuthentication]
    permission_classes = [IsAuthenticated]

    def list(self, request):
        print(request.user)
        cid = self.request.query_params.get('cid')
        print(cid)
        queryset = Message.objects.filter(room_id__in=[cid])
        serializer = ReadMessageSerializer(queryset, many=True)
        return Response(serializer.data)
