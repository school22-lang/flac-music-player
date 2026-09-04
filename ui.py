"""GUI components for FLAC Music Player."""

import tkinter as tk
from tkinter import filedialog, messagebox, ttk
import os
from metadata import get_flac_metadata, format_duration
from player import FlacPlayer


class FlacPlayerGUI:
    """
    Tkinter-based GUI for the FLAC music player.
    """
    
    def __init__(self, root):
        self.root = root
        self.root.title("FLAC Music Player")
        self.root.geometry("600x500")
        self.root.resizable(True, True)
        
        # Initialize player
        self.player = FlacPlayer()
        self.player.on_playback_finished = self.on_track_finished
        self.playlist = []
        self.current_track_index = -1
        self.update_job = None
        
        # Create GUI elements
        self.create_widgets()
        
    def create_widgets(self):
        """
        Create all GUI widgets.
        """
        # Title and info section
        info_frame = tk.Frame(self.root, bg="lightgray", height=100)
        info_frame.pack(fill=tk.BOTH, padx=10, pady=10)
        info_frame.pack_propagate(False)
        
        self.title_label = tk.Label(info_frame, text="No track loaded", font=("Arial", 14, "bold"), bg="lightgray")
        self.title_label.pack(anchor="w", padx=10, pady=5)
        
        self.artist_label = tk.Label(info_frame, text="Unknown Artist", font=("Arial", 10), bg="lightgray")
        self.artist_label.pack(anchor="w", padx=10)
        
        self.album_label = tk.Label(info_frame, text="Unknown Album", font=("Arial", 9), bg="lightgray")
        self.album_label.pack(anchor="w", padx=10, pady=(0, 5))
        
        # Progress bar
        progress_frame = tk.Frame(self.root)
        progress_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.time_label = tk.Label(progress_frame, text="00:00", font=("Arial", 9))
        self.time_label.pack(side=tk.LEFT)
        
        self.progress_var = tk.DoubleVar()
        self.progress_bar = ttk.Scale(progress_frame, from_=0, to=100, orient=tk.HORIZONTAL, 
                                      variable=self.progress_var, command=self.on_seek)
        self.progress_bar.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.duration_label = tk.Label(progress_frame, text="00:00", font=("Arial", 9))
        self.duration_label.pack(side=tk.LEFT)
        
        # Control buttons
        control_frame = tk.Frame(self.root)
        control_frame.pack(pady=10)
        
        self.prev_btn = tk.Button(control_frame, text="⏮ Previous", command=self.previous_track, width=12)
        self.prev_btn.pack(side=tk.LEFT, padx=5)
        
        self.play_btn = tk.Button(control_frame, text="▶ Play", command=self.play_pause, width=12)
        self.play_btn.pack(side=tk.LEFT, padx=5)
        
        self.stop_btn = tk.Button(control_frame, text="⏹ Stop", command=self.stop, width=12)
        self.stop_btn.pack(side=tk.LEFT, padx=5)
        
        self.next_btn = tk.Button(control_frame, text="⏭ Next", command=self.next_track, width=12)
        self.next_btn.pack(side=tk.LEFT, padx=5)
        
        # Volume control
        volume_frame = tk.Frame(self.root)
        volume_frame.pack(fill=tk.X, padx=10, pady=5)
        
        tk.Label(volume_frame, text="Volume:").pack(side=tk.LEFT, padx=5)
        self.volume_var = tk.DoubleVar(value=100)
        self.volume_scale = ttk.Scale(volume_frame, from_=0, to=100, orient=tk.HORIZONTAL, 
                                      variable=self.volume_var, command=self.on_volume_change)
        self.volume_scale.pack(side=tk.LEFT, fill=tk.X, expand=True, padx=5)
        
        self.volume_label = tk.Label(volume_frame, text="100%", width=5)
        self.volume_label.pack(side=tk.LEFT)
        
        # Playlist section
        playlist_label = tk.Label(self.root, text="Playlist", font=("Arial", 12, "bold"))
        playlist_label.pack(anchor="w", padx=10, pady=(10, 5))
        
        # Playlist listbox with scrollbar
        list_frame = tk.Frame(self.root)
        list_frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=5)
        
        scrollbar = ttk.Scrollbar(list_frame)
        scrollbar.pack(side=tk.RIGHT, fill=tk.Y)
        
        self.playlist_box = tk.Listbox(list_frame, yscrollcommand=scrollbar.set, height=10)
        self.playlist_box.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)
        self.playlist_box.bind('<Double-Button-1>', self.on_playlist_double_click)
        scrollbar.config(command=self.playlist_box.yview)
        
        # Playlist control buttons
        button_frame = tk.Frame(self.root)
        button_frame.pack(fill=tk.X, padx=10, pady=5)
        
        self.add_btn = tk.Button(button_frame, text="+ Add Song", command=self.add_song)
        self.add_btn.pack(side=tk.LEFT, padx=5)
        
        self.remove_btn = tk.Button(button_frame, text="- Remove", command=self.remove_song)
        self.remove_btn.pack(side=tk.LEFT, padx=5)
        
        self.clear_btn = tk.Button(button_frame, text="✕ Clear", command=self.clear_playlist)
        self.clear_btn.pack(side=tk.LEFT, padx=5)
    
    def add_song(self):
        """
        Add a FLAC song to the playlist.
        """
        file_path = filedialog.askopenfilename(
            title="Select FLAC file",
            filetypes=[("FLAC files", "*.flac"), ("All files", "*.*")]
        )
        
        if file_path:
            if os.path.isfile(file_path):
                self.playlist.append(file_path)
                metadata = get_flac_metadata(file_path)
                display_text = f"{metadata['title']} - {metadata['artist']}"
                self.playlist_box.insert(tk.END, display_text)
            else:
                messagebox.showerror("Error", "File not found")
    
    def remove_song(self):
        """
        Remove selected song from playlist.
        """
        try:
            index = self.playlist_box.curselection()[0]
            self.playlist_box.delete(index)
            self.playlist.pop(index)
        except IndexError:
            messagebox.showwarning("Warning", "Select a song to remove")
    
    def clear_playlist(self):
        """
        Clear the entire playlist.
        """
        if messagebox.askyesno("Confirm", "Clear entire playlist?"):
            self.playlist_box.delete(0, tk.END)
            self.playlist.clear()
            self.player.stop()
            self.current_track_index = -1
    
    def play_pause(self):
        """
        Toggle play/pause.
        """
        if self.player.is_playing:
            self.player.pause()
            self.play_btn.config(text="▶ Play")
        else:
            if self.current_track_index == -1 and self.playlist:
                self.current_track_index = 0
            
            if self.current_track_index >= 0 and self.current_track_index < len(self.playlist):
                file_path = self.playlist[self.current_track_index]
                if self.player.load_file(file_path):
                    self.player.play()
                    self.play_btn.config(text="⏸ Pause")
                    self.update_track_info()
                    self.start_update_loop()
                else:
                    messagebox.showerror("Error", f"Could not load file: {os.path.basename(file_path)}")
            else:
                messagebox.showwarning("Warning", "No song selected. Add a song to playlist.")
    
    def stop(self):
        """
        Stop playback.
        """
        self.player.stop()
        self.play_btn.config(text="▶ Play")
        self.progress_var.set(0)
        self.time_label.config(text="00:00")
    
    def next_track(self):
        """
        Play next track in playlist.
        """
        if self.playlist:
            self.current_track_index = (self.current_track_index + 1) % len(self.playlist)
            self.player.stop()
            self.play_pause()
    
    def previous_track(self):
        """
        Play previous track in playlist.
        """
        if self.playlist:
            self.current_track_index = (self.current_track_index - 1) % len(self.playlist)
            self.player.stop()
            self.play_pause()
    
    def on_track_finished(self):
        """
        Called when a track finishes playing.
        """
        self.next_track()
    
    def on_playlist_double_click(self, event):
        """
        Handle double-click on playlist item.
        """
        try:
            index = self.playlist_box.curselection()[0]
            self.current_track_index = index
            self.player.stop()
            self.play_pause()
        except IndexError:
            pass
    
    def on_seek(self, value):
        """
        Handle seek bar movement.
        """
        if self.player.duration > 0:
            position = (float(value) / 100) * self.player.duration
            self.player.seek(position)
    
    def on_volume_change(self, value):
        """
        Handle volume slider change.
        """
        volume = float(value) / 100
        self.player.set_volume(volume)
        self.volume_label.config(text=f"{int(float(value))}%")
    
    def update_track_info(self):
        """
        Update track information display.
        """
        if self.current_track_index >= 0 and self.current_track_index < len(self.playlist):
            file_path = self.playlist[self.current_track_index]
            metadata = get_flac_metadata(file_path)
            
            self.title_label.config(text=metadata['title'])
            self.artist_label.config(text=f"Artist: {metadata['artist']}")
            self.album_label.config(text=f"Album: {metadata['album']}")
            self.duration_label.config(text=format_duration(metadata['duration']))
    
    def start_update_loop(self):
        """
        Start updating progress bar and time display.
        """
        self.update_progress()
    
    def update_progress(self):
        """
        Update progress bar and time display.
        """
        if self.player.is_playing:
            current = self.player.get_position()
            duration = self.player.get_duration()
            
            if duration > 0:
                progress_percent = (current / duration) * 100
                self.progress_var.set(progress_percent)
            
            self.time_label.config(text=format_duration(current))
            
            # Schedule next update
            self.update_job = self.root.after(100, self.update_progress)
        else:
            if self.update_job:
                self.root.after_cancel(self.update_job)
                self.update_job = None
