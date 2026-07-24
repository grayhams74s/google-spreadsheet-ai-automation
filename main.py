from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import json

load_dotenv()

GOOGLE_API_KEY = os.getenv('GOOGLE_API_KEY')
SPREADSHEET_ID= os.getenv('SPREADSHEET_ID')
SHEET_NAME = os.getenv("SHEET_NAME")

def get_processed_ids():
    if not os.path.exists("processed_ids.json"):
        return set()

    with open("processed_ids.json") as file:
        return set(json.load(file))


def save_processed_ids(processed_ids):
    with open("processed_ids.json", "w") as file:
        json.dump(list(processed_ids), file)


def get_spreadsheet_data():
    """Fetch only products that have not been processed yet."""
    service = build("sheets", "v4", developerKey=GOOGLE_API_KEY)

    all_rows = service.spreadsheets().values().get(
        spreadsheetId=SPREADSHEET_ID,
        range=SHEET_NAME
    ).execute().get("values", [])

    if not all_rows:
        return [], [], []

    headers = all_rows[0]
    data_rows = all_rows[1:]
    processed_ids = get_processed_ids()

    # Product ID is column B, index 1.
    new_rows = [
        row for row in data_rows
        if len(row) > 1 and row[1] not in processed_ids
    ]

    return all_rows, new_rows, headers


all_rows, new_rows, headers = get_spreadsheet_data()

print("ALL ROWS", all_rows)
print("NEW ROWS", new_rows)

# Save IDs only after the new rows have been successfully processed.
if new_rows:
    processed_ids = get_processed_ids()

    for row in new_rows:
        processed_ids.add(row[1])  # Column B: Product ID

    save_processed_ids(processed_ids)
