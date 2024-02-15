# Installa le dipendenze necessarie
# pip install uvicorn fastapi python-multipart faster-whisper
from typing import Optional

from fastapi import FastAPI, Header, HTTPException, Depends, BackgroundTasks
import process
from pydantic import BaseModel


class AudioFile(BaseModel):
    file_link: str


class TranscriptionResult(BaseModel):
    file_link: str
    force: Optional[bool]


app = FastAPI()


# Definisci la tua chiave segreta/token
SECRET_TOKEN = "6X7eG28XdmFiaKiAoVwq75"


# Funzione di dipendenza per verificare la presenza del token nella richiesta
def verify_token(authorization: str = Header(...)):
    token = authorization.split("Bearer ")[1]  # Estrai il token dal valore dell'header
    # Esegui la logica di verifica del token qui, ad esempio confrontalo con un token fisso
    expected_token = "6X7eG28XdmFiaKiAoVwq75"
    if token != expected_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True


@app.get("/")
def read_root():
    return {"status": "Server is online"}


@app.post("/transcribe")
def transcribe_audio(
        data: AudioFile,
        background_tasks: BackgroundTasks,
        is_token_valid: bool = Depends(verify_token)
):
    return process.transcribe(data, background_tasks=background_tasks)


@app.post("/transcribe/true")
def immediate_transcribe_audio(
        data: AudioFile,
        background_tasks: BackgroundTasks,
        is_token_valid: bool = Depends(verify_token)
):
    return process.immediate_transcribe(data)


@app.get("/transcribe/{task_id}")
def get_transcription(task_id: str, is_token_valid: bool = Depends(verify_token)):
    return process.get_transcription(task_id)


if __name__ == "__main__":
    import uvicorn

    # Avvia il server con uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
