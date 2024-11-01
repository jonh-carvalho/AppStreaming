from rest_framework import serializers
from .models import Content
from .models import Playlist
import os

class ContentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Content
        fields = '__all__'
    
    def validate_file_url(self, value):
        # Verifica a extensão do arquivo
        ext = os.path.splitext(value.name)[-1].lower()
        valid_extensions = ['.mp4', '.mp3']
        if ext not in valid_extensions:
            raise serializers.ValidationError("O conteúdo deve estar nos formatos .mp4 ou .mp3.")
        return value
        
class PlaylistSerializer(serializers.ModelSerializer):
    contents = ContentSerializer(many=True, read_only=True)
    content_ids = serializers.PrimaryKeyRelatedField(
        queryset=Content.objects.all(), write_only=True, many=True, source='contents'
    )

    class Meta:
        model = Playlist
        fields = ['id', 'title', 'description', 'user', 'contents', 'content_ids', 'created_at']
        read_only_fields = ['user', 'created_at']

    def create(self, validated_data):
        content_data = validated_data.pop('contents', [])
        playlist = super().create(validated_data)
        playlist.contents.set(content_data)
        return playlist

    def update(self, instance, validated_data):
        content_data = validated_data.pop('contents', None)
        playlist = super().update(instance, validated_data)
        if content_data is not None:
            playlist.contents.set(content_data)
        return playlist