import sounddevice as sd
import numpy as np
import threading
import time
import wave
import logging
from typing import Callable

logger = logging.getLogger(__name__)

class SpeechListener:
    def __init__(self, callback: Callable[[np.ndarray], None], chunk_duration_sec: int = 5):
        self.callback = callback
        self.chunk_duration_sec = chunk_duration_sec
        self.rate = 16000
        self.channels = 1
        
        self.is_listening = False
        self._thread = None
        
    def start_microphone(self):
        if self.is_listening:
            return
        self.is_listening = True
        self._thread = threading.Thread(target=self._record_and_dispatch, daemon=True)
        self._thread.start()
        logger.info("Started microphone listener using sounddevice.")
        
    def stop(self):
        self.is_listening = False
        if self._thread:
            self._thread.join()
        logger.info("Stopped microphone listener.")
            
    def _record_and_dispatch(self):
        frames_per_chunk = int(self.rate * self.chunk_duration_sec)
        
        try:
            with sd.InputStream(samplerate=self.rate, channels=self.channels, dtype='float32') as stream:
                while self.is_listening:
                    # Read 'frames_per_chunk' frames from the stream blockingly
                    data, overflowed = stream.read(frames_per_chunk)
                    
                    if overflowed:
                        logger.warning("Audio input overflow detected.")
                        
                    if self.is_listening and len(data) > 0:
                        # sounddevice returns data shape (frames, channels), flatten it for Whisper
                        np_data = data.flatten()
                        
                        # Dispatch in a separate thread so as not to block continuous recording
                        threading.Thread(target=self.callback, args=(np_data,), daemon=True).start()
                        
        except Exception as e:
            logger.error(f"Failed to open microphone: {e}. Ensure recording devices are available or run in simulation mode.")
            self.is_listening = False
            return

    def process_wav_file(self, file_path: str):
        """Simulate real-time streaming from a .wav file."""
        if not file_path.endswith('.wav'):
             logger.error("Only .wav files are supported for demo mode.")
             return
             
        try:
            wf = wave.open(file_path, 'rb')
            if wf.getnchannels() != 1 or wf.getframerate() != 16000:
                 logger.warning(f"WAV file {file_path} should ideally be 16kHz mono. Got {wf.getnchannels()} channels, {wf.getframerate()}Hz.")
                 
            chunk_frames = self.rate * self.chunk_duration_sec
            while True:
                data = wf.readframes(chunk_frames)
                if not data:
                    break
                
                # Assuming 16-bit PCM
                np_data = np.frombuffer(data, dtype=np.int16).astype(np.float32) / 32768.0
                self.callback(np_data)
                time.sleep(self.chunk_duration_sec) # simulate real-time processing time
            wf.close()
        except Exception as e:
            logger.error(f"Failed to process wav file {file_path}: {e}")
