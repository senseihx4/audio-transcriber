from django.shortcuts import render
from rest_framework import viewsets, status
from rest_framework.permissions import AllowAny
from rest_framework.response import Response
from django.contrib.auth import login
from ailock.models import User
from ailock.serializers import UserSerializer, LoginSerializer, AudioTextSerializer, youtubeSerializer
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.permissions import IsAdminUser
from rest_framework.exceptions import ValidationError
import requests
import time
import tempfile
import wave
import pyaudio
from .apisecrets import api_key
from ailock.models import audiotext, yotubeaudio
from rest_framework import viewsets
from rest_framework.decorators import action
import json
import yt_dlp
from api import save_transcript, upload





class loginviewset(viewsets.ViewSet):
    permission_classes = [AllowAny]
    serializer_class = LoginSerializer

    def create(self, request):
        serializer = LoginSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        email = serializer.validated_data['email']
        password = serializer.validated_data['password']

        user = User.objects.filter(email=email).first()

        if user and user.check_password(password):
            login(request, user)
            refresh = RefreshToken.for_user(user)
            return Response({
                'access': str(refresh.access_token),
                'refresh': str(refresh),
            }, status=status.HTTP_200_OK)
        else:
            return Response({'detail': 'Invalid email or password.'}, status=status.HTTP_401_UNAUTHORIZED)


class userviewset(viewsets.ModelViewSet):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def get_permissions(self):
        if self.action == 'create':
            return [AllowAny()]
        return [IsAdminUser()]

    def perform_create(self, serializer):
        email = self.request.data.get('email')
        if User.objects.filter(email=email).exists():
            raise ValidationError({'email': 'A user with this email already exists.'})
        serializer.save()



class audiouploadviewset(viewsets.ModelViewSet):
    queryset = audiotext.objects.all()
    serializer_class = AudioTextSerializer
    permission_classes = [AllowAny]

    UPLOAD_URL = 'https://api.assemblyai.com/v2/upload'
    TRANSCRIPTION_ENDPOINT = 'https://api.assemblyai.com/v2/transcript'
    HEADERS = {'authorization': api_key}

    FRAMES_PER_BUFFER = 8192
    FORMAT = pyaudio.paInt16
    CHANNELS = 1
    INPUT_DEVICE_INDEX = 1  # pipewire — change if needed

    def _record_wav(self, seconds):
        p = pyaudio.PyAudio()
        rate = int(p.get_device_info_by_index(self.INPUT_DEVICE_INDEX)['defaultSampleRate'])
        stream = p.open(
            format=self.FORMAT,
            channels=self.CHANNELS,
            rate=rate,
            input=True,
            frames_per_buffer=self.FRAMES_PER_BUFFER,
            input_device_index=self.INPUT_DEVICE_INDEX,
        )
        frames = []
        for _ in range(int(rate / self.FRAMES_PER_BUFFER * seconds)):
            frames.append(stream.read(self.FRAMES_PER_BUFFER, exception_on_overflow=False))
        stream.stop_stream()
        stream.close()
        p.terminate()

        tmp = tempfile.NamedTemporaryFile(suffix='.wav', delete=False)
        with wave.open(tmp.name, 'wb') as obj:
            obj.setnchannels(self.CHANNELS)
            obj.setsampwidth(p.get_sample_size(self.FORMAT))
            obj.setframerate(rate)
            obj.writeframes(b''.join(frames))
        return tmp.name

    @action(detail=False, methods=['post'])
    def record(self, request):
        seconds = int(request.data.get('seconds', 5))
        wav_path = self._record_wav(seconds)

        with open(wav_path, 'rb') as f:
            audio_url = self._upload_audio(f)

        job_id = self._start_transcription(audio_url)
        transcript = self._poll_transcript(job_id)

        with open(wav_path, 'rb') as f:
            from django.core.files import File
            django_file = File(f, name='recording.wav')
            instance = audiotext.objects.create(
                audio_file=django_file,
                record_audiofile=django_file,
                user=request.user,
                text=transcript,
            )

        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def _upload_audio(self, file_obj):
        def read_chunks(f, chunk_size=5242880):
            while True:
                data = f.read(chunk_size)
                if not data:
                    break
                yield data

        response = requests.post(
            self.UPLOAD_URL,
            headers=self.HEADERS,
            data=read_chunks(file_obj),
        )
        return response.json()['upload_url']

    def _start_transcription(self, audio_url):
        payload = {'audio_url': audio_url, 'speech_models': ['universal-2']}
        response = requests.post(self.TRANSCRIPTION_ENDPOINT, json=payload, headers=self.HEADERS)
        data = response.json()
        if 'id' not in data:
            raise Exception(f"AssemblyAI error: {data}")
        return data['id']

    def _poll_transcript(self, job_id):
        polling_endpoint = f'{self.TRANSCRIPTION_ENDPOINT}/{job_id}'
        while True:
            data = requests.get(polling_endpoint, headers=self.HEADERS).json()
            if data['status'] == 'completed':
                return data['text']
            elif data['status'] == 'error':
                raise Exception(data.get('error', 'Transcription failed'))
            time.sleep(5)

    def create(self, request):
        audio_file = request.FILES.get('audio_file')
        if not audio_file:
            return Response({'error': 'audio_file is required'}, status=status.HTTP_400_BAD_REQUEST)

        audio_url = self._upload_audio(audio_file)
        job_id = self._start_transcription(audio_url)
        transcript = self._poll_transcript(job_id)

        instance = audiotext.objects.create(
            audio_file=audio_file,
            record_audiofile=audio_file,
            user=request.user,
            text=transcript,
        )
        serializer = self.get_serializer(instance)
        return Response(serializer.data, status=status.HTTP_201_CREATED)


