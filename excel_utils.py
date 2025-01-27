from openpyxl import Workbook

def save_to_excel(data, filename="spotify_data.xlsx"):
    """
    Save data to an Excel file.
    
    Args:
        data (list of dicts): The data to save.
        filename (str): The name of the Excel file.
    """
    # Create a new workbook and select the active worksheet
    wb = Workbook()
    ws = wb.active

    # Write headers (keys of the first dictionary)
    if data:
        headers = data[0].keys()
        ws.append(headers)

        # Write data rows
        for row in data:
            ws.append([row.get(header) for header in headers])

    # Save the workbook
    wb.save(filename)
    print(f"Data saved to {filename}")