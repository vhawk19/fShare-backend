from django.urls import path, include
from rest_framework.routers import DefaultRouter
from chat import views

router = DefaultRouter()
router.register(prefix=r'chat',viewset=views.ChatRoomViewset,basename="chat")
router.register(prefix=r'messages',viewset=views.MessageViewset,basename="messages")
router.register(prefix=r'user',viewset=views.UserViewset,basename="user")


urlpatterns = [
    path('', include(router.urls)),
]