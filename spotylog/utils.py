from .models import Track  # Import the Track class from models.py

def format_track_info(track_data):
    """
    Format track information for display.
    
    Args:
        track_data (dict): The raw track data from the Spotify API.
    
    Returns:
        str: A formatted string representation of the track.
    """
    track = Track(track_data)  # Create a Track object
    return str(track)  # Use the Track's __str__ method