import requests
import sys
import os
from apisecrets import api_key

upload_url = 'https://api.assemblyai.com/v2/upload'
Transcription_endpoint = "https://api.assemblyai.com/v2/transcript"


if len(sys.argv) < 2:
    print("Usage: python main.py <audio-file>")
    sys.exit(1)
filename = sys.argv[1]
headers = {'authorization': api_key}

def upload(filename):
    def read_file(filename, chunk_size=5242880):
        with open(filename, 'rb') as _file:
            while True:
                data = _file.read(chunk_size)
                if not data:
                    break
                yield data


    
    response = requests.post(upload_url,
                            headers=headers,
                            data=read_file(filename))

    audio_url = response.json()['upload_url']
    return audio_url





def save_transcript(text, audio_filename):
    base = os.path.splitext(os.path.basename(audio_filename))[0]
    output_path = base + "_transcript.txt"
    with open(output_path, 'w') as f:
        f.write(text)
    print(f"Transcript saved to {output_path}")


def transcribe(audio_url):

    json = { "audio_url": audio_url, "speech_models": ["universal-2"] }


    response = requests.post(Transcription_endpoint, json=json, headers=headers)
    
    job_id = response.json()['id']
    return job_id




audio_url = upload(filename)
job_id = transcribe(audio_url)
print(job_id)


#polling endpoint
import time

polling_endpoint = Transcription_endpoint + "/" + job_id
while True:
    polling_response = requests.get(polling_endpoint, headers=headers).json()
    status = polling_response['status']
    print(f"Status: {status}")
    if status == 'completed':
        text = polling_response['text']
        print(text)
        save_transcript(text, filename)
        break
    elif status == 'error':
        print("Error:", polling_response.get('error'))
        break
    time.sleep(5)