# Bitrix24 Deal Stage Updater

This script allows you to **bulk update deal stages in Bitrix24** using a webhook and an Excel file with a list of deal IDs.

---

## 🛠️ Requirements

Make sure you have Python 3.8+ installed.

Install dependencies with:

```bash
pip install pandas openpyxl requests
```
Tkinter is included by default in most Python installations. If not, install it via your package manager:

- **Ubuntu/Debian**: `sudo apt-get install python3-tk`
- **macOS**: Included
- **Windows**: Included

---
## 📁 Input Format

Prepare an Excel file (`.xlsx` or `.xls`) with the **first column** containing the `DEAL_ID`s you want to update:

| DEAL_ID   |
|-----------|
| 123456    |
| 789012    |
| ...       |

---

## 🚀 How to Run

1. Launch the script:

```bash
python move.py
```

2. You will be prompted to select an Excel file.
3. Enter your **Bitrix24 webhook URL**:
   ```
   https://yourcompany.bitrix24.com/rest/123/abc123/crm.deal.update
   ```
4. Enter the target **STAGE_ID** (e.g. `C7:UC_XYZABC`).
5. The script will:
   - Read the deal IDs
   - Update their stage via Bitrix24 API
   - Log results to `deal_update_log.txt`

---

## 🧠 Notes

- Each update request is spaced by **2 seconds** to avoid rate limits.
- The webhook URL must have access to the `crm.deal.update` method.
- If your Excel file is incorrectly formatted or the webhook is wrong, you'll get an error message.

---

## 📂 Output

The script will print and save a log file like:

```
✅ Deal 123456 moved successfully.
❌ Deal 789012 failed: {'error': 'invalid_request', 'error_description': '...'}
```

---

## 🧩 Example Use Case

If you need to move deals from stage “Proposal Sent” to “Negotiation” for a cleanup or migration, just extract those deal IDs into Excel and run this script.

---

## 📄 License

This project is licensed under the MIT License.
