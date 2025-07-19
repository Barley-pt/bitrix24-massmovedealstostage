import pandas as pd
import requests
import time
import os
import tkinter as tk
from tkinter import filedialog

def select_excel_file():
    root = tk.Tk()
    root.withdraw()  # Hide the root window
    file_path = filedialog.askopenfilename(
        title="Select Excel File",
        filetypes=[("Excel files", "*.xlsx *.xls")]
    )
    return file_path

def main():
    print("📤 Bitrix24 Deal Stage Updater (v2.1)")

    # GUI file picker
    print("🔍 Please select your Excel file...")
    excel_file = select_excel_file()
    if not excel_file or not os.path.exists(excel_file):
        print("❌ File not selected or not found.")
        return
    print(f"📄 File selected: {excel_file}")

    # Prompt for Webhook
    webhook_url = input("Enter your full Bitrix24 webhook URL: ").strip()
    if not webhook_url.endswith("/crm.deal.update"):
        webhook_url = webhook_url.rstrip("/") + "/crm.deal.update"

    # Prompt for target stage ID
    stage_id = input("Enter the target STAGE_ID (e.g., C7:UC_XD9O3Q): ").strip()

    # Load Excel file
    try:
        df = pd.read_excel(excel_file)
        deal_ids = df.iloc[:, 0].dropna().astype(int).tolist()
    except Exception as e:
        print(f"❌ Error reading Excel file: {e}")
        return

    # Logging
    log_file = "deal_update_log.txt"
    with open(log_file, "w", encoding="utf-8") as log:
        for deal_id in deal_ids:
            payload = {
                "id": deal_id,
                "fields": {
                    "STAGE_ID": stage_id
                }
            }
            try:
                response = requests.post(webhook_url, json=payload)
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

    print("\n✅ Process finished. Log saved to 'deal_update_log.txt'")

if __name__ == "__main__":
    main()
