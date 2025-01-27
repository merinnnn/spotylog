import csv
import json
from openpyxl import Workbook
from openpyxl.styles import Font, Alignment

def save_to_excel(data, filename="spotify_data.xlsx"):
    """Save data to an Excel file with formatting."""
    wb = Workbook()
    ws = wb.active

    if data:
        headers = data[0].keys()
        ws.append(headers)

        # Format headers
        for cell in ws[1]:
            cell.font = Font(bold=True)
            cell.alignment = Alignment(horizontal="center")

        # Write data rows
        for row in data:
            ws.append([row.get(header) for header in headers])

    wb.save(filename)
    print(f"Data saved to {filename}")

def save_to_csv(data, filename="spotify_data.csv"):
    """Save data to a CSV file."""
    with open(filename, mode="w", newline="", encoding="utf-8") as file:
        writer = csv.DictWriter(file, fieldnames=data[0].keys())
        writer.writeheader()
        writer.writerows(data)
    print(f"Data saved to {filename}")

def save_to_json(data, filename="spotify_data.json"):
    """Save data to a JSON file."""
    with open(filename, mode="w", encoding="utf-8") as file:
        json.dump(data, file, indent=4)
    print(f"Data saved to {filename}")

def save_recently_played_tracks_to_excel(tracks, filename="recently_played.xlsx"):
    """
    Save recently played tracks to an Excel file.
    
    Args:
        tracks (list): A list of recently played tracks.
        filename (str): The name of the Excel file.
    """
    data = []
    for track in tracks:
        played_at = track.get("played_at", "")
        track_data = track.get("track", {})
        data.append({
            "Played At": played_at,
            "Name": track_data.get("name"),
            "Artists": ", ".join(artist["name"] for artist in track_data.get("artists", [])),
            "Album": track_data.get("album", {}).get("name"),
        })
    save_to_excel(data, filename)
