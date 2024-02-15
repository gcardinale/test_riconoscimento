
import uuid
from fastapi import FastAPI, Header, HTTPException, Depends, BackgroundTasks
from celery import Celery
from redis import Redis
from fastapi.responses import JSONResponse
import requests

MAX_FILE_SIZE_FOR_SYNC_PROCESSING = 10485760  # 10 MB

celery = Celery("tasks", broker="redis://10.168.223.204:6379/0")
redis_client = Redis(host='10.168.223.204', port=6379, db=0)


def get_pipeline():
    from pipelines import pipe
    return pipe


async def transcribe(file, background_tasks: BackgroundTasks):
    file_data = await get_file(file)
    if file_data is None:
        return JSONResponse(content={"error": "Failed to download the audio file"}, status_code=400)
    else:
        task_id = str(uuid.uuid4())
        if file.size < MAX_FILE_SIZE_FOR_SYNC_PROCESSING:
            result = process_audio_file(task_id, file_data)
        else:
            result = ""
            background_tasks.add_task(process_audio_file, task_id, file_data)

        return {"task_id": task_id, "transcription": result}


async def get_transcription(task_id):
    transcription = redis_client.get(task_id)
    if transcription is None:
        return JSONResponse(content={"error": "Task not found"}, status_code=404)
    return {"task_id": task_id, "transcription": transcription.decode("utf-8")}


async def get_file(file):
    try:
        response = requests.get(file.file_link)
        response.raise_for_status()
        file_content = response.content
        return file_content
    except requests.exceptions.RequestException as e:
        return None


@celery.task
async def process_audio_file(task_id, file_content):
    whisper_pipeline = get_pipeline()
    text = whisper_pipeline.predict_instant(file_content)
    result = process_transcription(text)
    redis_client.set(task_id, result)
    return result


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
    result = result.replace("Simana", "Simona")
    result = result.replace("Mahler None", "Manlio Arnone")

    return result
