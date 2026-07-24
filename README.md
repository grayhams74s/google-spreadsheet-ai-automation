# Spreadsheet AI Automation

A Python starter project for reading data from a Google Spreadsheet using the Google Sheets API. It is set up to load credentials and spreadsheet settings from a local `.env` file.

![Spreadsheet AI Automation](images/AI%20Automation%20Spreadsheet.png)

## Requirements

- Python 3.10 or later
- A Google Cloud project with the Google Sheets API enabled
- A Google API key with access to the spreadsheet

## Setup

1. Create and activate a virtual environment.

   ```powershell
   python -m venv .venv
   .\.venv\Scripts\Activate.ps1
   ```

2. Install the dependencies.

   ```powershell
   pip install -r requirements.txt
   ```

3. Create a `.env` file in the project root:

   ```env
   GOOGLE_API_KEY=your_google_api_key
   SPREADSHEET_ID=your_spreadsheet_id
   SHEET_NAME=Sheet1!A:Z
   ```

   `SHEET_NAME` is currently passed directly to the API as a range, so use A1 notation. The worksheet tab name is not the spreadsheet file title. For example, use `Sheet1!A:Z`, or `'Sales Sheets'!A:Z` when the tab name contains spaces.

4. Run the script.

   ```powershell
   python main.py
   ```

## Project structure

```text
.
├── main.py             # Fetches values from Google Sheets
├── requirements.txt    # Python dependencies
├── images/             # Project images
└── .env                # Local configuration (not committed)
```

## Screenshot

![Google Sheets example](images/screenshots.png)

## Security

Never commit `.env` or share API keys. If a key is exposed, rotate it in Google Cloud and update your local `.env` file.
