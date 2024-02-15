# Installa le dipendenze necessarie
# pip install uvicorn fastapi python-multipart faster-whisper

from fastapi import FastAPI, Header, HTTPException, Depends, BackgroundTasks
from pydantic import BaseModel
import process

app = FastAPI()

# Definisci la tua chiave segreta/token
SECRET_TOKEN = "6X7eG28XdmFiaKiAoVwq75"


class AudioFile(BaseModel):
    file_link: str



# Funzione di dipendenza per verificare la presenza del token nella richiesta
async def verify_token(authorization: str = Header(...)):
    token = authorization.split("Bearer ")[1]  # Estrai il token dal valore dell'header
    # Esegui la logica di verifica del token qui, ad esempio confrontalo con un token fisso
    expected_token = "6X7eG28XdmFiaKiAoVwq75"
    if token != expected_token:
        raise HTTPException(status_code=401, detail="Unauthorized")
    return True


@app.get("/")
async def read_root():
    return {"status": "Server is online"}


@app.post("/transcribe/")
async def transcribe_audio(
        file: AudioFile,
        background_tasks: BackgroundTasks,
        is_token_valid: bool = Depends(verify_token)
):
    return await process.transcribe(file, background_tasks)


@app.get("/transcribe/{task_id}")
async def get_transcription(task_id: str):
    return await process.get_transcription(task_id)


if __name__ == "__main__":
    import uvicorn

    # Avvia il server con uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
