# Installa le dipendenze necessarie
# pip install uvicorn fastapi python-multipart faster-whisper

from fastapi import FastAPI, File, UploadFile, Header, HTTPException, Depends
from fastapi.responses import JSONResponse
from faster_whisper import WhisperModel
import requests
from pydantic import BaseModel

app = FastAPI()

# Definisci la tua chiave segreta/token
SECRET_TOKEN = "6X7eG28XdmFiaKiAoVwq75"

class AudioFile(BaseModel):
    file_link: str

def get_pipeline():
    from pipelines import pipe
    return pipe

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
    is_token_valid: bool = Depends(verify_token) 
):

    whisper_pipeline = get_pipeline()

    try:
        response = requests.get(file.file_link)
        response.raise_for_status()
        file_content = response.content
    except requests.exceptions.RequestException as e:
        return JSONResponse(content={"error": "Failed to download the audio file"}, status_code=400)

    text = whisper_pipeline.predict_instant(file_content)

    result = text.replace("Weavods", "Wevoz")
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

    return {"transcription": result}

if __name__ == "__main__":
    import uvicorn

    # Avvia il server con uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)
