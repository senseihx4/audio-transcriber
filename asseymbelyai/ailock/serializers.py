from rest_framework import serializers
from ailock.models import audiotext, yotubeaudio, User


class AudioTextSerializer(serializers.ModelSerializer):
    audio_file = serializers.FileField(required=True)
    text = serializers.CharField(read_only=True)

    class Meta:
        model = audiotext
        fields = ['id', 'audio_file', 'record_audiofile', 'user', 'text']
        read_only_fields = ['id', 'text', 'record_audiofile', 'user']


class youtubeSerializer(serializers.ModelSerializer):
    youtube_url = serializers.URLField(required=True)
    text = serializers.CharField(read_only=True)

    class Meta:
        model = yotubeaudio
        fields = ['id', 'youtube_url', 'user', 'text']
        read_only_fields = ['id', 'text', 'user']


class UserSerializer(serializers.ModelSerializer):
    user_type_display = serializers.CharField(source='get_user_type_display', read_only=True)
    password = serializers.CharField(write_only=True, required=True)
    email = serializers.EmailField(required=True)
    class Meta:
        model = User
        fields = ['id', 'email', 'user_type', 'user_type_display', 'password']
        extra_kwargs = {
            'email': {'required': True},
            'user_type': {'required': True},
        }
        read_only_fields = ['id']


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField(required=True)
    password = serializers.CharField(required=True, write_only=True)




     