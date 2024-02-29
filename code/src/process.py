import os
import uuid
import json
from typing import Optional

from fastapi import FastAPI, Header, HTTPException, Depends, BackgroundTasks
from celery import Celery
import redis
from fastapi.responses import JSONResponse
import requests

MAX_FILE_SIZE_FOR_SYNC_PROCESSING = 10485760  # 10 MB

# Leggi l'host e la porta del broker Redis dalle variabili d'ambiente
redis_host = os.environ.get('REDIS_HOST', 'localhost')
redis_port = int(os.environ.get('REDIS_PORT', 6379))
redis_expire = int(os.environ.get('REDIS_EXPIRE', 86400))

celery = Celery("tasks", broker="redis://{redis_host}:{redis_port}/0")
redis_client = redis.Redis(host=redis_host, port=redis_port, db=0)


def get_pipeline():
    from pipelines import pipe
    return pipe


def transcribe(file, background_tasks: BackgroundTasks):
    try:
        task_id = str(uuid.uuid4())
        result = ""
        background_tasks.add_task(process_audio_file, task_id, file)
        redis_client.setex(task_id, redis_expire,
                           json.dumps(dict(status="Processing", status_code=0, transcription="", error="")))
        return JSONResponse(
            status_code=200, content={"task_id": task_id,
                                      "status": "Processing",
                                      "status_code": 0,
                                      "transcription": result,
                                      "error": ""})
    except Exception as e:
        return JSONResponse(
            status_code=500, content={"task_id": "",
                                      "status": "Error",
                                      "status_code": 9,
                                      "transcription": "",
                                      "error": "Invalid: " + str(e)})


def immediate_transcribe(file):
    task_id = str(uuid.uuid4())
    try:
        result = process_audio_file(task_id, file)
        return JSONResponse(
            status_code=200, content={"task_id": task_id,
                                      "status": "Complete",
                                      "status_code": 1,
                                      "transcription": result,
                                      "error": ""})
    except Exception as e:
        return JSONResponse(
            status_code=500, content={"task_id": task_id,
                                      "status": "Error",
                                      "status_code": 9,
                                      "transcription": "",
                                      "error": "Invalid: " + str(e)})


def get_transcription(task_id):
    transcription = redis_client.get(task_id)
    transcription_data = json.loads(transcription.decode('utf-8'))
    if transcription is None:
        return JSONResponse(
            status_code=404, content={"task_id": task_id,
                                      "status": transcription_data['status'],
                                      "status_code": transcription_data['status_code'],
                                      "transcription": transcription_data['transcription'],
                                      "error": transcription_data['error']})
    else:
        if transcription_data['status_code'] == 9:
            return JSONResponse(
                status_code=400, content={"task_id": task_id,
                                          "status": transcription_data['status'],
                                          "status_code": transcription_data['status_code'],
                                          "transcription": transcription_data['transcription'],
                                          "error": transcription_data['error']})
        else:
            return JSONResponse(
                status_code=200, content={"task_id": task_id,
                                          "status": transcription_data['status'],
                                          "status_code": transcription_data['status_code'],
                                          "transcription": transcription_data['transcription'],
                                          "error": transcription_data['error']})


def get_file(file):
    try:
        response = requests.get(file.file_link)
        response.raise_for_status()
        file_content = response.content
        return file_content
    except requests.exceptions.RequestException as e:
        return None


@celery.task
def process_audio_file(task_id, file):
    try:
        file_data = get_file(file)
        if file_data is None:
            redis_client.setex(task_id,
                               redis_expire,
                               json.dumps(
                                   dict(status="Error", status_code=9, transcription="", error="File not found")))
        else:
            whisper_pipeline = get_pipeline()
            text = whisper_pipeline.predict_instant(file_data)
            result = process_transcription(text)
            redis_client.setex(task_id, redis_expire,
                               json.dumps(dict(status="Complete", status_code=1, transcription=result, error="")))
            return result
    except Exception as e:
        redis_client.setex(task_id, redis_expire,
                           json.dumps(dict(status="Error", status_code=9, transcription="", error=str(e))))


def process_transcription(text):
    result = text.replace("Weavods", "Wevoz")
    result = result.replace("Weavods", "Wevoz")
    result = result.replace("Iwots", "Wevoz")
    result = result.replace("WeWords", "Wevoz")
    result = result.replace("WeWats", "Wevoz")
    result = result.replace("wewots", "Wevoz")
    result = result.replace("WeWots", "Wevoz")
    result = result.replace("wewods", "Wevoz")
    result = result.replace("WeWods", "Wevoz")
    result = result.replace("we-wods", "Wevoz")
    result = result.replace("Weevoz", "Wevoz")
    result = result.replace("Weavots", "Wevoz")
    result = result.replace("Ui Uozo", "Wevoz")
    result = result.replace("WiiWatts", "Wevoz")
    result = result.replace("WeWATCH", "Wevoz")
    result = result.replace("WIWOTS", "Wevoz")
    result = result.replace("WeWATSU", "Wevoz")
    result = result.replace("We Vots", "Wevoz")
    result = result.replace("Vivoz", "Wevoz")
    result = result.replace("Weevoots", "Wevoz")
    result = result.replace("WeWATHS", "Wevoz")
    result = result.replace("IWATS", "Wevoz")
    result = result.replace("wevods", "Wevoz")
    result = result.replace("we watch", "Wevoz")
    result = result.replace("wewoods", "Wevoz")
    result = result.replace("WIWOTZ", "Wevoz")
    result = result.replace("WeWATS", "Wevoz")
    result = result.replace("we-vots", "Wevoz")
    result = result.replace("we wots", "Wevoz")
    result = result.replace("Weevoads", "Wevoz")
    result = result.replace("weavods", "Wevoz")
    result = result.replace("Simana", "Simona")
    result = result.replace("Malle", "Manlio")
    result = result.replace("Mahler None", "Manlio Arnone")

    return result