class YoutubeViewSet(viewsets.ModelViewSet):
    queryset = yotubeaudio.objects.all()
    serializer_class = youtubeSerializer
    permission_classes = [AllowAny]

    TRANSCRIPTION_ENDPOINT = 'https://api.assemblyai.com/v2/transcript'
    HEADERS = {'authorization': api_key}

    def _get_audio_url(self, youtube_url):
        ydl_opts = {'format': 'bestaudio[ext=m4a]/bestaudio', 'quiet': True}
        with yt_dlp.YoutubeDL(ydl_opts) as ydl:
            info = ydl.extract_info(youtube_url, download=False)
        for f in info['formats']:
            if f.get('ext') == 'm4a':
                return f['url']
        return info['formats'][-1]['url']

    def _start_transcription(self, audio_url, sentiment_analysis=False):
        payload = {'audio_url': audio_url}
        if sentiment_analysis:
            payload['sentiment_analysis'] = True
        response = requests.post(self.TRANSCRIPTION_ENDPOINT, json=payload, headers=self.HEADERS)
        data = response.json()
        if 'id' not in data:
            raise Exception(f"AssemblyAI error: {data}")
        return data['id']

    def _poll_transcript(self, job_id):
        polling_endpoint = f'{self.TRANSCRIPTION_ENDPOINT}/{job_id}'
        while True:
            data = requests.get(polling_endpoint, headers=self.HEADERS).json()
            if data['status'] == 'completed':
                return data['text'], data.get('sentiment_analysis_results', [])
            elif data['status'] == 'error':
                raise Exception(data.get('error', 'Transcription failed'))
            time.sleep(5)

    def create(self, request):
        youtube_url = request.data.get('youtube_url')
        if not youtube_url:
            return Response({'error': 'youtube_url is required'}, status=status.HTTP_400_BAD_REQUEST)
        sentiment_analysis = request.data.get('sentiment_analysis', False)

        audio_url = self._get_audio_url(youtube_url)
        job_id = self._start_transcription(audio_url, sentiment_analysis=sentiment_analysis)
        transcript, sentiments = self._poll_transcript(job_id)

        instance = yotubeaudio.objects.create(
            youtube_url=youtube_url,
            record_audiofile='',
            user=request.user,
            text=transcript,
        )
        serializer = self.get_serializer(instance)
        response_data = dict(serializer.data)
        if sentiments:
            response_data['sentiment_analysis'] = sentiments
        return Response(response_data, status=status.HTTP_201_CREATED)

