import logging
from faster_whisper import WhisperModel
from io import BytesIO
#from config import settings

logging.basicConfig(level=logging.INFO)

# MODEL_PATH = settings.model_path

class WhisperPipeline:
    def __init__(self) -> None:
        # Run on GPU with FP16
        #self.model = WhisperModel("medium", device="cpu", compute_type="int8")
        self.model = WhisperModel("models/whisper-model-small", device="cpu", compute_type="int8", local_files_only=True)
        
        # self.warmup()
        
    # def predict_batched(self, audio_file):
    #     return self.batch_pipeline(audio_file)['text']
    
    def predict_instant(self, file_content):
        
        segments, info = self.model.transcribe(audio=BytesIO(file_content), beam_size=5, vad_filter=True)   
             
        logging.info("Detected language '%s' with probability %f" % (info.language, info.language_probability))

        text = ""
        for segment in segments:
            text = text + segment.text 
            
        return text
    
    

pipe = WhisperPipeline()