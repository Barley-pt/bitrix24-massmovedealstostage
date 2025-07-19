import pandas as pd
import requests
import time

# CONFIGURATION
EXCEL_FILE = "deals.xlsx"  # Replace with your file name
WEBHOOK_URL = "https://fvl.bitrix24.com.br/rest/241/4n9rinmvhdpknq4k/crm.deal.update"
TARGET_STAGE = "C7:UC_XD9O3Q"
LOG_FILE = "deal_update_log.txt"

# Load Excel file (assumes single column with deal IDs)
try:
    df = pd.read_excel(EXCEL_FILE)
    deal_ids = df.iloc[:, 0].dropna().astype(int).tolist()
except Exception as e:
    print(f"Error reading Excel file: {e}")
    exit()

# Open log file
with open(LOG_FILE, "w", encoding="utf-8") as log:
    for deal_id in deal_ids:
        payload = {
            "id": deal_id,
            "fields": {
                "STAGE_ID": TARGET_STAGE
            }
        }
        try:
            response = requests.post(WEBHOOK_URL, json=payload)
            result = response.json()
            if result.get("result") is True:
                msg = f"✅ Deal {deal_id} moved successfully."
            else:
                msg = f"❌ Deal {deal_id} failed: {result}"
        except Exception as e:
            msg = f"❌ Deal {deal_id} error: {e}"

        print(msg)
        log.write(msg + "\n")
        time.sleep(2)

print("\nDone. Check 'deal_update_log.txt' for results.")
