# Usa un'immagine di base di Python
FROM python:3.8

# Imposta il lavoro di lavoro all'interno del container
WORKDIR /app

# Copia i file del tuo progetto nel container
COPY . .

# Installa le dipendenze
RUN pip install --no-cache-dir uvicorn fastapi python-multipart faster-whisper
RUN pip install --upgrade faster-whisper

# Espone la porta su cui il server FastAPI sarà in ascolto
EXPOSE 8000

# Comando di avvio del server FastAPI
CMD ["uvicorn", "app:app", "--host", "0.0.0.0", "--port", "8000"]
