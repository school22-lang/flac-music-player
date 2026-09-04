"""Audio playback logic for FLAC files."""

import sounddevice as sd
import soundfile as sf
import threading
import time


class FlacPlayer:
    """
    FLAC audio player using sounddevice and soundfile.
    """
    
    def __init__(self):
        self.current_file = None
        self.is_playing = False
        self.is_paused = False
        self.playback_thread = None
        self.audio_data = None
        self.sample_rate = None
        self.current_position = 0
        self.duration = 0
        self.stream = None
        self.volume = 1.0
        self.on_playback_finished = None
        
    def load_file(self, filepath):
        """
        Load a FLAC file.
        
        Args:
            filepath (str): Path to the FLAC file
            
        Returns:
            bool: True if successful, False otherwise
        """
        try:
            self.audio_data, self.sample_rate = sf.read(filepath, dtype='float32')
            self.current_file = filepath
            self.duration = len(self.audio_data) / self.sample_rate
            self.current_position = 0
            return True
        except Exception as e:
            print(f"Error loading file {filepath}: {e}")
            return False
    
    def play(self):
        """
        Start playing the loaded file.
        """
        if self.current_file is None:
            print("No file loaded")
            return
        
        if self.is_paused:
            # Resume from pause
            self.is_paused = False
            self.is_playing = True
            return
        
        # Start new playback in a separate thread
        self.is_playing = True
        self.current_position = 0
        self.playback_thread = threading.Thread(target=self._playback_worker, daemon=True)
        self.playback_thread.start()
    
    def _playback_worker(self):
        """
        Worker thread for audio playback.
        """
        try:
            # Apply volume
            audio_with_volume = self.audio_data * self.volume
            
            # Play audio
            sd.play(audio_with_volume, self.sample_rate)
            
            # Calculate actual duration in samples
            num_samples = len(self.audio_data)
            samples_per_second = self.sample_rate
            
            # Update position while playing
            while self.is_playing and sd.get_stream().active:
                # Get current position from sounddevice
                try:
                    current_frame = sd.get_stream().latency[0] * self.sample_rate
                    self.current_position = min(current_frame, num_samples) / samples_per_second
                except:
                    pass
                time.sleep(0.01)
            
            # Playback finished
            self.is_playing = False
            self.current_position = self.duration
            
            if self.on_playback_finished:
                self.on_playback_finished()
                
        except Exception as e:
            print(f"Error during playback: {e}")
            self.is_playing = False
    
    def pause(self):
        """
        Pause playback.
        """
        if self.is_playing:
            sd.stop()
            self.is_playing = False
            self.is_paused = True
    
    def stop(self):
        """
        Stop playback.
        """
        sd.stop()
        self.is_playing = False
        self.is_paused = False
        self.current_position = 0
    
    def seek(self, position):
        """
        Seek to a specific position in seconds.
        
        Args:
            position (float): Position in seconds
        """
        if self.audio_data is None:
            return
        
        position = max(0, min(position, self.duration))
        self.current_position = position
        
        if self.is_playing:
            self.stop()
            self.play()
    
    def set_volume(self, volume):
        """
        Set playback volume (0.0 to 1.0).
        
        Args:
            volume (float): Volume level
        """
        self.volume = max(0.0, min(1.0, volume))
    
    def get_position(self):
        """
        Get current playback position in seconds.
        
        Returns:
            float: Current position in seconds
        """
        return self.current_position
    
    def get_duration(self):
        """
        Get total duration in seconds.
        
        Returns:
            float: Duration in seconds
        """
        return self.duration
