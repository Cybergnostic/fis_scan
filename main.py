import json
import os
import re
from scraper import scrape_receipt_data

# Учитавање података са QR кода
url = input("Унесите URL са QR кода: ")

# Скенирање података
receipt_data = scrape_receipt_data(url)

if receipt_data:
    # Екстракција метаподатака за име фајла (променити по потреби) 
    timestamp = receipt_data['metadata']['ПФР време (временска зона сервера)']
    shop_name = receipt_data['metadata']['Име продајног места']
    timestamp = re.sub(r'[\\/:*?"<>|]', '_', timestamp)
    shop_name = re.sub(r'[\\/:*?"<>|]', '_', shop_name)

    filename = f"{timestamp}_{shop_name}.json"

    # Чување података у JSON формату у фолдеру "receipts"
    with open(os.path.join('receipts', filename), 'w', encoding='utf-8') as jsonfile:
        json.dump(receipt_data, jsonfile, ensure_ascii=False, indent=4)

    print(f"Подаци о рачуну су сачувани у receipts/{filename}")