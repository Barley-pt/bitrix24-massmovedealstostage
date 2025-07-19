import pandas as pd
import requests
import time
import os

def main():
    print("📤 Bitrix24 Deal Stage Updater")

    # Prompt for Excel file
    excel_file = input("Enter the path to your Excel file (e.g., deals.xlsx): ").strip()
    if not os.path.exists(excel_file):
        print("❌ File not found. Please check the path.")
        return

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
