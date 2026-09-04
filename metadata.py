"""Metadata handling for FLAC files."""

from mutagen.flac import FLAC
import os


def get_flac_metadata(filepath):
    """
    Extract metadata from a FLAC file.
    
    Args:
        filepath (str): Path to the FLAC file
        
    Returns:
        dict: Dictionary containing metadata
    """
    try:
        flac = FLAC(filepath)
        
        # Extract metadata with fallbacks
        title = flac.get('title', ['Unknown'])[0] if flac.get('title') else 'Unknown'
        artist = flac.get('artist', ['Unknown Artist'])[0] if flac.get('artist') else 'Unknown Artist'
        album = flac.get('album', ['Unknown Album'])[0] if flac.get('album') else 'Unknown Album'
        duration = flac.info.length if hasattr(flac.info, 'length') else 0
        
        return {
            'title': title,
            'artist': artist,
            'album': album,
            'duration': duration,
            'filename': os.path.basename(filepath)
        }
    except Exception as e:
        print(f"Error reading metadata from {filepath}: {e}")
        return {
            'title': os.path.basename(filepath),
            'artist': 'Unknown Artist',
            'album': 'Unknown Album',
            'duration': 0,
            'filename': os.path.basename(filepath)
        }


def format_duration(seconds):
    """
    Format duration in seconds to MM:SS format.
    
    Args:
        seconds (float): Duration in seconds
        
    Returns:
        str: Formatted duration string (MM:SS)
    """
    mins = int(seconds) // 60
    secs = int(seconds) % 60
    return f"{mins:02d}:{secs:02d}"
