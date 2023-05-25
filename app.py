import logging
import tempfile
from fastapi import FastAPI
from celery_worker import trancribe_audio
from celery_worker import celery



app = FastAPI()


@app.get("/")
def read_main():
    return {"message": "This is the main app"}


@app.get("/get_task_status")
def read_task(celery_task_id: str):
    '''
    get the status of the task, use celery task id to get the status

    Parameters
    ----------
    celery_task_id : str
        task id of the celery task that was returned when the task training was started

    Returns
    -------
    dict
        task_id, task_status, task_result
    '''    
    task_result = celery.AsyncResult(celery_task_id)
    
    return {
        "task_id": celery_task_id,
        "task_status": task_result.status,
        "task_result": task_result.result,
    }


@app.post("/transcribe")
def transcribe_audio_file(
    request_id: str,
    file_link: str,
):


    print("in task")
    celery_task_id = trancribe_audio.delay(request_id, file_link)
    
    return {"request_id": request_id,
            "celery_task_id": celery_task_id.id}


if __name__ == "__main__":
    import uvicorn
    uvicorn.run("app:app", host="0.0.0.0", port=8005, log_level="info")
    