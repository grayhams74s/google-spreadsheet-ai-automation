from langchain.chat_models import init_chat_model
from googleapiclient.discovery import build
from dotenv import load_dotenv
import os
import json


load_dotenv()

GOOGLE_SPREADSHEET_API_KEY = os.getenv('GOOGLE_SPREADSHEET_API_KEY')
SPREADSHEET_ID= os.getenv('SPREADSHEET_ID')
SHEET_NAME = os.getenv("SHEET_NAME")
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

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
    service = build("sheets", "v4", developerKey=GOOGLE_SPREADSHEET_API_KEY)

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

def clean_ai_response(response):
    """Extract clean text from an AI response."""
    content = response.content

    # Some models return plain text directly.
    if isinstance(content, str):
        return content.strip()

    # Gemini may return a list of blocks: [{"type": "text", "text": "..."}]
    text_parts = []

    for block in content:
        if isinstance(block, dict) and block.get("type") == "text":
            text_parts.append(block.get("text", ""))

    return "\n".join(text_parts).strip()

def summarize_with_ai(text):
    system_prompt = """
    You write concise email notifications for newly added spreadsheet records.

    Use plain text only. Do not use Markdown formatting, including asterisks,
    headings, or code blocks. Use hyphens for lists.

    Include a short subject line, the number of new records, and each record's
    Product Name, Product ID, and Price. Do not invent missing information.
    """

    model = init_chat_model(
        "gemini-3.5-flash-lite",
        api_key=GEMINI_API_KEY,
        model_provider="google_genai"
    )

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": f"New spreadsheet rows:\n{text}"}
    ]

    response = model.invoke(messages)
    return clean_ai_response(response)

all_rows, new_rows, headers = get_spreadsheet_data()

print("ALL ROWS", all_rows)
print("NEW ROWS", new_rows)

# Save IDs only after the new rows have been successfully processed.
if new_rows:
    processed_ids = get_processed_ids()

    for row in new_rows:
        processed_ids.add(row[1])  # Column B: Product ID

    save_processed_ids(processed_ids)

summary = summarize_with_ai(new_rows)
print(summary)