from celery import Celery
from celery.utils.log import get_task_logger
import os
import sys
import requests
from fastapi import HTTPException

sys.path.append("/app/")

# URL = settings.endpoint
#TOKEN = settings.auth_token

celery = Celery(
    "tasks",
    broker="pyamqp://guest:guest@localhost//"
)

celery_log = get_task_logger(__name__)

def get_pipeline():
    from pipelines import pipe
    return pipe
 

@celery.task
def trancribe_audio(request_id, file_link):
    
    whisper_pipeline = get_pipeline()
    

    try:
        response = requests.get(file_link)
        response.raise_for_status()
        file_content = response.content
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=400, detail="Failed to download the audio file")

    
    text = whisper_pipeline.predict_instant(file_content)
    
    return text;

    #token = "Bearer " + TOKEN
    # Define the headers with the bearer token
    #headers = {"Authorization": token, "Content-Type": "application/json"}
    
    # Define the JSON payload
    #payload = {
    #    "request_id": request_id,
    #    "transcription": text,
    #}
    
    # Send the POST request with the JSON payload and headers
    #response = requests.post(URL, headers=headers, json=payload)
    
    # Check the response status code
    #if response.status_code == 200:
    #    print("Request successful!")
    #else:
    #    print("Request failed with status code:", response.status_code)
        
    
    #return {
    #    "request_id": request_id,
    #    "transcription": text,
    #}
    
