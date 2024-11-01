from django.shortcuts import render

from rest_framework import viewsets
from .models import Content
from .serializers import ContentSerializer
from rest_framework.permissions import IsAuthenticatedOrReadOnly
from rest_framework import viewsets, permissions
from .models import Playlist
from .serializers import PlaylistSerializer

class ContentViewSet(viewsets.ModelViewSet):
    queryset = Content.objects.all()
    serializer_class = ContentSerializer
    #permission_classes = [IsAuthenticatedOrReadOnly]

    #def perform_create(self, serializer):
     #   serializer.save(creator=self.request.user)# Create your views here.



class PlaylistViewSet(viewsets.ModelViewSet):
    queryset = Playlist.objects.all()
    serializer_class = PlaylistSerializer
    #permission_classes = [permissions.IsAuthenticated]

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)

    def get_queryset(self):
        # Permite que o usuário veja apenas suas próprias playlists
        return self.queryset.filter(user=self.request.user)
